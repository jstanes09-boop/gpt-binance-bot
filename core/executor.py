from typing import List, Dict, Any
from .risk import apply_risk

def place_orders(signals: List[Dict[str, Any]], dry_run: bool = True) -> Dict[str, Any]:
    """
    Apply risk to each signal and 'place' the order (simulated for now).
    Returns a summary so we can test wiring.
    """
    trades = []
    for s in signals:
        trade = {"symbol": s.get("symbol","UNK"), "side": s.get("side","BUY"), "size": s.get("size", 0)}
        trade = apply_risk(trade)
        if not dry_run:
            # real exchange logic will go here
            pass
        trades.append(trade)

    return {
        "placed": len(trades),
        "dry_run": dry_run,
        "trades": trades
    }
