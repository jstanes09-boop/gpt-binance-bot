import sys, pathlib, importlib

# Ensure project root (C:\GBT-bot) is on sys.path
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

for m in ("bot.core.signals", "bot.core.executor", "bot.core.risk"):
    importlib.import_module(m)
print("[tests] imports OK")
