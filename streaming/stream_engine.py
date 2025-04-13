import asyncio
import streamlit as st
from live_data.market_connectors.polygon_ws import PolygonStream
from streaming.indicators import StreamingTA
from streaming.predictor import StockPredictor, OptionsPredictor
from live_data.data_buffer import DataBuffer

class StreamEngine:
    def __init__(self, symbols, data_source='polygon', api_key=None):
        self.symbols = symbols
        self.data_source = data_source
        self.api_key = api_key or st.secrets["POLYGON_API_KEY"]
        self.ta = StreamingTA()
        self.buffers = {s: DataBuffer() for s in symbols}
        self.running = False
        self.stock_predictor = StockPredictor()
        self.options_predictor = OptionsPredictor()

    async def start(self):
        self.running = True
        if self.data_source == 'polygon':
            connector = PolygonStream(
                api_key=self.api_key,
                symbols=self.symbols
            )
            await connector.connect()

    def stop(self):
        self.running = False

    def process_tick(self, tick):
        symbol = tick["symbol"]
        self.buffers[symbol].add(tick)
        df = self.buffers[symbol].snapshot()
        indicators = self.ta.calculate_all(df)
        stock_pred = self.stock_predictor.predict(df)
        iv_pred = self.options_predictor.predict_iv_change(df)
        return {"indicators": indicators, "stock_pred": stock_pred, "iv_pred": iv_pred}
