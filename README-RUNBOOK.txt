RUNBOOK (Quick)

Baseline:
  python scripts\full_backtest.py --config config\markets_top200.yaml --days 60 --out artifacts\baseline.json

Experiment:
  python experiments\run_experiment.py --feature <feature> --days 60 --out artifacts\exp_<feature>.json
  python experiments\compare_to_baseline.py --baseline artifacts\baseline.json --candidate artifacts\exp_<feature>.json --thresholds config\thresholds.yaml --out artifacts\decision_<feature>.json
  python experiments\report.py --baseline artifacts\baseline.json --candidate artifacts\exp_<feature>.json --decision artifacts\decision_<feature>.json --html artifacts\report_<feature>.html
  python build.py apply-decision --feature <feature> --decision artifacts\decision_<feature>.json

Helpers (PowerShell):
  .\scripts\baseline.ps1
  .\scripts\experiment.ps1 adaptive_trailing_tp
  .\scripts\apply_decision.ps1 adaptive_trailing_tp
  .\scripts\open_report.ps1 adaptive_trailing_tp
