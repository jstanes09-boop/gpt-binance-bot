param(
  [Parameter(Mandatory=$true)][string]$Feature,
  [int]$Days = 60
)
$exp = "artifacts\exp_$Feature.json"
$dec = "artifacts\decision_$Feature.json"
$rep = "artifacts\report_$Feature.html"

Write-Host "[experiment] feature=$Feature"
python experiments\run_experiment.py --feature $Feature --days $Days --out $exp
python experiments\compare_to_baseline.py --baseline artifacts\baseline.json --candidate $exp --thresholds config\thresholds.yaml --out $dec
python experiments\report.py --baseline artifacts\baseline.json --candidate $exp --decision $dec --html $rep
Write-Host "[experiment] finished. Report -> $rep"
