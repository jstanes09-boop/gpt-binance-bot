import time, sys, pathlib, os
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

from bot.core import signals as S
from bot.core.executor import place_orders
from bot.core.settings import Config

poll = int(os.getenv("LOOP_SECONDS","10"))
print("[loop] starting; poll =", poll, "seconds")
while True:
    sigs = S.generate_signals()
    if sigs:
        summary = place_orders(sigs, dry_run=Config().dry_run)
        print("[loop] placed:", summary["placed"], "dry_run:", summary["dry_run"])
    else:
        print("[loop] no signals")
    time.sleep(poll)
