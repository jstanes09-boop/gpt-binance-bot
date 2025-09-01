param(
  [Parameter(Mandatory=$true)][string]$Feature
)
$dec = "artifacts\decision_$Feature.json"
if (!(Test-Path $dec)) {
  Write-Error "Decision file not found: $dec (run experiment first)"
  exit 1
}
python build.py apply-decision --feature $Feature --decision $dec
Write-Host "[apply_decision] done for $Feature"
