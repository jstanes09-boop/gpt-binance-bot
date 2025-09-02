import argparse, json, pathlib
from bot.backtest.engine import run
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--days", type=int, default=7)
parser.add_argument("--coins", type=int, default=2)  # ignored for now
parser.add_argument("--out", type=str, default="artifacts/smoke.json")
args = parser.parse_args()

pathlib.Path("artifacts").mkdir(parents=True, exist_ok=True)
res = run(["BTCUSDT","ETHUSDT"], days=args.days)
pathlib.Path(args.out).write_text(json.dumps(res, indent=2))
print("[smoke_backtest] wrote", args.out)
