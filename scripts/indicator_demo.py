import numpy as np, pandas as pd
from bot.core import indicators as I

n = 200
rng = np.random.default_rng(0)
prices = 100 + np.cumsum(rng.normal(0, 1, n))
high = prices + rng.normal(0.2, 0.3, n).clip(min=0)
low  = prices - rng.normal(0.2, 0.3, n).clip(min=0)
close = pd.Series(prices, name="close")
high  = pd.Series(high, name="high")
low   = pd.Series(low, name="low")

print("[demo] tail:")
print(pd.DataFrame({
  "ema12": I.ema(close, 12).tail(),
  "ema26": I.ema(close, 26).tail(),
  "rsi14": I.rsi(close, 14).tail(),
  "atr14": I.atr(high, low, close, 14).tail()
}))
m, s, h = I.macd(close)
print("\n[demo] macd last:", float(m.iloc[-1]), "signal:", float(s.iloc[-1]), "hist:", float(h.iloc[-1]))
