param(
  [int]$Days = 60,
  [string]$Config = "config\markets_top200.yaml",
  [string]$Out = "artifacts\baseline.json"
)
Write-Host "[baseline] running..."
python scripts\full_backtest.py --config $Config --days $Days --out $Out
Write-Host "[baseline] wrote $Out"
