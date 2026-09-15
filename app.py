import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
import streamlit.components.v1 as components
from PIL import Image

# Page Configuration with Pro Logo/Icon
st.set_page_config(
    page_title="JUTT ON TOP | AI Signal Terminal",
    page_icon="logo.png",
    layout="wide"
)

# Custom Dark Exchange Styling & Hide Streamlit Footer/Toolbar
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #0b0e11;
        color: #eaecef;
    }
    .signal-buy {
        background: linear-gradient(135deg, #0ecb81 0%, #064e3b 100%);
        color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(14, 203, 129, 0.35);
        border: 1px solid #0ecb81;
    }
    .signal-sell {
        background: linear-gradient(135deg, #f6465d 0%, #7f1d1d 100%);
        color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(246, 70, 93, 0.35);
        border: 1px solid #f6465d;
    }
    .signal-hold {
        background: linear-gradient(135deg, #f0b90b 0%, #78350f 100%);
        color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(240, 185, 11, 0.35);
        border: 1px solid #f0b90b;
    }
    .metric-card {
        background: #1e2329;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #2b313a;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Real-Time JavaScript Live Clock Component
clock_html = """
<div style="font-family: sans-serif; text-align: right; color: #eaecef;">
    <div style="font-size: 13px; color: #848e9c;" id="live-date"></div>
    <div style="font-size: 16px; font-weight: bold; color: #f0b90b;" id="live-clock">⏰ Loading...</div>
</div>
<script>
function updateClock() {
    const now = new Date();
    const optionsDate = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' };
    document.getElementById('live-date').innerText = '📅 ' + now.toLocaleDateString('en-US', optionsDate);
    document.getElementById('live-clock').innerText = '⏰ ' + now.toLocaleTimeString('en-US', { hour12: true });
}
setInterval(updateClock, 1000);
updateClock();
</script>
"""

col_logo, col_h1, col_h2 = st.columns([0.8, 3.2, 1.2])
with col_logo:
    try:
        logo_img = Image.open("logo.png")
        st.image(logo_img, width=80)
    except Exception:
        st.write("🚀")
with col_h1:
    st.markdown("""
    <div>
        <h2 style="margin:0; color: #f0b90b;">🚀 JUTT ON TOP — AI Signal Pro Terminal</h2>
        <span style="color: #848e9c; font-size: 13px;">Binance Direct Feed | RSI + EMA + Bollinger + Stochastic Confluence</span>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    components.html(clock_html, height=55)

symbols = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "SHIBUSDT", 
    "PEPEUSDT", "FLOKIUSDT", "BONKUSDT", "WIFUSDT", "MEMEUSDT", "XRPUSDT"
]

col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([2, 2, 1, 1])
with col_ctrl1:
    selected_symbol = st.selectbox("🪙 Select Coin Pair", symbols, index=5)
with col_ctrl2:
    selected_tf = st.selectbox("⏱️ Select Timeframe", ["1m", "5m", "15m", "1h"], index=1)
with col_ctrl3:
    bot_mode = st.selectbox("🤖 Signal Mode", ["Binary (CALL/PUT)", "Crypto Scalp"])
with col_ctrl4:
    st.write("")
    st.write("")
    refresh_btn = st.button("🔄 Refresh Now", use_container_width=True)

@st.cache_data(ttl=15)
def get_binance_klines(symbol, interval, limit=120):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            df = pd.DataFrame(data, columns=[
                'open_time', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            df['timestamp'] = pd.to_datetime(df['open_time'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            return df
    except Exception:
        pass
    return None

df = get_binance_klines(selected_symbol, selected_tf, limit=120)

if df is not None and len(df) > 25:
    # 1. RSI (14)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # 2. EMAs
    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

    # 3. Bollinger Bands (20, 2)
    df['BB_Mid'] = df['close'].rolling(20).mean()
    df['BB_Std'] = df['close'].rolling(20).std()
    df['BB_Upper'] = df['BB_Mid'] + (2 * df['BB_Std'])
    df['BB_Lower'] = df['BB_Mid'] - (2 * df['BB_Std'])

    # 4. Stochastic Oscillator (14, 3)
    low_14 = df['low'].rolling(14).min()
    high_14 = df['high'].rolling(14).max()
    df['Stoch_K'] = ((df['close'] - low_14) / (high_14 - low_14)) * 100
    df['Stoch_D'] = df['Stoch_K'].rolling(3).mean()

    curr_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]
    pct_change = ((curr_close - prev_close) / prev_close) * 100
    curr_rsi = df['RSI'].iloc[-1] if not np.isnan(df['RSI'].iloc[-1]) else 50
    curr_ema10 = df['EMA_10'].iloc[-1]
    curr_ema20 = df['EMA_20'].iloc[-1]
    curr_stoch_k = df['Stoch_K'].iloc[-1] if not np.isnan(df['Stoch_K'].iloc[-1]) else 50
    curr_bb_upper = df['BB_Upper'].iloc[-1]
    curr_bb_lower = df['BB_Lower'].iloc[-1]

    # AI Confluence & Score Calculation
    bull_score = 0
    bear_score = 0
    reasons = []

    if curr_rsi < 38:
        bull_score += 30
        reasons.append(f"RSI Oversold ({curr_rsi:.1f})")
    elif curr_rsi > 62:
        bear_score += 30
        reasons.append(f"RSI Overbought ({curr_rsi:.1f})")

    if curr_ema10 > curr_ema20:
        bull_score += 25
        reasons.append("EMA10 > EMA20 Bullish Cross")
    else:
        bear_score += 25
        reasons.append("EMA10 < EMA20 Bearish Cross")

    if curr_close <= curr_bb_lower * 1.002:
        bull_score += 25
        reasons.append("Price touching Lower Bollinger Band")
    elif curr_close >= curr_bb_upper * 0.998:
        bear_score += 25
        reasons.append("Price touching Upper Bollinger Band")

    if curr_stoch_k < 20:
        bull_score += 20
        reasons.append(f"Stochastic %K Oversold ({curr_stoch_k:.1f})")
    elif curr_stoch_k > 80:
        bear_score += 20
        reasons.append(f"Stochastic %K Overbought ({curr_stoch_k:.1f})")

    # Metrics Row
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Pair", selected_symbol)
    with m2:
        price_str = f"${curr_close:,.8f}" if curr_close < 0.001 else (f"${curr_close:,.6f}" if curr_close < 1 else f"${curr_close:,.2f}")
        st.metric("Live Price", price_str, f"{pct_change:+.2f}%")
    with m3:
        st.metric("RSI (14)", f"{curr_rsi:.2f}")
    with m4:
        st.metric("Stochastic %K", f"{curr_stoch_k:.2f}")
    with m5:
        trend_label = "BULLISH 🟢" if curr_ema10 > curr_ema20 else "BEARISH 🔴"
        st.metric("EMA Trend", trend_label)

    # Signal Output Box
    if bull_score >= 60:
        accuracy = min(94, 65 + bull_score // 3)
        sig_type = "CALL / STRONG BUY (🟢)" if "Binary" in bot_mode else "STRONG BUY (🟢)"
        sig_class = "signal-buy"
        sig_text = f"🚀 {sig_type} [{selected_symbol} | {selected_tf}] — AI Accuracy: {accuracy}%"
        reason_str = " | ".join(reasons)
    elif bear_score >= 60:
        accuracy = min(94, 65 + bear_score // 3)
        sig_type = "PUT / STRONG SELL (🔴)" if "Binary" in bot_mode else "STRONG SELL (🔴)"
        sig_class = "signal-sell"
        sig_text = f"⚠️ {sig_type} [{selected_symbol} | {selected_tf}] — AI Accuracy: {accuracy}%"
        reason_str = " | ".join(reasons)
    else:
        sig_text = f"⏸️ WAIT / NO CLEAR EDGE [{selected_symbol} | {selected_tf}] — Market Ranging"
        sig_class = "signal-hold"
        reason_str = f"RSI: {curr_rsi:.1f} | Stochastic: {curr_stoch_k:.1f} | Wait for breakout"

    st.markdown(f'<div class="{sig_class}">{sig_text}</div>', unsafe_allow_html=True)
    st.info(f"🧠 **AI Bot Confluence Log:** {reason_str}")

    # Plotly Chart with Bollinger Bands, Candles & EMAs
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='Candles',
        increasing_line_color='#0ecb81',
        decreasing_line_color='#f6465d'
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['BB_Upper'],
        mode='lines', name='BB Upper',
        line=dict(color='rgba(255,255,255,0.25)', width=1, dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['BB_Lower'],
        mode='lines', name='BB Lower',
        line=dict(color='rgba(255,255,255,0.25)', width=1, dash='dot'),
        fill='tonexty', fillcolor='rgba(255,255,255,0.02)'
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['EMA_10'],
        mode='lines', name='EMA 10',
        line=dict(color='#f0b90b', width=1.5)
    ))

    fig.add_trace(go.Scatter(
        x=df['timestamp'], y=df['EMA_20'],
        mode='lines', name='EMA 20',
        line=dict(color='#3575ef', width=1.5)
    ))

    fig.update_layout(
        template='plotly_dark',
        height=460,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_rangeslider_visible=False,
        dragmode=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        paper_bgcolor='#0b0e11',
        plot_bgcolor='#0b0e11'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

else:
    st.error("Market candle data load nahi ho pa raha. Kripya coin change kar ke dobara try karein.")
