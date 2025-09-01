import time
from bot.core.settings import Config, diagnostics

def run():
    cfg = Config()
    print(diagnostics(cfg))
    print("\n[bot] Bot is running! (dry_run=" + str(cfg.dry_run) + ")")
    # heartbeat loop (press Ctrl+C to stop)
    for i in range(3):
        print(f"[bot] heartbeat {i+1}/3")
        time.sleep(1)

if __name__ == "__main__":
    run()
