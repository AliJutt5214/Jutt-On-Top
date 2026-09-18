import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import websocket
import json
import threading
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange

# ============================================================
# PAGE CONFIG & PROFESSIONAL LOGO SETUP
# ============================================================

LOGO_URL = "https://raw.githubusercontent.com/AliJutt5214/Jutt-On-Top/main/WhatsApp%20Image%202026-09-14%20at%209.03.23%20PM.jpeg"

st.set_page_config(
    page_title="JUTT BOT PRO TRADER",
    page_icon=LOGO_URL,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PROFESSIONAL CSS STYLING & HIDING STREAMLIT BADGES
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #07090e;
        color: #ffffff;
    }
    
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Completely hide Streamlit branding, footer badges, and floating menus */
    .stApp > footer { display: none !important; }
    #stDecoration { display: none !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    .viewerBadge_container__1QSob { display: none !important; }
    div[class*="viewerBadge"] { display: none !important; }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .header-container {
        display: flex;
        align-items: center;
        background: linear-gradient(135deg, #11151c 0%, #1a222d 100%);
        border: 2px solid #d4af37;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(212, 175, 55, 0.15);
    }
    
    .logo-img {
        width: 90px;
        height: 90px;
        border-radius: 15px;
        object-fit: cover;
        border: 2px solid #d4af37;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }

    .title-text {
        margin-left: 20px;
    }

    .main-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd700, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }

    .sub-title {
        color: #a0aec0;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    .card {
        background: #111622;
        border: 1px solid #232d3f;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    .signal-call {
        color: #00ecb0;
        font-size: 42px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 236, 176, 0.4);
    }

    .signal-put {
        color: #ff4d4d;
        font-size: 42px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 20px rgba(255, 77, 77, 0.4);
    }

    .signal-none {
        color: #ffcc00;
        font-size: 38px;
        font-weight: 900;
        text-align: center;
    }

    .reason-box {
        padding: 10px 0;
        border-bottom: 1px solid #1a2233;
        font-size: 15px;
        color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

PAIR_LIST = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", 
    "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT"
]

# ============================================================
# BINANCE SECURE LIVE WEBSOCKET ENGINE
# ============================================================

class BinanceProEngine:
    def __init__(self):
        self.connected = False
        self.ticks = []
        self.last_update = time.time()
        self.lock = threading.Lock()
        self.current_symbol = "SOLUSDT"

    def start_socket(self, symbol):
        self.current_symbol = symbol.lower()
        socket_url = f"wss://stream.binance.com:9443/ws/{self.current_symbol}@trade"

        def run():
            def on_message(ws, message):
                data = json.loads(message)
                item = {
                    "time": float(data['T']) / 1000.0,
                    "price": float(data['p'])
                }
                with self.lock:
                    self.ticks.append(item)
                    if len(self.ticks) > 1500:
                        self.ticks.pop(0)
                    self.last_update = time.time()
                    self.connected = True

            def on_open(ws):
                self.connected = True

            def on_close(ws, close_status_code, close_msg):
                self.connected = False

            ws = websocket.WebSocketApp(
                socket_url,
                on_open=on_open,
                on_message=on_message,
                on_close=lambda w, c, m: setattr(self, 'connected', False)
            )
            ws.run_forever()

        threading.Thread(target=run, daemon=True).start()

    def get_candles(self, symbol, interval="5m", limit=120):
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            candles = []
            for c in data:
                candles.append({
                    "time": float(c[0]) / 1000.0,
                    "open": float(c[1]),
                    "high": float(c[2]),
                    "low": float(c[3]),
                    "close": float(c[4]),
                    "volume": float(c[5])
                })
            return candles
        except Exception:
            return []

    def get_ticks(self, limit=100):
        with self.lock:
            return list(self.ticks)[-limit:]

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "engine" not in st.session_state:
    st.session_state.engine = BinanceProEngine()
    st.session_state.engine.start_socket("SOLUSDT")

engine = st.session_state.engine

# ============================================================
# HEADER WITH LOGO
# ============================================================

st.markdown(f"""
<div class="header-container">
    <img src="{LOGO_URL}" class="logo-img">
    <div class="title-text">
        <div class="main-title">JUTT BOT PRO TRADER</div>
        <div class="sub-title">AI-Powered Binance Futures & Scalping Analyzer</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONTROLS PANEL
# ============================================================

col1, col2, col3 = st.columns([1.5, 1, 1])

with col1:
    pair = st.selectbox("SELECT TRADING PAIR", PAIR_LIST, index=2)
    if pair.lower() != engine.current_symbol.upper():
        engine.start_socket(pair)

with col2:
    timeframe = st.selectbox("TIMEFRAME", ["1m", "3m", "5m", "15m", "30m", "1h"], index=2)

with col3:
    st.write("")
    generate = st.button("⚡ GENERATE PROFESSIONAL SIGNAL", use_container_width=True)

# ============================================================
# LIVE METRICS BAR
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    if engine.connected:
        st.success("🟢 100% SECURE & LIVE")
    else:
        st.warning("🔄 CONNECTING TO BINANCE...")

with m2:
    ticks = engine.get_ticks(10)
    live_price = ticks[-1]['price'] if ticks else 0.0
    st.metric("REAL-TIME PRICE", f"${live_price:,.2f}" if live_price > 0 else "Waiting...")

with m3:
    candles = engine.get_candles(pair, timeframe, 50)
    df_m = pd.DataFrame(candles)
    rsi_val = RSIIndicator(close=df_m["close"], window=14).rsi().iloc[-1] if not df_m.empty else 0
    st.metric("RSI (14)", f"{rsi_val:.2f}" if rsi_val > 0 else "--")

with m4:
    st.metric("LIVE TICKS STREAM", len(engine.get_ticks(300)))

# ============================================================
# PROFESSIONAL LIVE CANDLESTICK CHART
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(f"📊 Live Market Feed & Candlestick Analysis — {pair}")

if candles:
    df_chart = pd.DataFrame(candles)
    fig = go.Figure(data=[go.Candlestick(
        x=pd.to_datetime(df_chart['time'], unit='s'),
        open=df_chart['open'],
        high=df_chart['high'],
        low=df_chart['low'],
        close=df_chart['close'],
        name=pair,
        increasing_line_color='#00ecb0',
        decreasing_line_color='#ff4d4d'
    )])
    
    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor='#111622',
        plot_bgcolor='#111622',
        font=dict(color='#ffffff', family='Poppins'),
        xaxis_rangeslider_visible=False,
        xaxis=dict(gridcolor='#1a2233'),
        yaxis=dict(gridcolor='#1a2233')
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
else:
    st.info("Fetching live candles from Binance servers...")
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# ADVANCED SIGNAL ANALYSIS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🤖 JUTT BOT AI SIGNAL ENGINE")

if generate:
    if candles and len(candles) >= 30:
        df_ana = pd.DataFrame(candles)
        df_ana["RSI"] = RSIIndicator(close=df_ana["close"], window=14).rsi()
        df_ana["EMA_9"] = EMAIndicator(close=df_ana["close"], window=9).ema_indicator()
        df_ana["EMA_21"] = EMAIndicator(close=df_ana["close"], window=21).ema_indicator()
        
        atr = AverageTrueRange(
            high=df_ana["high"], low=df_ana["low"], close=df_ana["close"], window=14
        ).average_true_range().iloc[-1]

        current_price = df_ana["close"].iloc[-1]
        current_rsi = df_ana["RSI"].iloc[-1]
        ema_9 = df_ana["EMA_9"].iloc[-1]
        ema_21 = df_ana["EMA_21"].iloc[-1]

        signal = "NO SIGNAL"
        reasons = []

        if current_rsi < 42 and ema_9 > ema_21:
            signal = "CALL"
            reasons.append("RSI shows strong oversold momentum turning upward.")
            reasons.append("Fast EMA (9) has crossed above Slow EMA (21).")
        elif current_rsi > 58 and ema_9 < ema_21:
            signal = "PUT"
            reasons.append("RSI indicates overbought market pressure.")
            reasons.append("Fast EMA (9) is trading below Slow EMA (21).")
        else:
            reasons.append("Market is currently consolidating or moving sideways. Waiting for high-probability setup.")

        st.session_state.last_analysis = {
            "signal": signal,
            "price": current_price,
            "rsi": current_rsi,
            "atr": atr,
            "reasons": reasons
        }

analysis = st.session_state.get("last_analysis")

if analysis:
    sig = analysis["signal"]
    if sig == "CALL":
        sl = analysis['price'] - (1.5 * analysis['atr'])
        tp = analysis['price'] + (2.5 * analysis['atr'])
        st.markdown('<div class="signal-call">🚀 BUY / LONG (CALL)</div>', unsafe_allow_html=True)
        st.success(f"🎯 **Entry Price:** {analysis['price']:,.2f} | 🛡️ **Stop-Loss:** {sl:,.2f} | 💰 **Take-Profit:** {tp:,.2f}")
    elif sig == "PUT":
        sl = analysis['price'] + (1.5 * analysis['atr'])
        tp = analysis['price'] - (2.5 * analysis['atr'])
        st.markdown('<div class="signal-put">🔻 SELL / SHORT (PUT)</div>', unsafe_allow_html=True)
        st.error(f"🎯 **Entry Price:** {analysis['price']:,.2f} | 🛡️ **Stop-Loss:** {sl:,.2f} | 💰 **Take-Profit:** {tp:,.2f}")
    else:
        st.markdown('<div class="signal-none">⏳ NO CLEAR SETUP (WAIT)</div>', unsafe_allow_html=True)

    for r in analysis["reasons"]:
        st.markdown(f'<div class="reason-box">• {r}</div>', unsafe_allow_html=True)
else:
    st.info("Click **GENERATE PROFESSIONAL SIGNAL** above to get instant market prediction with Stop-Loss & Take-Profit targets.")

st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh loop to keep live ticks active
time.sleep(1.5)
st.rerun()
