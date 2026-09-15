import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration - Pro Exchange Layout
st.set_page_config(
    page_title="JUTT ON TOP | Pro Exchange Terminal",
    page_icon="⚡",
    layout="wide"
)

# Custom Dark Exchange Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e11;
        color: #eaecef;
    }
    .top-header {
        background: #1e2329;
        padding: 12px 18px;
        border-radius: 8px;
        border: 1px solid #2b313a;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .signal-buy {
        background: linear-gradient(135deg, #0ecb81 0%, #064e3b 100%);
        color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(14, 203, 129, 0.25);
    }
    .signal-sell {
        background: linear-gradient(135deg, #f6465d 0%, #7f1d1d 100%);
        color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(246, 70, 93, 0.25);
    }
    .signal-hold {
        background: linear-gradient(135deg, #f0b90b 0%, #78350f 100%);
        color: #ffffff;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 15px rgba(240, 185, 11, 0.25);
    }
</style>
""", unsafe_allow_html=True)

# Header Bar
now = datetime.now()
st.markdown(f"""
<div class="top-header">
    <div>
        <h2 style="margin:0; color: #f0b90b;">⚡ JUTT ON TOP — Live Exchange Terminal</h2>
        <span style="color: #848e9c; font-size: 13px;">Real-Time Japanese Candlesticks | RSI & EMA Signal Engine</span>
    </div>
    <div style="text-align: right; color: #eaecef; font-size: 13px;">
        📅 <b>{now.strftime('%A, %b %d, %Y')}</b><br>
        ⏰ <b>{now.strftime('%I:%M:%S %p')}</b>
    </div>
</div>
""", unsafe_allow_html=True)

# Fetch USDT Symbols from Binance Vision API
@st.cache_data(ttl=3600)
def get_binance_symbols():
    try:
        url = "https://data.api.binance.vision/api/v3/exchangeInfo"
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            data = res.json()
            symbols = [s['symbol'] for s in data['symbols'] if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING']
            return sorted(symbols)
    except Exception:
        pass
    return ["BTCUSDT", "ETHUSDT", "DOGEUSDT", "PEPEUSDT", "SHIBUSDT", "SOLUSDT", "XRPUSDT"]

symbols = get_binance_symbols()
default_idx = symbols.index("DOGEUSDT") if "DOGEUSDT" in symbols else 0

# Selector Controls
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 1])
with col_ctrl1:
    selected_symbol = st.selectbox("🪙 Select Coin Pair (A-Z / Meme)", symbols, index=default_idx)
with col_ctrl2:
    selected_tf = st.selectbox("⏱️ Select Timeframe Schedule", ["1m", "3m", "5m", "15m", "30m", "1h", "4h", "1d"], index=3)
with col_ctrl3:
    st.write("")
    st.write("")
    refresh_btn = st.button("🔄 Refresh Data", use_container_width=True)

# Fetch OHLC Candlestick Data
@st.cache_data(ttl=30)
def get_klines_data(symbol, interval, limit=120):
    url = f"https://data.api.binance.vision/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        res = requests.get(url, timeout=8)
        if res.status_code == 200:
            raw = res.json()
            df = pd.DataFrame(raw, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_vol', 'trades', 'tb_base_vol', 'tb_quote_vol', 'ignore'
            ])
            df['timestamp'] = pd.to_datetime(df['open_time'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            return df
    except Exception:
        return None
    return None

df = get_klines_data(selected_symbol, selected_tf, limit=120)

if df is not None and len(df) > 20:
    # Calculate RSI (14)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Calculate EMA 10 & EMA 20
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

    curr_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]
    pct_change = ((curr_close - prev_close) / prev_close) * 100
    curr_rsi = df['RSI'].iloc[-1]
    curr_ema10 = df['EMA_10'].iloc[-1]
    curr_ema20 = df['EMA_20'].iloc[-1]

    # Quick Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Pair", selected_symbol)
    with m2:
        st.metric("Live Candle Close", f"${curr_close:,.6f}" if curr_close < 1 else f"${curr_close:,.2f}", f"{pct_change:+.2f}%")
    with m3:
        st.metric("RSI (14)", f"{curr_rsi:.2f}")
    with m4:
        trend_label = "BULLISH 🟢" if curr_ema10 > curr_ema20 else "BEARISH 🔴"
        st.metric("EMA Trend", trend_label)

    # Signal Generation Logic for Selected Timeframe
    if curr_rsi < 36 and curr_ema10 >= curr_ema20:
        sig_text = f"🚀 STRONG BUY SIGNAL ({selected_tf.upper()} TIMEFRAME) — PRICE LIKELY TO PUMP UP!"
        sig_class = "signal-buy"
        reason = f"RSI is oversold ({curr_rsi:.1f}) and short EMA is above long EMA on {selected_tf} chart."
    elif curr_rsi > 64 and curr_ema10 <= curr_ema20:
        sig_text = f"⚠️ STRONG SELL SIGNAL ({selected_tf.upper()} TIMEFRAME) — PRICE LIKELY TO DUMP DOWN!"
        sig_class = "signal-sell"
        reason = f"RSI is overbought ({curr_rsi:.1f}) with bearish EMA rejection on {selected_tf} chart."
    else:
        sig_text = f"⏸️ HOLD / RANGE MARKET ({selected_tf.upper()} TIMEFRAME)"
        sig_class = "signal-hold"
        reason = f"Balanced momentum (RSI: {curr_rsi:.1f}). Awaiting breakout confirmation on {selected_tf}."

    st.markdown(f'<div class="{sig_class}">{sig_text}</div>', unsafe_allow_html=True)
    st.info(f"📊 **Bot Analysis Note:** {reason}")

    # Plotly Japanese Candlestick Chart with EMAs
    fig = go.Figure()

    # Candlestick Trace
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='OHLC Candles',
        increasing_line_color='#0ecb81',
        decreasing_line_color='#f6465d'
    ))

    # EMA 15 Line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['EMA_10'],
        mode='lines',
        name='EMA 10',
        line=dict(color='#f0b90b', width=1.5)
    ))

    # EMA 20 Line
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['EMA_20'],
        mode='lines',
        name='EMA 20',
        line=dict(color='#3575ef', width=1.5)
    ))

    fig.update_layout(
        template='plotly_dark',
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='#0b0e11',
        plot_bgcolor='#0b0e11'
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Market candle data load nahi ho pa raha. Kripya coin ya timeframe change kar ke dobara try karein.")
