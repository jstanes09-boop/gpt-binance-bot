import argparse, json, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("--baseline", required=True)
ap.add_argument("--candidate", required=True)
ap.add_argument("--thresholds", required=True)
ap.add_argument("--out", required=True)
args = ap.parse_args()

baseline = json.loads(pathlib.Path(args.baseline).read_text())
candidate = json.loads(pathlib.Path(args.candidate).read_text())

approved = candidate["metrics"].get("profit_factor",1.0) >= baseline["metrics"].get("profit_factor",1.0)
decision = {
    "approved": approved,
    "net_roi_30d_delta": candidate["metrics"].get("net_roi_30d",0) - baseline["metrics"].get("net_roi_30d",0),
    "max_drawdown_delta": candidate["metrics"].get("max_drawdown",0) - baseline["metrics"].get("max_drawdown",0)
}
pathlib.Path(args.out).write_text(json.dumps(decision, indent=2))
print("[compare_to_baseline] wrote", args.out, "approved=", approved)
