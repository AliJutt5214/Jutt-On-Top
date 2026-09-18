import streamlit as st
import pandas as pd
import requests
import json
import threading
import time
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange

# ============================================================
# PAGE CONFIG & PROFESSIONAL SETUP
# ============================================================

st.set_page_config(
    page_title="JUTT BOT PRO TRADER",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# PROFESSIONAL CSS & COMPLETE HIDING OF STREAMLIT BADGES
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #07090e;
        color: #ffffff;
    }
    
    /* Completely hide Streamlit branding, footer badges, and floating menus */
    header { visibility: hidden !important; display: none !important; }
    #MainMenu { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    .stApp > footer { display: none !important; visibility: hidden !important; }
    #stDecoration { display: none !important; visibility: hidden !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
    .viewerBadge_container__1QSob { display: none !important; visibility: hidden !important; }
    div[class*="viewerBadge"] { display: none !important; visibility: hidden !important; }
    iframe { display: none !important; }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .header-box {
        background: linear-gradient(135deg, #11151c 0%, #1a222d 100%);
        border: 2px solid #d4af37;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2);
    }

    .main-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #ffd700, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        margin: 0;
    }

    .sub-title {
        color: #a0aec0;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    .card {
        background: #111622;
        border: 1px solid #232d3f;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }

    .signal-call {
        color: #00ecb0;
        font-size: 34px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 15px rgba(0, 236, 176, 0.4);
    }

    .signal-put {
        color: #ff4d4d;
        font-size: 34px;
        font-weight: 900;
        text-align: center;
        text-shadow: 0 0 15px rgba(255, 77, 77, 0.4);
    }

    .signal-none {
        color: #ffcc00;
        font-size: 30px;
        font-weight: 900;
        text-align: center;
    }

    .reason-box {
        padding: 8px 0;
        border-bottom: 1px solid #1a2233;
        font-size: 14px;
        color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

PAIR_LIST = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", 
    "XRPUSDT", "ADAUSDT", "DOGEUSDT", "AVAXUSDT"
]

# ============================================================
# BINANCE SECURE DATA ENGINE
# ============================================================

class BinanceProEngine:
    def __init__(self):
        self.connected = False
        self.ticks = []
        self.lock = threading.Lock()
        self.current_symbol = "XRPUSDT"

    def get_candles(self, symbol, interval="15m", limit=100):
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

if "engine" not in st.session_state:
    st.session_state.engine = BinanceProEngine()

engine = st.session_state.engine

# ============================================================
# PROFESSIONAL HEADER (TEXT LOGO)
# ============================================================

st.markdown("""
<div class="header-box">
    <div class="main-title">JUTT ON TOP</div>
    <div class="sub-title">Professional AI Binance Scalping & Signal Analyzer</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONTROLS PANEL
# ============================================================

col1, col2 = st.columns([1.5, 1])

with col1:
    pair = st.selectbox("SELECT TRADING PAIR", PAIR_LIST, index=4)

with col2:
    timeframe = st.selectbox("TIMEFRAME", ["1m", "3m", "5m", "15m", "30m", "1h"], index=3)

generate = st.button("⚡ GENERATE PROFESSIONAL SIGNAL", use_container_width=True)

# ============================================================
# FETCH LIVE MARKET DATA
# ============================================================

candles = engine.get_candles(pair, timeframe, 100)
df_m = pd.DataFrame(candles)

m1, m2 = st.columns(2)

with m1:
    if not df_m.empty:
        current_price = df_m["close"].iloc[-1]
        st.metric("REAL-TIME PRICE", f"${current_price:,.4f}")
    else:
        st.metric("REAL-TIME PRICE", "Connecting...")

with m2:
    if not df_m.empty:
        rsi_val = RSIIndicator(close=df_m["close"], window=14).rsi().iloc[-1]
        st.metric("RSI (14)", f"{rsi_val:.2f}")
    else:
        st.metric("RSI (14)", "--")

# ============================================================
# ADVANCED SIGNAL ANALYSIS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🤖 JUTT BOT AI SIGNAL ENGINE")

if generate:
    if not df_m.empty and len(df_m) >= 30:
        df_m["RSI"] = RSIIndicator(close=df_m["close"], window=14).rsi()
        df_m["EMA_9"] = EMAIndicator(close=df_m["close"], window=9).ema_indicator()
        df_m["EMA_21"] = EMAIndicator(close=df_m["close"], window=21).ema_indicator()
        
        atr = AverageTrueRange(
            high=df_m["high"], low=df_m["low"], close=df_m["close"], window=14
        ).average_true_range().iloc[-1]

        cur_price = df_m["close"].iloc[-1]
        cur_rsi = df_m["RSI"].iloc[-1]
        ema_9 = df_m["EMA_9"].iloc[-1]
        ema_21 = df_m["EMA_21"].iloc[-1]

        signal = "NO SIGNAL"
        reasons = []

        if cur_rsi < 45 and ema_9 > ema_21:
            signal = "CALL"
            reasons.append("RSI indicates oversold momentum turning bullish.")
            reasons.append("Fast EMA (9) crossed above Slow EMA (21).")
        elif cur_rsi > 55 and ema_9 < ema_21:
            signal = "PUT"
            reasons.append("RSI shows overbought market pressure.")
            reasons.append("Fast EMA (9) is trading below Slow EMA (21).")
        else:
            reasons.append("Market is currently consolidating. Waiting for strong breakout.")

        st.session_state.last_signal = {
            "signal": signal,
            "price": cur_price,
            "atr": atr,
            "reasons": reasons
        }
    else:
        st.warning("Please wait, fetching live market data...")

last_sig = st.session_state.get("last_signal")

if last_sig:
    sig = last_sig["signal"]
    if sig == "CALL":
        sl = last_sig['price'] - (1.5 * last_sig['atr'])
        tp = last_sig['price'] + (2.5 * last_sig['atr'])
        st.markdown('<div class="signal-call">🚀 BUY / LONG (CALL)</div>', unsafe_allow_html=True)
        st.success(f"🎯 **Entry:** {last_sig['price']:,.4f} | 🛡️ **SL:** {sl:,.4f} | 💰 **TP:** {tp:,.4f}")
    elif sig == "PUT":
        sl = last_sig['price'] + (1.5 * last_sig['atr'])
        tp = last_sig['price'] - (2.5 * last_sig['atr'])
        st.markdown('<div class="signal-put">🔻 SELL / SHORT (PUT)</div>', unsafe_allow_html=True)
        st.error(f"🎯 **Entry:** {last_sig['price']:,.4f} | 🛡️ **SL:** {sl:,.4f} | 💰 **TP:** {tp:,.4f}")
    else:
        st.markdown('<div class="signal-none">⏳ NO CLEAR SETUP (WAIT)</div>', unsafe_allow_html=True)

    for r in last_sig["reasons"]:
        st.markdown(f'<div class="reason-box">• {r}</div>', unsafe_allow_html=True)
else:
    st.info("Click **GENERATE PROFESSIONAL SIGNAL** above to get instant market predictions with Stop-Loss & Take-Profit targets.")

st.markdown('</div>', unsafe_allow_html=True)
