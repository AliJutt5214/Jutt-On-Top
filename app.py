import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components

# Page Configuration - Pro Exchange Layout
st.set_page_config(
    page_title="JUTT ON TOP | Live Exchange Terminal",
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

col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div>
        <h2 style="margin:0; color: #f0b90b;">⚡ JUTT ON TOP — Live Exchange Terminal</h2>
        <span style="color: #848e9c; font-size: 13px;">Real-Time Japanese Candlesticks | RSI & EMA Signal Engine</span>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    components.html(clock_html, height=55)

symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "PEPEUSDT", "SHIBUSDT", "XRPUSDT"]
tf_map = {
    "1m": "1",
    "3m": "3",
    "5m": "5",
    "15m": "15",
    "30m": "30",
    "1h": "60",
    "4h": "240",
    "1d": "D"
}

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 1])
with col_ctrl1:
    selected_symbol = st.selectbox("🪙 Select Coin Pair", symbols, index=4)
with col_ctrl2:
    selected_tf_label = st.selectbox("⏱️ Select Timeframe Schedule", list(tf_map.keys()), index=3)
with col_ctrl3:
    st.write("")
    st.write("")
    refresh_btn = st.button("🔄 Refresh Data", use_container_width=True)

bybit_tf = tf_map[selected_tf_label]

@st.cache_data(ttl=15)
def get_bybit_klines(symbol, interval, limit=120):
    url = "https://api.bybit.com/v5/market/kline"
    params = {
        'category': 'spot',
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }
    try:
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data.get('retCode') == 0 and 'list' in data.get('result', {}):
                raw_list = data['result']['list']
                raw_list.reverse() # Oldest to newest
                df = pd.DataFrame(raw_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
                df['timestamp'] = pd.to_datetime(df['timestamp'].astype(float), unit='ms')
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = df[col].astype(float)
                return df
    except Exception:
        pass
    return None

df = get_bybit_klines(selected_symbol, bybit_tf, limit=120)

if df is not None and len(df) > 20:
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['EMA_10'] = df['close'].ewm(span=10, adjust=False).mean()
    df['EMA_20'] = df['close'].ewm(span=20, adjust=False).mean()

    curr_close = df['close'].iloc[-1]
    prev_close = df['close'].iloc[-2]
    pct_change = ((curr_close - prev_close) / prev_close) * 100
    curr_rsi = df['RSI'].iloc[-1] if not np.isnan(df['RSI'].iloc[-1]) else 50
    curr_ema10 = df['EMA_10'].iloc[-1]
    curr_ema20 = df['EMA_20'].iloc[-1]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Pair", selected_symbol)
    with m2:
        price_str = f"${curr_close:,.8f}" if curr_close < 0.001 else (f"${curr_close:,.6f}" if curr_close < 1 else f"${curr_close:,.2f}")
        st.metric("Live Candle Close", price_str, f"{pct_change:+.2f}%")
    with m3:
        st.metric("RSI (14)", f"{curr_rsi:.2f}")
    with m4:
        trend_label = "BULLISH 🟢" if curr_ema10 > curr_ema20 else "BEARISH 🔴"
        st.metric("EMA Trend", trend_label)

    if curr_rsi < 38 and curr_ema10 >= curr_ema20:
        sig_text = f"🚀 STRONG BUY SIGNAL ({selected_tf_label.upper()} TIMEFRAME) — PRICE LIKELY TO PUMP UP!"
        sig_class = "signal-buy"
        reason = f"RSI is oversold ({curr_rsi:.1f}) and short EMA is above long EMA."
    elif curr_rsi > 62 and curr_ema10 <= curr_ema20:
        sig_text = f"⚠️ STRONG SELL SIGNAL ({selected_tf_label.upper()} TIMEFRAME) — PRICE LIKELY TO DUMP DOWN!"
        sig_class = "signal-sell"
        reason = f"RSI is overbought ({curr_rsi:.1f}) with bearish EMA rejection."
    else:
        sig_text = f"⏸️ HOLD / RANGE MARKET ({selected_tf_label.upper()} TIMEFRAME)"
        sig_class = "signal-hold"
        reason = f"Balanced momentum (RSI: {curr_rsi:.1f}). Awaiting breakout confirmation."

    st.markdown(f'<div class="{sig_class}">{sig_text}</div>', unsafe_allow_html=True)
    st.info(f"📊 **Bot Analysis Note:** {reason}")

    fig = go.Figure()

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

    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['EMA_10'],
        mode='lines',
        name='EMA 10',
        line=dict(color='#f0b90b', width=1.5)
    ))

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
    st.error("Market candle data load nahi ho pa raha. Kripya coin change kar ke dobara try karein.")
