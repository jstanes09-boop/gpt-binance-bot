from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Signal:
    symbol: str
    side: str          # "BUY" or "SELL"
    size: float        # position size in quote currency (e.g., USDT)
    meta: Optional[Dict[str, Any]] = None

@dataclass
class Trade:
    symbol: str
    side: str
    size: float
    tp: float          # take-profit (fraction, e.g., 0.02)
    sl: float          # stop-loss  (fraction)
    meta: Optional[Dict[str, Any]] = None

@dataclass
class OrderResult:
    ok: bool
    symbol: str
    side: str
    qty: float
    price: float
    order_id: str
    dry_run: bool
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

