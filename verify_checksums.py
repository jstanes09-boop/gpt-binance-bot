import hashlib, sys, json, pathlib
def sha256(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

if __name__ == "__main__":
    manifest = json.loads(pathlib.Path("checksums.json").read_text())
    bad = []
    for path, expected in manifest.items():
        path = pathlib.Path(path)
        if not path.exists():
            bad.append((str(path), "MISSING"))
            continue
        actual = sha256(path)
        if actual != expected:
            bad.append((str(path), f"MISMATCH actual={actual[:10]} expected={expected[:10]}"))
    if bad:
        print("[verify] FAIL:")
        for p,m in bad: print(" -", p, ":", m)
        sys.exit(1)
    print("[verify] OK")
