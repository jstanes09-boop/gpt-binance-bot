param(
  [Parameter(Mandatory=$true)][string]$Feature
)
$rep = "artifacts\report_$Feature.html"
if (Test-Path $rep) {
  Write-Host "[open_report] $rep"
  Start-Process $rep
} else {
  Write-Error "Report not found: $rep (run experiment first)"
}
