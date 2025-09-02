import importlib
for m in ("bot.core.signals", "bot.core.executor", "bot.core.risk"):
    importlib.import_module(m)
print("[tests] imports OK")
