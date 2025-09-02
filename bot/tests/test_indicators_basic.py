import numpy as np, pandas as pd
from bot.core import indicators as I

def test_shapes():
    n = 50
    c = pd.Series(np.arange(n, dtype=float))
    h = c + 1; l = c - 1
    assert len(I.ema(c, 12)) == n
    assert len(I.rsi(c, 14)) == n
    assert len(I.atr(h, l, c, 14)) == n
    m, s, hst = I.macd(c)
    assert len(m) == len(s) == len(hst) == n
