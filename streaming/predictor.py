import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

class StockPredictor:
    def __init__(self, window=20):
        self.window = window
        self.model = LinearRegression()

    def predict(self, df):
        if len(df) < self.window:
            return None
        df = df.tail(self.window)
        X = np.arange(len(df)).reshape(-1, 1)
        y = df['price'].values
        self.model.fit(X, y)
        next_x = np.array([[len(df)]])
        prediction = self.model.predict(next_x)[0]
        return prediction

class OptionsPredictor:
    def __init__(self):
        pass

    def predict_iv_change(self, df):
        if len(df) < 10:
            return None
        returns = df['price'].pct_change().dropna()
        volatility = np.std(returns)
        return volatility * 100  # pseudo implied volatility change %
