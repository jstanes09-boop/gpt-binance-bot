import pandas as pd
from indicators import ema, rsi, atr
class SignalEngine:
    def __init__(self, ema_fast, ema_slow, rsi_period, atr_period, min_atr_pct, max_atr_pct):
        self.ema_fast=ema_fast; self.ema_slow=ema_slow; self.rsi_period=rsi_period
        self.atr_period=atr_period; self.min_atr_pct=min_atr_pct; self.max_atr_pct=max_atr_pct
    def analyze(self, df: pd.DataFrame):
        df=df.copy()
        df["ema_fast"]=ema(df["close"], self.ema_fast)
        df["ema_slow"]=ema(df["close"], self.ema_slow)
        df["rsi"]=rsi(df["close"], self.rsi_period)
        df["atr"]=atr(df, self.atr_period)
        df["atr_pct"]= (df["atr"]/df["close"])*100.0
        last=df.iloc[-1]
        trending_up = last.ema_fast>last.ema_slow
        rsi_ok = 50<=last.rsi<=75
        atr_ok = self.min_atr_pct<=last.atr_pct<=self.max_atr_pct
        score = (40 if trending_up else 0)+(30 if rsi_ok else 0)+(30 if atr_ok else 0)
        return {"trend_up":bool(trending_up),"rsi":float(last.rsi),"atr":float(last.atr),
                "atr_pct":float(last.atr_pct),"score":int(score),"entry":float(last.close)}
