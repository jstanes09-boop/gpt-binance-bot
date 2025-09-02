from __future__ import annotations
from typing import Dict, Any
from .models import OrderResult
from .settings import Config

class ExchangeAdapter:
    """
    Minimal adapter. In dry_run, it simulates fills at a fake price.
    Later you can swap this to real Binance REST/websocket calls.
    """
    def __init__(self, cfg: Config | None = None):
        self.cfg = cfg or Config()

    def place_market(self, symbol: str, side: str, quote_amount: float) -> OrderResult:
        # Simulate a fill at a dummy price; real connector goes here.
        price = 100.0
        qty = quote_amount / price if price > 0 else 0.0
        return OrderResult(
            ok=True, symbol=symbol, side=side, qty=qty, price=price,
            order_id="SIM-DRYRUN", dry_run=self.cfg.dry_run, raw=None
        )
