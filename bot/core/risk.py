from typing import Dict, Any
DEFAULT_TP=0.02; DEFAULT_SL=0.01
def apply_risk(trade: Dict[str, Any]) -> Dict[str, Any]:
    trade=dict(trade); trade.setdefault("tp",DEFAULT_TP); trade.setdefault("sl",DEFAULT_SL); return trade
