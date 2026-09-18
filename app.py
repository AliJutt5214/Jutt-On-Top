import streamlit as st
import pandas as pd
import requests
import json
import os
import base64
import textwrap
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JUTT BOT PRO TRADER",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# HTML RENDER FIX
# ============================================================

def html(content):
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )

# ============================================================
# CSS
# ============================================================

html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background: radial-gradient(circle at 50% -10%, #17251c 0%, #080d11 38%, #040608 80%);
    color: #ffffff !important;
}

header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stStatusWidget"], [data-testid="stDecoration"], [data-testid="stHeader"], [data-testid="stBottom"], [data-testid="stDeployButton"], [data-testid="stAppDeployButton"], .viewerBadge_container__1QSob, [class*="viewerBadge"] {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 12px !important;
    padding-bottom: 20px !important;
}

.hero {
    background: radial-gradient(circle at 50% 40%, rgba(255,193,7,.14), transparent 38%), linear-gradient(125deg, #05080b, #10171b, #06090c);
    border: 2px solid #d6aa2c;
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 0 35px rgba(255,193,7,.12), inset 0 0 35px rgba(255,193,7,.025);
}

.hero-grid {
    display: grid;
    grid-template-columns: 220px 1fr 180px;
    gap: 20px;
    align-items: center;
    min-height: 190px;
}

.logo-box {
    width: 205px;
    height: 175px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
}

.logo-box img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 18px;
}

.brand-area { text-align: center; }
.brand-main { color: #ffd338; font-size: 52px; font-weight: 900; letter-spacing: 3px; line-height: 1; }
.brand-pro { color: #ffffff; font-size: 22px; font-weight: 800; letter-spacing: 7px; margin-top: 8px; }
.brand-tag { color: #ffd02f; font-size: 14px; font-weight: 800; letter-spacing: 3px; margin-top: 13px; }
.brand-sub { color: #9ba7b2; font-size: 10px; letter-spacing: 2px; margin-top: 9px; }

.live-card {
    background: #10171c;
    border: 1px solid #394650;
    border-radius: 16px;
    padding: 17px;
    text-align: center;
}

.live-title { color: #a9b2bc; font-size: 13px; }
.live-dot { color: #19e86c; font-size: 18px; }
.live-time { color: #ffd02f; font-size: 19px; font-weight: 900; margin-top: 7px; }

.panel {
    background: linear-gradient(145deg, #10171d, #090e13);
    border: 1px solid #303c47;
    border-radius: 17px;
    padding: 16px;
    margin-bottom: 14px;
}

div[data-baseweb="select"] > div {
    background: #10171d !important;
    border: 1px solid #34414c !important;
    border-radius: 12px !important;
}

div[data-baseweb="select"] span { color: #ffffff !important; }
label { color: #aab4bf !important; }

div.stButton > button {
    height: 58px;
    background: linear-gradient(135deg, #f2ba1d, #ffd33d);
    border: 1px solid #ffe47d;
    border-radius: 15px;
    color: #090909 !important;
    font-size: 20px;
    font-weight: 900;
    box-shadow: 0 0 25px rgba(255,193,7,.15);
}

.metric-card {
    background: linear-gradient(145deg, #11191f, #0b1015);
    border: 1px solid #303c47;
    border-radius: 16px;
    min-height: 108px;
    padding: 15px 8px;
    text-align: center;
}

.metric-title { color: #8f9aa5; font-size: 12px; letter-spacing: 1px; }
.metric-value { color: #ffffff; font-size: 22px; font-weight: 900; margin-top: 8px; }

.green { color: #20e875 !important; }
.red { color: #ff5261 !important; }
.yellow { color: #ffd02f !important; }

.signal-call {
    background: linear-gradient(135deg, #087d38, #20b953);
    border: 2px solid #29f66e;
    border-radius: 18px;
    padding: 19px;
    text-align: center;
    margin: 15px 0;
}

.signal-put {
    background: linear-gradient(135deg, #981727, #dc3043);
    border: 2px solid #ff5969;
    border-radius: 18px;
    padding: 19px;
    text-align: center;
    margin: 15px 0;
}

.signal-neutral {
    background: linear-gradient(135deg, #242b31, #12181d);
    border: 1px solid #56616b;
    border-radius: 18px;
    padding: 19px;
    text-align: center;
    margin: 15px 0;
}

.signal-title { color: #ffffff; font-size: 27px; font-weight: 900; }
.signal-sub { color: #ffffff; font-size: 14px; margin-top: 6px; }

.chart-panel {
    background: #080d12;
    border: 1px solid #2d3943;
    border-radius: 17px;
    padding: 10px;
    margin-bottom: 14px;
}

.chart-heading { color: #dce3e8; font-size: 15px; font-weight: 800; padding: 8px; }
.footer { text-align: center; color: #65717c; font-size: 10px; letter-spacing: 3px; padding: 18px; }
</style>
""")

# ============================================================
# BINANCE CONSTANTS
# ============================================================

BINANCE_HOSTS = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com"
]

PAIRS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT"
]

PAIR_NAMES = {
    "BTCUSDT": "BTCUSDT (Bitcoin)", "ETHUSDT": "ETHUSDT (Ethereum)",
    "SOLUSDT": "SOLUSDT (Solana)", "BNBUSDT": "BNBUSDT (BNB)",
    "XRPUSDT": "XRPUSDT (XRP)", "ADAUSDT": "ADAUSDT (Cardano)",
    "DOGEUSDT": "DOGEUSDT (Dogecoin)", "AVAXUSDT": "AVAXUSDT (Avalanche)",
    "LINKUSDT": "LINKUSDT (Chainlink)", "LTCUSDT": "LTCUSDT (Litecoin)"
}

TIMEFRAMES = {
    "1 Minute (1m)": "1m", "3 Minutes (3m)": "3m", "5 Minutes (5m)": "5m",
    "15 Minutes (15m)": "15m", "30 Minutes (30m)": "30m", "1 Hour (1h)": "1h"
}

# ============================================================
# API REQUEST FUNCTION
# ============================================================

def binance_request(endpoint, params):
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    for host in BINANCE_HOSTS:
        try:
            response = requests.get(host + endpoint, params=params, headers=headers, timeout=7)
            if response.status_code == 200:
                return response.json()
        except Exception:
            continue
    return None

@st.cache_data(ttl=1)
def get_live_price(symbol):
    data = binance_request("/api/v3/ticker/price", {"symbol": symbol})
    if data and "price" in data:
        return float(data["price"])
    return None

@st.cache_data(ttl=2)
def get_24h(symbol):
    data = binance_request("/api/v3/ticker/24hr", {"symbol": symbol})
    if data:
        return float(data.get("priceChange", 0)), float(data.get("priceChangePercent", 0))
    return 0.0, 0.0

@st.cache_data(ttl=2)
def get_candles(symbol, interval):
    data = binance_request("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": 200})
    if not data:
        return pd.DataFrame()
    rows = []
    for c in data:
        rows.append({
            "time": int(c[0]), "open": float(c[1]), "high": float(c[2]),
            "low": float(c[3]), "close": float(c[4]), "volume": float(c[5])
        })
    return pd.DataFrame(rows)

# ============================================================
# TECHNICAL ANALYSIS
# ============================================================

def analyze_market(df):
    if df.empty or len(df) < 50:
        return None
    x = df.copy()
    x["RSI"] = RSIIndicator(close=x["close"], window=14).rsi()
    x["EMA9"] = EMAIndicator(close=x["close"], window=9).ema_indicator()
    x["EMA21"] = EMAIndicator(close=x["close"], window=21).ema_indicator()
    x["ATR"] = AverageTrueRange(high=x["high"], low=x["low"], close=x["close"], window=14).average_true_range()

    i, p = -2, -3
    price = float(x["close"].iloc[i])
    rsi = float(x["RSI"].iloc[i])
    ema9 = float(x["EMA9"].iloc[i])
    ema21 = float(x["EMA21"].iloc[i])
    prev9 = float(x["EMA9"].iloc[p])
    prev21 = float(x["EMA21"].iloc[p])
    atr = float(x["ATR"].iloc[i])

    call_score, put_score = 0, 0
    reasons = []

    if ema9 > ema21:
        call_score += 30
        reasons.append("EMA 9 is above EMA 21")
    elif ema9 < ema21:
        put_score += 30
        reasons.append("EMA 9 is below EMA 21")

    if prev9 <= prev21 and ema9 > ema21:
        call_score += 30
        reasons.append("Bullish EMA crossover")
    elif prev9 >= prev21 and ema9 < ema21:
        put_score += 30
        reasons.append("Bearish EMA crossover")

    if rsi < 35:
        call_score += 20
        reasons.append("RSI is in oversold zone")
    elif rsi > 65:
        put_score += 20
        reasons.append("RSI is in overbought zone")

    if x["close"].iloc[i] > x["open"].iloc[i]:
        call_score += 10
    elif x["close"].iloc[i] < x["open"].iloc[i]:
        put_score += 10

    if call_score >= 60 and call_score > put_score:
        signal, confidence = "CALL", min(call_score, 95)
    elif put_score >= 60 and put_score > call_score:
        signal, confidence = "PUT", min(put_score, 95)
    else:
        signal, confidence = "NO SIGNAL", max(call_score, put_score)

    trend = "BULLISH" if ema9 > ema21 else ("BEARISH" if ema9 < ema21 else "NEUTRAL")

    return {
        "signal": signal, "confidence": confidence, "price": price,
        "rsi": rsi, "ema9": ema9, "ema21": ema21, "atr": atr,
        "trend": trend, "reasons": reasons
    }

# ============================================================
# LOGO HANDLING
# ============================================================

logo_path = "jutt_bot_logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}">'
else:
    logo_html = '<div style="color:#ffd338;font-size:60px;font-weight:900;">⭐</div>'

# ============================================================
# HEADER & LAYOUT
# ============================================================

clock = datetime.now().strftime("%I:%M:%S %p")

html(f"""
<div class="hero">
    <div class="hero-grid">
        <div class="logo-box">{logo_html}</div>
        <div class="brand-area">
            <div class="brand-main">JUTT BOT</div>
            <div class="brand-pro">PRO TRADER</div>
            <div class="brand-tag">ANALYZE | SIGNAL | TRADE | GROW</div>
            <div class="brand-sub">DISCIPLINE TODAY • BIGGER TOMORROW</div>
        </div>
        <div class="live-card">
            <div class="live-title"><span class="live-dot">●</span> LIVE MARKET</div>
            <div class="live-time">{clock}</div>
        </div>
    </div>
</div>
""")

html('<div class="panel">')
c1, c2 = st.columns(2)
with c1:
    pair = st.selectbox("📊 Pair / Asset", PAIRS, format_func=lambda x: PAIR_NAMES[x])
with c2:
    timeframe_name = st.selectbox("⏳ Timeframe", list(TIMEFRAMES.keys()))

timeframe = TIMEFRAMES[timeframe_name]
generate = st.button("⚡ GENERATE AI SIGNAL", use_container_width=True)
html('</div>')

live_price = get_live_price(pair)
change, change_percent = get_24h(pair)
df = get_candles(pair, timeframe)
analysis = analyze_market(df)

rsi = analysis["rsi"] if analysis else 0
trend = analysis["trend"] if analysis else "OFFLINE"
connected = live_price is not None and not df.empty

m1, m2, m3, m4 = st.columns(4)

with m1:
    status = "CONNECTED" if connected else "OFFLINE"
    cls = "green" if connected else "red"
    html(f'<div class="metric-card"><div class="metric-title">LIVE FEED</div><div class="metric-value {cls}">● {status}</div></div>')

with m2:
    price_text = f"${live_price:,.2f}" if live_price is not None else "--"
    change_cls = "green" if change_percent >= 0 else "red"
    html(f'<div class="metric-card"><div class="metric-title">LIVE PRICE</div><div class="metric-value">{price_text}</div><div class="{change_cls}">{change:+,.2f} ({change_percent:+.2f}%)</div></div>')

with m3:
    html(f'<div class="metric-card"><div class="metric-title">RSI (14)</div><div class="metric-value">{rsi:.2f}</div></div>')

with m4:
    trend_html = '<span class="green">BULLISH 🟢</span>' if trend == "BULLISH" else ('<span class="red">BEARISH 🔴</span>' if trend == "BEARISH" else '<span class="yellow">NEUTRAL 🟡</span>')
    html(f'<div class="metric-card"><div class="metric-title">TREND</div><div class="metric-value">{trend_html}</div></div>')

if generate:
    if analysis:
        st.session_state["signal_data"] = analysis
        st.session_state["signal_pair"] = pair
        st.session_state["signal_tf"] = timeframe
    else:
        st.error("Binance live market data is unavailable.")

signal_data = st.session_state.get("signal_data")
if signal_data and (st.session_state.get("signal_pair") != pair or st.session_state.get("signal_tf") != timeframe):
    signal_data = None

if signal_data:
    signal = signal_data["signal"]
    entry = live_price if live_price is not None else signal_data["price"]
    confidence = signal_data["confidence"]
    atr = signal_data["atr"]

    if signal == "CALL":
        sl, tp = entry - (1.5 * atr), entry + (2.5 * atr)
        html(f'<div class="signal-call"><div class="signal-title">▲ CALL ▲ [ {pair} — UP / HIGHER ]</div><div class="signal-sub">Technical Signal Strength: {confidence}% | Timeframe: {timeframe_name}</div></div>')
        a, b, c = st.columns(3)
        a.metric("ENTRY", f"{entry:,.2f}")
        b.metric("STOP LOSS", f"{sl:,.2f}")
        c.metric("TAKE PROFIT", f"{tp:,.2f}")
    elif signal == "PUT":
        sl, tp = entry + (1.5 * atr), entry - (2.5 * atr)
        html(f'<div class="signal-put"><div class="signal-title">▼ PUT ▼ [ {pair} — DOWN / LOWER ]</div><div class="signal-sub">Technical Signal Strength: {confidence}% | Timeframe: {timeframe_name}</div></div>')
        a, b, c = st.columns(3)
        a.metric("ENTRY", f"{entry:,.2f}")
        b.metric("STOP LOSS", f"{sl:,.2f}")
        c.metric("TAKE PROFIT", f"{tp:,.2f}")
    else:
        html(f'<div class="signal-neutral"><div class="signal-title">⏳ NO CLEAR SETUP — WAIT</div><div class="signal-sub">{pair} • {timeframe_name}</div></div>')
else:
    html(f'<div class="signal-neutral"><div class="signal-title">⚡ GENERATE AI SIGNAL</div><div class="signal-sub">{pair} • {timeframe_name} • Binance Live Market</div></div>')

# ============================================================
# RECENT SIGNALS & FOOTER
# ============================================================
if "recent_signals" not in st.session_state:
    st.session_state.recent_signals = []

if generate and signal_data:
    new_signal = {
        "TIME": datetime.now().strftime("%H:%M:%S"), "PAIR": pair,
        "SIGNAL": signal_data["signal"], "PRICE": signal_data["price"],
        "STRENGTH": f"{signal_data['confidence']}%"
    }
    st.session_state.recent_signals.insert(0, new_signal)
    st.session_state.recent_signals = st.session_state.recent_signals[:10]

html('<div class="panel"><div class="recent-title">📋 RECENT SIGNALS</div></div>')
if st.session_state.recent_signals:
    st.dataframe(pd.DataFrame(st.session_state.recent_signals), use_container_width=True, hide_index=True)
else:
    st.info("No signals generated yet.")

html('<div class="footer">JUTT BOT PRO • ANALYZE | SIGNAL | TRADE | GROW</div>'
