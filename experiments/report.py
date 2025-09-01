import argparse, json, pathlib

ap = argparse.ArgumentParser()
ap.add_argument("--baseline")
ap.add_argument("--candidate")
ap.add_argument("--decision")
ap.add_argument("--html", required=True)
ap.add_argument("--latest", action="store_true")
args = ap.parse_args()

html = ["<html><body><h1>Bot Report</h1>"]
def add_json(title, p):
    if p and pathlib.Path(p).exists():
        html.append(f"<h2>{title}</h2><pre>{pathlib.Path(p).read_text()}</pre>")

add_json("Baseline", args.baseline)
add_json("Candidate", args.candidate)
add_json("Decision", args.decision)

pathlib.Path(args.html).write_text("\n".join(html)+ "</body></html>")
print("[report] wrote", args.html)
