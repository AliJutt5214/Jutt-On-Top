import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Jutt On Top - Live Signal Bot",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .metric-card {
        background-color: #1f2937;
        padding: 15px;
        border-radius: 10px;
        border: 1px: solid #374151;
        text-align: center;
    }
    .buy-signal {
        background-color: #064e3b;
        color: #34d399;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border: 2px solid #10b981;
    }
    .sell-signal {
        background-color: #7f1d1d;
        color: #f87171;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border: 2px solid #ef4444;
    }
    .neutral-signal {
        background-color: #313338;
        color: #fbbf24;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border: 2px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# Header Section with Live Date & Time
now = datetime.now()
current_date_str = now.strftime("%A, %B %d, %Y")
current_time_str = now.strftime("%I:%M:%S %p")

st.title("⚡ JUTT ON TOP - Real-Time Crypto Signal Bot")
col_d1, col_d2 = st.columns(2)
with col_d1:
    st.info(f"📅 **Date:** {current_date_str}")
with col_d2:
    st.info(f"⏰ **Current Time (Live):** {current_time_str}")

# Function to get all USDT trading pairs from Binance Vision API
@st.cache_data(ttl=3600)
def get_binance_symbols():
    try:
        url = "https://data.api.binance.vision/api/v3/exchangeInfo"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            symbols = [s['symbol'] for s in data['symbols'] if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING']
            return sorted(symbols)
    except Exception as e:
        pass
    # Fallback default list if API fails
    return ["BTCUSDT", "ETHUSDT", "DOGEUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "PEPEUSDT"]

# Function to fetch live candle (klines) data
def get_klines(symbol, interval='15m', limit=100):
    url = f"https://data.api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw = response.json()
            df = pd.DataFrame(raw, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
            ])
            df['close'] = df['close'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['open'] = df['open'].astype(float)
            df['volume'] = df['volume'].astype(float)
            return df
    except Exception as e:
        return None
    return None

# Function to calculate RSI
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Sidebar Controls
st.sidebar.header("⚙️ Bot Settings")
all_symbols = get_binance_symbols()
default_idx = all_symbols.index("DOGEUSDT") if "DOGEUSDT" in all_symbols else 0

selected_symbol = st.sidebar.selectbox("Select Coin Symbol (USDT)", all_symbols, index=default_idx)
timeframe = st.sidebar.selectbox("Select Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"], index=2)
refresh_btn = st.sidebar.button("🔄 Refresh Signal Now")

# Main Logic & Fetching
with st.spinner(f"Analyzing live market data for {selected_symbol}..."):
    df = get_klines(selected_symbol, interval=timeframe, limit=50)

if df is not None and len(df) > 0:
    df['RSI'] = calculate_rsi(df['close'], period=14)
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

    current_price = df['close'].iloc[-1]
    prev_price = df['close'].iloc[-2]
    price_change_pct = ((current_price - prev_price) / prev_price) * 100
    current_rsi = df['RSI'].iloc[-1]
    ema_10 = df['EMA_10'].iloc[-1]
    ema_20 = df['EMA_20'].iloc[-1]

    # Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric(label="Coin Pair", value=selected_symbol)
    with c2:
        st.metric(label="Live Price (USDT)", value=f"${current_price:,.4f}", delta=f"{price_change_pct:.2f}%")
    with c3:
        st.metric(label="RSI (14)", value=f"{current_rsi:.2f}")
    with c4:
        trend_status = "BULLISH 🟢" if ema_10 > ema_20 else "BEARISH 🔴"
        st.metric(label="Trend Status", value=trend_status)

    # Signal Generation Logic
    if current_rsi < 35 and ema_10 > ema_20:
        signal_type = "STRONG BUY SIGNAL 🚀"
        signal_class = "buy-signal"
        reason = "RSI is oversold (< 35) and short-term EMA is above long-term EMA."
    elif current_rsi > 65 and ema_10 < ema_20:
        signal_type = "STRONG SELL SIGNAL ⚠️"
        signal_class = "sell-signal"
        reason = "RSI is overbought (> 65) and short-term EMA is below long-term EMA."
    else:
        signal_type = "HOLD / NEUTRAL ⏸️"
        signal_class = "neutral-signal"
        reason = "Market is consolidating. Wait for a clear breakout confirmation."

    st.markdown("### 📡 Live Signal Analysis (Now This Time)")
    st.markdown(f'<div class="{signal_class}">{signal_type}</div>', unsafe_allow_html=True)
    st.markdown(f"**Analysis Reason:** {reason} | **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Chart Section
    st.markdown("### 📈 Live Price & Trend Chart")
    chart_data = df[['close', 'EMA_10', 'EMA_20']].tail(40)
    st.line_chart(chart_data)

else:
    st.error("Could not fetch data from Binance. Please check your internet connection or try again.")
