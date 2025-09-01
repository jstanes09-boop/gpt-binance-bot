from typing import Dict, Any

DEFAULT_TP = 0.02   # 2%
DEFAULT_SL = 0.01   # 1%

def apply_risk(trade: Dict[str, Any]) -> Dict[str, Any]:
    """
    Attach simple TP/SL to a trade dict. Replace with your real logic later.
    """
    trade = dict(trade)
    trade.setdefault("tp", DEFAULT_TP)
    trade.setdefault("sl", DEFAULT_SL)
    return trade
