from typing import List, Dict, Any
from .risk import apply_risk
def place_orders(signals: List[Dict[str, Any]], dry_run: bool = True) -> Dict[str, Any]:
    trades=[]
    for s in signals:
        trade={"symbol": s.get("symbol","UNK"), "side": s.get("side","BUY"), "size": s.get("size",0)}
        trade=apply_risk(trade); trades.append(trade)
    return {"placed": len(trades), "dry_run": dry_run, "trades": trades}
