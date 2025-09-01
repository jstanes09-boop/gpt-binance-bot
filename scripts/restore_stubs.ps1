$targets = @("bot\core\signals.py","bot\core\executor.py","bot\core\risk.py","bot\core\fees.py")
foreach ($t in $targets) {
  $bak = "$t.bak"
  if (Test-Path $bak) {
    Copy-Item $bak $t -Force
    Write-Host "[restore] $bak -> $t"
  }
}
Write-Host "[restore] done."

