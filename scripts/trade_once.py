import os, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
from bot.core.exchange_adapter import ExchangeAdapter
from bot.core.settings import Config

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--symbol", default="BTCUSDT")
ap.add_argument("--quote", type=float, default=float(os.getenv("MIN_QUOTE_PER_ORDER", "10")))
ap.add_argument("--side", default="BUY", choices=["BUY","SELL"])
args = ap.parse_args()

cfg = Config()
confirm = os.getenv("CONFIRM_LIVE", "NO").upper()
if not cfg.dry_run and os.getenv("BINANCE_TESTNET","true").lower() not in ("1","true","yes") and confirm != "YES":
    print("[trade_once] LIVE trading blocked. Set CONFIRM_LIVE=YES to proceed.")
    sys.exit(2)

ex = ExchangeAdapter(cfg)
res = ex.place_market(args.symbol, args.side, args.quote)
print("[trade_once]", res.to_dict())
