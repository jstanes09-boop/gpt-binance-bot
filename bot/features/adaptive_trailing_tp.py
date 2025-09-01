def adjust_take_profit(price: float, atr: float = 0.0, k: float = 2.0) -> float:
    """
    Placeholder: trailing TP = price - k * ATR (not below 0).
    """
    return max(0.0, price - k * atr)
