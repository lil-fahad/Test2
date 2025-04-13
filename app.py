import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streaming.stream_engine import StreamEngine
import asyncio

st.set_page_config(layout="wide")
st.title("Real-Time Market Dashboard")

# --- Symbol search input ---
user_symbols = st.text_input(
    "Enter stock symbols (comma-separated)", 
    value="AAPL, MSFT, TSLA"
)
symbols = [s.strip().upper() for s in user_symbols.split(",") if s.strip()]

# --- Prediction type selector ---
prediction_type = st.selectbox(
    "Select prediction type",
    ["None", "Stock Forecast", "Options Forecast"]
)

# --- Stream trigger ---
if st.button("Start Real-Time Feed"):
    st.session_state.engine = StreamEngine(
        symbols=symbols,
        data_source='polygon',
        api_key=st.secrets["POLYGON_API_KEY"]
    )
    st.session_state.prediction_type = prediction_type
    asyncio.run(st.session_state.engine.start())

# --- Real-time output ---
placeholder = st.empty()

if 'engine' in st.session_state and st.session_state.engine.running:
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

                result = st.session_state.engine.process_tick(latest)

                if st.session_state.prediction_type == "Stock Forecast" and result["stock_pred"]:
                    st.metric(label=f"{symbol} Predicted Price", value=f"${result['stock_pred']:.2f}")

                if st.session_state.prediction_type == "Options Forecast" and result["iv_pred"]:
                    st.metric(label=f"{symbol} IV Forecast", value=f"{result['iv_pred']:.2f} %")
