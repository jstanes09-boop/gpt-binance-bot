param([Parameter(Mandatory=$true)][string]$ArchivePath)
if (!(Test-Path $ArchivePath)) { Write-Error "Archive not found: $ArchivePath"; exit 1 }
$dst = "bot\core\signals.py"
$match = Get-ChildItem -Path $ArchivePath -Recurse -Filter signals.py -File -ErrorAction SilentlyContinue | Select-Object -First 1
if (!$match) { Write-Error "Could not find signals.py under $ArchivePath"; exit 1 }
if (Test-Path $dst) { Copy-Item $dst "$dst.bak" -Force; Write-Host "[backup] $dst -> $dst.bak" }
Copy-Item $match.FullName $dst -Force
Write-Host "[migrate] signals.py -> $dst"
