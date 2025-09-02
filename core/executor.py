from __future__ import annotations
from typing import List, Dict, Any
from .risk import apply_risk
from .fees import apply_fee
from .models import Signal, Trade, OrderResult
from .exchange_adapter import ExchangeAdapter
from .settings import Config

def _to_signal(d: Dict[str, Any]) -> Signal:
    return Signal(
        symbol=d.get("symbol","UNK"),
        side=d.get("side","BUY").upper(),
        size=float(d.get("size", 0.0)),
        meta=d.get("meta")
    )

def place_orders(signals: List[Dict[str, Any] | Signal], dry_run: bool | None = None) -> Dict[str, Any]:
    """
    Convert incoming signals -> risk-managed trades -> submit via ExchangeAdapter.
    Returns a summary including per-order results.
    """
    cfg = Config()
    if dry_run is not None:
        cfg.dry_run = bool(dry_run)

    adapter = ExchangeAdapter(cfg)
    norm_signals = [s if isinstance(s, Signal) else _to_signal(s) for s in signals]

    trades: List[Trade] = []
    for s in norm_signals:
        trade = {"symbol": s.symbol, "side": s.side, "size": s.size, "meta": s.meta or {}}
        trade = apply_risk(trade)  # adds tp/sl
        trades.append(Trade(**trade))

    results: List[OrderResult] = []
    for t in trades:
        # Apply fee on the quote amount up front (simple model)
        quote_amount = apply_fee(t.size, rate=cfg.fee_rate)
        res = adapter.place_market(t.symbol, t.side, quote_amount)
        results.append(res)

    return {
        "placed": sum(1 for r in results if r.ok),
        "dry_run": cfg.dry_run,
        "results": [r.to_dict() for r in results],
    }
