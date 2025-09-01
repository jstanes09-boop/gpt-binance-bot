$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
New-Item -ItemType Directory -Force -Path backups | Out-Null
$zip = "backups\bot_$timestamp.zip"

$exclude = @("backups","__pycache__",".venv","artifacts","dist","reports",".git")
$files = Get-ChildItem -Recurse -File | Where-Object {
  $p = $_.FullName
  -not ($exclude | ForEach-Object { $p -like "*\$_\*" })
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipStream = [System.IO.Compression.ZipFile]::Open($zip, 'Create')
foreach ($f in $files) {
  $rel = Resolve-Path -Relative $f
  [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zipStream, $f.FullName, $rel, 'Optimal') | Out-Null
}
$zipStream.Dispose()
Write-Host "Saved local backup -> $zip"
 