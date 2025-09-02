from __future__ import annotations
import pandas as pd
import numpy as np

def _to_series(x) -> pd.Series:
    return x if isinstance(x, pd.Series) else pd.Series(x)

def sma(close, period: int) -> pd.Series:
    c = _to_series(close)
    return c.rolling(period, min_periods=period).mean()

def ema(close, period: int) -> pd.Series:
    c = _to_series(close)
    return c.ewm(span=period, adjust=False).mean()

def rsi(close, period: int = 14) -> pd.Series:
    c = _to_series(close)
    delta = c.diff()
    up = delta.clip(lower=0)
    down = (-delta.clip(upper=0))
    avg_gain = up.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    avg_loss = down.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)

def atr(high, low, close, period: int = 14) -> pd.Series:
    h, l, c = map(_to_series, (high, low, close))
    prev_close = c.shift(1)
    tr = pd.concat([(h - l), (h - prev_close).abs(), (l - prev_close).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False, min_periods=period).mean()

def macd(close, fast: int = 12, slow: int = 26, signal: int = 9):
    c = _to_series(close)
    m = ema(c, fast) - ema(c, slow)
    s = m.ewm(span=signal, adjust=False).mean()
    hist = m - s
    return m, s, hist
