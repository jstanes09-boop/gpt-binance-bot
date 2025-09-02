from __future__ import annotations
import json, pathlib, math
import numpy as np, pandas as pd
from datetime import timedelta
from bot.core import indicators as I

def _load_prices(symbol: str, days: int) -> pd.DataFrame:
    p = pathlib.Path(f"data/{symbol}_1h.csv")
    if p.exists():
        df = pd.read_csv(p)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    else:
        # fallback synthetic 1h prices
        n = max(24*days, 200)
        rng = np.random.default_rng(0)
        ts = pd.date_range(end=pd.Timestamp.utcnow(), periods=n, freq="H")
        ret = rng.normal(0, 0.001, n)
        close = 100 * np.exp(np.cumsum(ret))
        high = close * (1 + rng.normal(0.0005, 0.0007, n).clip(min=0))
        low  = close * (1 - rng.normal(0.0005, 0.0007, n).clip(min=0))
        df = pd.DataFrame({"timestamp": ts, "open": close, "high": high, "low": low, "close": close, "volume": 0})
    # last N days only
    cutoff = df["timestamp"].max() - timedelta(days=days)
    df = df[df["timestamp"] >= cutoff].reset_index(drop=True)
    return df

def _metrics_from_equity(eq: pd.Series) -> dict:
    eq = eq.fillna(method="ffill").fillna(1.0)
    ret_total = eq.iloc[-1] - 1.0
    roll_max = eq.cummax()
    dd = (eq / roll_max) - 1.0
    max_dd = dd.min()
    return {"net_roi_30d": ret_total*100.0, "max_drawdown": abs(max_dd)*100.0}

def _trade_stats(rets: pd.Series) -> dict:
    # rough win/loss/profit factor
    wins = rets[rets > 0].sum()
    losses = -rets[rets < 0].sum()
    win_count = int((rets > 0).sum())
    loss_count = int((rets < 0).sum())
    pf = (wins / max(losses, 1e-9)) if losses > 0 else float("inf")
    trades = win_count + loss_count
    win_rate = (win_count / max(trades, 1)) * 100.0
    return {"profit_factor": float(pf), "win_rate": win_rate, "trades": trades}

def _sma_cross_strategy(df: pd.DataFrame, fast=20, slow=50) -> dict:
    c = pd.Series(df["close"].astype(float))
    fast_sma = c.rolling(fast, min_periods=fast).mean()
    slow_sma = c.rolling(slow, min_periods=slow).mean()
    pos = (fast_sma > slow_sma).astype(int)
    rets = c.pct_change().fillna(0)
    strat_ret = (pos.shift(1).fillna(0) * rets)
    eq = (1 + strat_ret).cumprod()
    # trade-level returns (entry at cross)
    cross = pos.diff().fillna(0)
    entries = cross[cross == 1].index.tolist()
    exits = cross[cross == -1].index.tolist()
    if exits and entries and exits[0] < entries[0]: exits.pop(0)
    if entries and (not exits or entries[-1] > exits[-1]): exits.append(len(df)-1)
    trade_rets = []
    for a, b in zip(entries, exits):
        trade_rets.append(float((c.iloc[b] / c.iloc[a]) - 1.0))
    trade_rets = pd.Series(trade_rets) if trade_rets else pd.Series(dtype=float)
    out = {"equity": eq, "trade_returns": trade_rets}
    out.update(_metrics_from_equity(eq))
    out.update(_trade_stats(trade_rets))
    return out

def run(universe: list[str], days: int = 60) -> dict:
    per = []
    for sym in universe:
        df = _load_prices(sym, days)
        res = _sma_cross_strategy(df)
        per.append({"symbol": sym, **{k:v for k,v in res.items() if k!='equity' and k!='trade_returns'}})
    # aggregate
    agg = {}
    for k in ["net_roi_30d","max_drawdown","profit_factor","win_rate","trades"]:
        vals = [x[k] for x in per if k in x]
        agg[k] = float(np.mean(vals)) if vals else 0.0
    return {"universe": universe, "days": days, "metrics": agg, "per_symbol": per}
