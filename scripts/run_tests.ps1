Write-Host "[tests] starting..."
python - << 'PY'
import importlib, sys
for m in ["bot.core.signals","bot.core.executor","bot.core.risk"]:
    importlib.import_module(m)
print("[tests] imports OK")
PY

python scripts\selfcheck.py
python scripts\smoke_backtest.py --days 1 --coins 1 --out artifacts\smoke.json
Write-Host "[tests] complete."
