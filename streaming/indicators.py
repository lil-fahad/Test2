import pandas as pd
import numpy as np
import talib

class StreamingTA:
    def __init__(self, window=50):
        self.window = window
        
    def calculate_all(self, df):
        if len(df) < self.window:
            return None
        closes = df["price"].values
        volumes = df["size"].values
        return {
            "sma_20": talib.SMA(closes, timeperiod=20)[-1],
            "ema_50": talib.EMA(closes, timeperiod=50)[-1],
            "rsi": talib.RSI(closes, timeperiod=14)[-1],
            "macd": talib.MACD(closes)[0][-1],
            "obv": talib.OBV(closes, volumes)[-1],
            "atr": talib.ATR(df["high"].values, df["low"].values, closes, timeperiod=14)[-1]
        }
