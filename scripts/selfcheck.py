import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import bot.core.signals as S
import bot.core.executor as E
import bot.core.risk as R
import bot.core.portfolio as P
from bot.features.adaptive_trailing_tp import adjust_take_profit

# Dummy signal (since generate_signals is a placeholder)
test_signals = [{"symbol": "BTCUSDT", "side": "BUY", "size": 100}]
summary = E.place_orders(test_signals, dry_run=True)
tp_level = adjust_take_profit(price=50000, atr=100, k=2.0)

print("[selfcheck] orders placed:", summary["placed"], "dry_run:", summary["dry_run"])
print("[selfcheck] sample TP level:", tp_level)
print("[selfcheck] portfolio snapshot:", P.snapshot())
