import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

from bot.core.executor import place_orders

signals = [
    {"symbol": "BTCUSDT", "side": "BUY",  "size": 100.0},
    {"symbol": "ETHUSDT", "side": "SELL", "size": 50.0},
]
summary = place_orders(signals, dry_run=True)
print("[demo] placed:", summary["placed"], "dry_run:", summary["dry_run"])
for r in summary["results"]:
    print(" ", r["symbol"], r["side"], "qty=", round(r["qty"], 6), "price=", r["price"])
