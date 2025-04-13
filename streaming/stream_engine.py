import asyncio
import streamlit as st
from live_data.market_connectors.polygon_ws import PolygonStream
from streaming.indicators import StreamingTA
from live_data.data_buffer import DataBuffer

class StreamEngine:
    def __init__(self, symbols, data_source='polygon', api_key=None):
        self.symbols = symbols
        self.data_source = data_source
        self.api_key = api_key or st.secrets["POLYGON_API_KEY"]
        self.ta = StreamingTA()
        self.buffers = {s: DataBuffer() for s in symbols}

    async def start(self):
        if self.data_source == 'polygon':
            connector = PolygonStream(
                api_key=self.api_key,
                symbols=self.symbols
            )
            await connector.connect()

    def process_tick(self, tick):
        symbol = tick["symbol"]
        self.buffers[symbol].add(tick)
        df = self.buffers[symbol].snapshot()
        return self.ta.calculate_all(df)
