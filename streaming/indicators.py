import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.volatility import AverageTrueRange

class StreamingTA:
    def __init__(self, window=50):
        self.window = window

    def calculate_all(self, df):
        if len(df) < self.window:
            return None

        df = df.copy()

        df['sma_20'] = SMAIndicator(close=df['price'], window=20).sma_indicator()
        df['ema_50'] = EMAIndicator(close=df['price'], window=50).ema_indicator()
        df['rsi'] = RSIIndicator(close=df['price'], window=14).rsi()
        macd = MACD(close=df['price'])
        df['macd'] = macd.macd()
        df['obv'] = OnBalanceVolumeIndicator(close=df['price'], volume=df['size']).on_balance_volume()
        df['atr'] = AverageTrueRange(
            high=df.get('high', df['price']),
            low=df.get('low', df['price']),
            close=df['price'],
            window=14
        ).average_true_range()

        return df.iloc[-1][['sma_20', 'ema_50', 'rsi', 'macd', 'obv', 'atr']].to_dict()
