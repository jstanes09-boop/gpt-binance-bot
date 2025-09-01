import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

@dataclass
class Config:
    binance_key: str = os.getenv("BINANCE_API_KEY", "")
    binance_secret: str = os.getenv("BINANCE_API_SECRET", "")
    telegram_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_chat: str = os.getenv("TELEGRAM_PUSH_CHAT_ID", "")
    dry_run: bool = os.getenv("DRY_RUN", "true").lower() in ("1","true","yes")
    fee_rate: float = float(os.getenv("FEE_RATE", "0.001"))
    base_ccy: str = os.getenv("BASE_CURRENCY", "USDT")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

def diagnostics(cfg: Config) -> str:
    def yn(x): return "YES" if x else "NO"
    lines = [
        "=== GBT Diagnostics ===",
        f"Working dir: {os.getcwd()}",
        f".env exists: {yn(os.path.exists('.env'))}",
        "",
        "ENV PRESENCE",
        f"BINANCE_API_KEY present? {yn(bool(cfg.binance_key))}",
        f"BINANCE_API_SECRET present? {yn(bool(cfg.binance_secret))}",
        f"TELEGRAM_BOT_TOKEN present? {yn(bool(cfg.telegram_token))}",
        f"TELEGRAM_PUSH_CHAT_ID present? {yn(bool(cfg.telegram_chat))}",
        f"DRY_RUN: {cfg.dry_run}",
        f"FEE_RATE: {cfg.fee_rate}",
        f"BASE_CURRENCY: {cfg.base_ccy}",
        f"LOG_LEVEL: {cfg.log_level}",
    ]
    return "\n".join(lines)
