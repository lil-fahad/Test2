import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streaming.stream_engine import StreamEngine
import asyncio

st.set_page_config(layout="wide")
st.title("Real-Time Market Dashboard")

if 'engine' not in st.session_state:
    st.session_state.engine = StreamEngine(
        symbols=["AAPL", "MSFT", "TSLA"],
        data_source='polygon',
        api_key=st.secrets["POLYGON_API_KEY"]
    )

async def run_stream():
    await st.session_state.engine.start()

if st.button("Start Real-Time Feed"):
    asyncio.run(run_stream())

placeholder = st.empty()

while st.session_state.engine.running:
    with placeholder.container():
        for symbol in st.session_state.engine.symbols:
            df = st.session_state.engine.buffers[symbol].snapshot()
            if len(df) > 0:
                fig = go.Figure(
                    go.Scatter(x=df["timestamp"], y=df["price"], mode='lines')
                )
                st.plotly_chart(fig, use_container_width=True)

                latest = df.iloc[-1]
                st.metric(label=f"{symbol} Price", value=f"${latest['price']:.2f}", delta=f"{latest['size']} shares")

                # Get predictions
                result = st.session_state.engine.process_tick(latest)
                if result["stock_pred"]:
                    st.metric(label=f"{symbol} Predicted Price", value=f"${result['stock_pred']:.2f}")
                if result["iv_pred"]:
                    st.metric(label=f"{symbol} IV Swing Forecast", value=f"{result['iv_pred']:.2f} %")
