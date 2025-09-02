from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Signal:
    symbol: str
    side: str
    size: float
    meta: Optional[Dict[str, Any]] = None

@dataclass
class Trade:
    symbol: str
    side: str
    size: float
    tp: float
    sl: float
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
    def to_dict(self) -> Dict[str, Any]: return asdict(self)
