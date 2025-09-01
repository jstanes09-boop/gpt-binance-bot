import argparse, json, pathlib
from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument("--days", type=int, default=7)
parser.add_argument("--coins", type=int, default=25)
parser.add_argument("--out", type=str, default="artifacts/smoke.json")
args = parser.parse_args()

pathlib.Path("artifacts").mkdir(parents=True, exist_ok=True)
result = {
    "type": "smoke",
    "days": args.days,
    "coins": args.coins,
    "timestamp": datetime.utcnow().isoformat()+"Z",
    "metrics": {"net_roi_30d": 0.0, "max_drawdown": 0.0, "win_rate": 0.0, "profit_factor": 1.0}
}
pathlib.Path(args.out).write_text(json.dumps(result, indent=2))
print("[smoke_backtest] wrote", args.out)

