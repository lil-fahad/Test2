import websockets
import asyncio
import json
from datetime import datetime
from live_data.data_buffer import DataBuffer

class PolygonStream:
    def __init__(self, api_key, symbols):
        self.uri = "wss://socket.polygon.io/stocks"
        self.api_key = api_key
        self.symbols = symbols
        self.buffer = DataBuffer(capacity=1000)

    async def connect(self):
        async with websockets.connect(self.uri) as ws:
            await ws.send(json.dumps({
                "action": "auth",
                "params": self.api_key
            }))
            await ws.send(json.dumps({
                "action": "subscribe",
                "params": ",".join([f"A.{s}" for s in self.symbols])
            }))
            await self.handle_messages(ws)

    async def handle_messages(self, ws):
        async for message in ws:
            data = json.loads(message)
            for event in data:
                await self.process_event(event)

    async def process_event(self, event):
        if event.get("ev") == "A":
            tick_data = {
                "symbol": event["sym"],
                "price": event["p"],
                "size": event["s"],
                "timestamp": datetime.fromtimestamp(event["t"] / 1000),
                "exchange": event["x"]
            }
            self.buffer.add(tick_data)
