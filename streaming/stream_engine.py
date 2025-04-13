import asyncio
from live_data.market_connectors.polygon_ws import PolygonStream
from streaming.indicators import StreamingTA
from live_data.data_buffer import DataBuffer

class StreamEngine:
    def __init__(self, symbols, data_source='polygon'):
        self.symbols = symbols
        self.data_source = data_source
        self.ta = StreamingTA()
        self.buffers = {s: DataBuffer() for s in symbols}
        
    async def start(self):
        if self.data_source == 'polygon':
            connector = PolygonStream(
                api_key=st.secrets["POLYGON_API_KEY"],
                symbols=self.symbols
            )
            await connector.connect()
            
    def process_tick(self, tick):
        symbol = tick["symbol"]
        self.buffers[symbol].add(tick)
        df = self.buffers[symbol].snapshot()
        processed = self.ta.calculate_all(df)
        return processed
