from __future__ import annotations
import os, math
from typing import Dict, Any
import ccxt
from .models import OrderResult
from .settings import Config

def _round_step(value: float, step: float) -> float:
    if step <= 0: return value
    return math.floor(value / step) * step

class ExchangeAdapter:
    """
    Binance Spot via ccxt. If cfg.dry_run=True -> simulate.
    If BINANCE_TESTNET=true -> ccxt sandbox (https://testnet.binance.vision).
    Quote-based sizing: provide quote_amount (e.g., 10 USDT), we convert to base qty.
    """
    def __init__(self, cfg: Config | None = None):
        self.cfg = cfg or Config()
        self._ex = None
        if not self.cfg.dry_run:
            self._ex = ccxt.binance({
                "apiKey": self.cfg.binance_key,
                "secret": self.cfg.binance_secret,
                "enableRateLimit": True,
                "options": {"defaultType": "spot"},
            })
            if os.getenv("BINANCE_TESTNET", "true").lower() in ("1","true","yes"):
                # ccxt toggles URLs to testnet
                self._ex.set_sandbox_mode(True)
            self._ex.load_markets()

    def _market(self, symbol: str) -> Dict[str, Any]:
        return self._ex.market(symbol) if self._ex else {}

    def _price(self, symbol: str) -> float:
        if self._ex:
            return float(self._ex.fetch_ticker(symbol)["last"])
        return 100.0  # dry-run dummy

    def place_market(self, symbol: str, side: str, quote_amount: float) -> OrderResult:
        side = side.lower()
        price = self._price(symbol)
        qty = quote_amount / price if price > 0 else 0.0

        if self._ex:
            m = self._market(symbol)
            amt_step = m.get("limits", {}).get("amount", {}).get("min") or m.get("precision", {}).get("amount")
            if isinstance(amt_step, float) and amt_step > 0:
                qty = _round_step(qty, amt_step)
            # Notional min
            min_cost = m.get("limits", {}).get("cost", {}).get("min")
            if min_cost and quote_amount < float(min_cost):
                raise ValueError(f"Quote amount {quote_amount} < min notional {min_cost} for {symbol}")
            order = self._ex.create_order(symbol, "market", side, qty, None)
            return OrderResult(True, symbol, side.upper(), qty, price, str(order.get("id","ORDER")), self.cfg.dry_run, raw=order)

        # dry-run path (no exchange)
        return OrderResult(True, symbol, side.upper(), qty, price, "SIM-DRYRUN", True, raw=None)
