import json, argparse, sys, pathlib

FEATURES = pathlib.Path("config/features.json")
CHANGELOG = pathlib.Path("CHANGELOG.md")
VERSION = pathlib.Path("VERSION")

def set_flag(key, enabled: bool):
    cfg = json.loads(FEATURES.read_text(encoding="utf-8"))
    for f in cfg["features"]:
        if f["key"] == key:
            f["enabled"] = bool(enabled)
            FEATURES.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            print(f"[build] feature '{key}' -> enabled={enabled}")
            return 0
    print(f"[build] feature '{key}' not found", file=sys.stderr)
    return 1

def bump_version(level="patch"):
    ver = VERSION.read_text().strip() if VERSION.exists() else "0.1.0"
    major, minor, patch = map(int, ver.split("."))
    if level == "major": major, minor, patch = major+1, 0, 0
    elif level == "minor": minor, patch = minor+1, 0
    else: patch += 1
    new = f"{major}.{minor}.{patch}"
    VERSION.write_text(new)
    print(f"[build] version -> {new}")
    return new

def log_change(key, dec, approved):
    prev = CHANGELOG.read_text() if CHANGELOG.exists() else ""
    entry = f"- Feature `{key}` {'APPROVED' if approved else 'REJECTED'} " \
            f"(net_roi_delta={dec.get('net_roi_30d_delta','?')}%, " \
            f"max_dd_delta={dec.get('max_drawdown_delta','?')}%)\n"
    CHANGELOG.write_text(prev + "\n" + entry)

def apply_decision(key, decision_path):
    dec = json.loads(pathlib.Path(decision_path).read_text(encoding="utf-8"))
    if dec.get("approved"):
        set_flag(key, True)
        bump_version("minor")
        log_change(key, dec, True)
    else:
        log_change(key, dec, False)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    s1 = sub.add_parser("set-flag"); s1.add_argument("--feature"); s1.add_argument("--enabled")
    s2 = sub.add_parser("apply-decision"); s2.add_argument("--feature"); s2.add_argument("--decision")
    args = ap.parse_args()
    if args.cmd == "set-flag":
        enabled = str(args.enabled).lower() in ("1","true","yes","y")
        sys.exit(set_flag(args.feature, enabled))
    elif args.cmd == "apply-decision":
        sys.exit(apply_decision(args.feature, args.decision) or 0)
    else:
        ap.print_help()
