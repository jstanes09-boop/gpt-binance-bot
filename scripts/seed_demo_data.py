import argparse, numpy as np, pandas as pd
from pathlib import Path
from datetime import timedelta, datetime, timezone

ap = argparse.ArgumentParser()
ap.add_argument("--symbols", default="BTCUSDT,ETHUSDT")
ap.add_argument("--days", type=int, default=90)
args = ap.parse_args()

Path("data").mkdir(exist_ok=True)
for sym in [s.strip() for s in args.symbols.split(",") if s.strip()]:
    n = args.days * 24
    rng = np.random.default_rng(abs(hash(sym)) % (2**32))
    ts = pd.date_range(end=pd.Timestamp.utcnow(), periods=n, freq="H")
    ret = rng.normal(0, 0.0012, n)
    close = 100 * np.exp(np.cumsum(ret))
    high = close * (1 + rng.normal(0.0006, 0.0008, n).clip(min=0))
    low  = close * (1 - rng.normal(0.0006, 0.0008, n).clip(min=0))
    openp = close / (1 + rng.normal(0, 0.0004, n))
    vol = rng.integers(100, 10000, n)
    df = pd.DataFrame({"timestamp": ts, "open": openp, "high": high, "low": low, "close": close, "volume": vol})
    out = Path(f"data/{sym}_1h.csv"); df.to_csv(out, index=False)
    print("[seed] wrote", out)
