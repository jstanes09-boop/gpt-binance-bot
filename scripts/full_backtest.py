import argparse, json, yaml, pathlib
from bot.backtest.engine import run

ap = argparse.ArgumentParser()
ap.add_argument("--config", required=True)
ap.add_argument("--days", type=int, default=60)
ap.add_argument("--out", default="artifacts/full.json")
args = ap.parse_args()

cfg = yaml.safe_load(pathlib.Path(args.config).read_text(encoding="utf-8"))
universe = cfg.get("symbols") or cfg.get("universe") or ["BTCUSDT","ETHUSDT"]

pathlib.Path("artifacts").mkdir(parents=True, exist_ok=True)
report = run(universe, days=args.days)
pathlib.Path(args.out).write_text(json.dumps(report, indent=2))
print("[full_backtest] wrote", args.out)
