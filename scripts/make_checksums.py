import hashlib, json, os, pathlib

ROOT = pathlib.Path(".").resolve()
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "backups", "artifacts", "dist", "reports"}
EXCLUDE_FILES = {"checksums.json"}

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def should_skip(path: pathlib.Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS: return True
    if path.name in EXCLUDE_FILES: return True
    return False

def main():
    manifest = {}
    for root, dirs, files in os.walk(ROOT):
        # prune excluded dirs in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            p = pathlib.Path(root) / name
            rel = p.relative_to(ROOT).as_posix()
            if should_skip(p): 
                continue
            manifest[rel] = sha256_file(p)
    pathlib.Path("checksums.json").write_text(json.dumps(manifest, indent=2))
    print(f"[make_checksums] wrote checksums.json with {len(manifest)} files")

if __name__ == "__main__":
    main()
