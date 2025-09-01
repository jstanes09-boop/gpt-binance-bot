param(
  [string]$ArchivePath
)

if (-not $ArchivePath) {
  $ArchivePath = Read-Host "Enter path to your old bot folder (e.g. C:\GBT-bot-archive-2025-09-01)"
}
if (-not (Test-Path $ArchivePath)) {
  Write-Error "Archive path not found: $ArchivePath"
  exit 1
}

$map = @{
  "signals.py"  = "bot\core\signals.py";
  "executor.py" = "bot\core\executor.py";
  "risk.py"     = "bot\core\risk.py";
  "fees.py"     = "bot\core\fees.py";
}

foreach ($srcName in $map.Keys) {
  $srcPath = Join-Path $ArchivePath $srcName
  if (-not (Test-Path $srcPath)) {
    # try to find in subfolders (common cases)
    $candidates = Get-ChildItem -Path $ArchivePath -Recurse -Filter $srcName -File -ErrorAction SilentlyContinue
    if ($candidates.Count -gt 0) { $srcPath = $candidates[0].FullName } else { continue }
  }

  $dstPath = Join-Path (Get-Location) $map[$srcName]
  $dstDir  = Split-Path $dstPath -Parent
  New-Item -ItemType Directory -Force -Path $dstDir | Out-Null

  if (Test-Path $dstPath) {
    Copy-Item $dstPath "$dstPath.bak" -Force
    Write-Host "[backup] $dstPath -> $dstPath.bak"
  }

  Copy-Item $srcPath $dstPath -Force
  Write-Host "[migrate] $srcName -> $dstPath"
}

Write-Host "[migrate] done. Now run: python scripts\selfcheck.py"
