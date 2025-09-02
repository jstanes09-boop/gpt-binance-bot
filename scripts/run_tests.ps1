Write-Host "[tests] starting..."
python scripts\import_check.py
python scripts\selfcheck.py
python scripts\smoke_backtest.py --days 1 --coins 1 --out artifacts\smoke.json
Write-Host "[tests] complete."
