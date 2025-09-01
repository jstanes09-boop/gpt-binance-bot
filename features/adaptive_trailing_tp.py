def adjust_take_profit(price: float, atr: float = 0.0, k: float = 2.0) -> float:
    """
    Placeholder: returns a trailing TP level = price - k * ATR (not below 0).
    Later we'll wire this into live exits and backtests.
    """
    return max(0.0, price - k * atr)
