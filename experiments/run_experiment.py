import argparse, json, pathlib
from datetime import datetime

ap = argparse.ArgumentParser()
ap.add_argument("--feature", required=True)
ap.add_argument("--days", type=int, default=60)
ap.add_argument("--out", default="artifacts/exp.json")
args = ap.parse_args()

pathlib.Path("artifacts").mkdir(parents=True, exist_ok=True)
res = {
    "feature": args.feature,
    "days": args.days,
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "metrics": {"net_roi_30d": 0.0, "max_drawdown": 0.0, "win_rate": 0.0, "profit_factor": 1.0}
}
pathlib.Path(args.out).write_text(json.dumps(res, indent=2))
print("[run_experiment] wrote", args.out)
