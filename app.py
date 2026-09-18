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
    page_title="Jutt On Top",
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
# CSS (EXACT MATCH SCREENSHOT LAYOUT)
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
    max-width: 480px !important;
    padding-top: 10px !important;
    padding-bottom: 20px !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
}

.main-title {
    color: #ffffff;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.top-card {
    background: linear-gradient(145deg, #131b22, #0a0f14);
    border: 1px solid #2a3744;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.logo-container {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-img {
    width: 36px;
    height: 36px;
    object-fit: contain;
    border-radius: 8px;
    border: 1px solid #ffd338;
}

.brand-text-sm {
    color: #ffd338;
    font-size: 14px;
    font-weight: 800;
    line-height: 1.1;
}

.brand-sub-sm {
    color: #8c9ba5;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 1px;
}

.time-text {
    color: #ffd338;
    font-size: 13px;
    font-weight: 700;
}

.panel {
    background: linear-gradient(145deg, #10171d, #090e13);
    border: 1px solid #303c47;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

div[data-baseweb="select"] > div {
    background: #10171d !important;
    border: 1px solid #34414c !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span { color: #ffffff !important; font-size: 13px !important; }
label { color: #aab4bf !important; font-size: 12px !important; }

div.stButton > button {
    height: 48px;
    background: linear-gradient(135deg, #f2ba1d, #ffd33d);
    border: 1px solid #ffe47d;
    border-radius: 12px;
    color: #090909 !important;
    font-size: 16px;
    font-weight: 900;
    box-shadow: 0 0 15px rgba(255,193,7,.15);
    width: 100%;
}

.timer-box {
    background: #121921;
    border: 1px solid #2a3744;
    border-radius: 12px;
    padding: 10px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    font-size: 13px;
    font-weight: 600;
    color: #aab4bf;
}

.timer-val {
    color: #ffd338;
    font-weight: 800;
    letter-spacing: 1px;
}

.metrics-row {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
}

.metric-box {
    flex: 1;
    background: linear-gradient(145deg, #11191f, #0b1015);
    border: 1px solid #303c47;
    border-radius: 12px;
    padding: 10px 6px;
    text-align: center;
}

.metric-lbl { color: #8f9aa5; font-size: 10px; font-weight: 600; letter-spacing: 0.5px; }
.metric-val { color: #ffffff; font-size: 14px; font-weight: 800; margin-top: 3px; }

.signal-call {
    background: linear-gradient(135deg, #0b8a3f, #1db954);
    border: 2px solid #29f66e;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    margin-bottom: 10px;
}

.signal-put {
    background: linear-gradient(135deg, #a8192a, #dc3043);
    border: 2px solid #ff5969;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    margin-bottom: 10px;
}

.signal-neutral {
    background: linear-gradient(135deg, #1c242b, #0f1419);
    border: 1px solid #303c47;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
    margin-bottom: 10px;
}

.sig-title { color: #ffffff; font-size: 16px; font-weight: 900; }
.sig-sub { color: #d0d7de; font-size: 11px; margin-top: 3px; font-weight: 500; }

.green { color: #20e875 !important; }
.red { color: #ff5261 !important; }
.yellow { color: #ffd02f !important; }
</style>
""")

# ============================================================
# BINANCE CONSTANTS & FOREX/CRYPTO SYMBOLS MAPPING
# ============================================================

BINANCE_HOSTS = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://data-api.binance.vision"
]

PAIRS = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT",
    "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "LTCUSDT"
]

PAIR_NAMES = {
    "BTCUSDT": "BTC/USDT (Bitcoin)", "ETHUSDT": "ETH/USDT (Ethereum)",
    "SOLUSDT": "SOL/USDT (Solana)", "BNBUSDT": "BNB/USDT (BNB)",
    "XRPUSDT": "XRP/USDT (XRP)", "ADAUSDT": "ADA/USDT (Cardano)",
    "DOGEUSDT": "DOGE/USDT (Dogecoin)", "AVAXUSDT": "AVAX/USDT (Avalanche)",
    "LINKUSDT": "LINK/USDT (Chainlink)", "LTCUSDT": "LTC/USDT (Litecoin)"
}

TV_SYMBOLS = {
    "BTCUSDT": "BINANCE:BTCUSDT", "ETHUSDT": "BINANCE:ETHUSDT",
    "SOLUSDT": "BINANCE:SOLUSDT", "BNBUSDT": "BINANCE:BNBUSDT",
    "XRPUSDT": "BINANCE:XRPUSDT", "ADAUSDT": "BINANCE:ADAUSDT",
    "DOGEUSDT": "BINANCE:DOGEUSDT", "AVAXUSDT": "BINANCE:AVAXUSDT",
    "LINKUSDT": "BINANCE:LINKUSDT", "LTCUSDT": "BINANCE:LTCUSDT"
}

TIMEFRAMES = {
    "1 Minute (1m)": "1m", "3 Minutes (3m)": "3m", "5 Minutes (5m)": "5m",
    "15 Minutes (15m)": "15m", "30 Minutes (30m)": "30m", "1 Hour (1h)": "1h"
}

# ============================================================
# API FUNCTIONS
# ============================================================

def binance_request(endpoint, params):
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    for host in BINANCE_HOSTS:
        try:
            res = requests.get(host + endpoint, params=params, headers=headers, timeout=4)
            if res.status_code == 200:
                return res.json()
        except:
            continue
    return None

@st.cache_data(ttl=2)
def get_candles(symbol, interval):
    data = binance_request("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": 100})
    if not data:
        return pd.DataFrame()
    rows = []
    for c in data:
        rows.append({
            "time": int(c[0]), "open": float(c[1]), "high": float(c[2]),
            "low": float(c[3]), "close": float(c[4]), "volume": float(c[5])
        })
    return pd.DataFrame(rows)

def analyze_market(df):
    if df.empty or len(df) < 25:
        return None
    x = df.copy()
    x["RSI"] = RSIIndicator(close=x["close"], window=14).rsi()
    x["EMA9"] = EMAIndicator(close=x["close"], window=9).ema_indicator()
    x["EMA21"] = EMAIndicator(close=x["close"], window=21).ema_indicator()
    x["ATR"] = AverageTrueRange(high=x["high"], low=x["low"], close=x["close"], window=14).average_true_range()

    i = -2
    price = float(x["close"].iloc[i])
    rsi = float(x["RSI"].iloc[i])
    ema9 = float(x["EMA9"].iloc[i])
    ema21 = float(x["EMA21"].iloc[i])
    atr = float(x["ATR"].iloc[i])

    call_score, put_score = 0, 0
    if ema9 > ema21: call_score += 45
    else: put_score += 45

    if rsi < 45: call_score += 40
    elif rsi > 55: put_score += 40
    else:
        call_score += 20
        put_score += 20

    if call_score > put_score:
        signal, conf = "CALL", min(call_score + 15, 92)
    else:
        signal, conf = "PUT", min(put_score + 15, 92)

    trend = "BULLISH" if ema9 > ema21 else "BEARISH"
    return {"signal": signal, "confidence": conf, "price": price, "rsi": rsi, "atr": atr, "trend": trend}

# ============================================================
# HEADER & LOGO
# ============================================================

logo_path = "jutt_bot_logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_img_tag = f'<img src="data:image/png;base64,{logo_b64}" class="logo-img">'
else:
    logo_img_tag = '<span style="font-size:24px;">⭐</span>'

current_time_str = datetime.now().strftime("%I:%M:%S %p").lower()

html(f"""
<div class="main-title">
    <span>Jutt On Top</span>
    <span style="font-size:16px;">⭐</span>
</div>

<div class="top-card">
    <div class="logo-container">
        {logo_img_tag}
        <div>
            <div class="brand-text-sm">JUTTBOT</div>
            <div class="brand-sub-sm">PRO TRADER</div>
        </div>
    </div>
    <div class="time-text">{current_time_str}</div>
</div>
""")

# ============================================================
# CONTROLS & INPUTS
# ============================================================

html('<div class="panel">')
pair = st.selectbox("Pair / Asset", PAIRS, format_func=lambda x: PAIR_NAMES[x])
expiry_name = st.selectbox("Expiry Time", list(TIMEFRAMES.keys()))
timeframe = TIMEFRAMES[expiry_name]
generate = st.button("⚡ GENERATE AI SIGNAL")
html('</div>')

df = get_candles(pair, timeframe)
analysis = analyze_market(df)

connected = not df.empty
rsi_val = analysis["rsi"] if analysis else 50.0
trend_val = analysis["trend"] if analysis else "BULLISH"

# Signal Expiry Timer Bar
html(f"""
<div class="timer-box">
    <span>Signal Expiry Timer</span>
    <span class="timer-val">EXPIRY: READY</span>
</div>
""")

# Metrics Row (Live Feed, RSI, Trend)
feed_status_class = "green" if connected else "red"
feed_status_text = "CONNECTED" if connected else "OFFLINE"
trend_display = '<span class="green">BULLISH 🟢</span>' if trend_val == "BULLISH" else '<span class="red">BEARISH 🔴</span>'

html(f"""
<div class="metrics-row">
    <div class="metric-box">
        <div class="metric-lbl">LIVE FEED</div>
        <div class="metric-val {feed_status_class}">{feed_status_text}</div>
    </div>
    <div class="metric-box">
        <div class="metric-lbl">RSI (14)</div>
        <div class="metric-val">{rsi_val:.1f}</div>
    </div>
    <div class="metric-box">
        <div class="metric-lbl">TREND</div>
        <div class="metric-val">{trend_display}</div>
    </div>
</div>
""")

# Handle Generation State
if generate:
    if analysis:
        st.session_state["signal_data"] = analysis
        st.session_state["signal_pair"] = pair
        st.session_state["signal_tf"] = timeframe

sig_data = st.session_state.get("signal_data")
if sig_data and (st.session_state.get("signal_pair") != pair or st.session_state.get("signal_tf") != timeframe):
    sig_data = None

clean_pair_name = pair.replace("USDT", " / USDT")

if sig_data:
    sig = sig_data["signal"]
    conf = sig_data["confidence"]
    if sig == "CALL":
        html(f"""
        <div class="signal-call">
            <div class="sig-title">CALL ▲ [ {clean_pair_name} — UP / HIGHER ]</div>
            <div class="sig-sub">Win Probability: {conf}% | Expiry: {expiry_name}</div>
        </div>
        """)
    else:
        html(f"""
        <div class="signal-put">
            <div class="sig-title">PUT ▼ [ {clean_pair_name} — DOWN / LOWER ]</div>
            <div class="sig-sub">Win Probability: {conf}% | Expiry: {expiry_name}</div>
        </div>
        """)
else:
    html(f"""
    <div class="signal-neutral">
        <div class="sig-title">⚡ READY FOR SIGNAL</div>
        <div class="sig-sub">Click above to analyze {clean_pair_name}</div>
    </div>
    """)

# ============================================================
# TRADINGVIEW LIVE CHART WIDGET (At the Bottom)
# ============================================================

tv_symbol = TV_SYMBOLS.get(pair, "BINANCE:BTCUSDT")

chart_html = f"""
<div style="background:#10171d; border:1px solid #303c47; border-radius:14px; padding:8px; margin-top:10px;">
    <div class="tradingview-widget-container" style="height:380px; width:100%;">
      <div class="tradingview-widget-container__widget" style="height:100%;width:100%"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
      {{
        "width": "100%",
        "height": "380",
        "symbol": "{tv_symbol}",
        "interval": "1",
        "timezone": "Etc/UTC",
        "theme": "dark",
        "style": "1",
        "locale": "en",
        "allow_symbol_change": false,
        "calendar": false,
        "support_host": "https://www.tradingview.com"
      }}
      </script>
    </div>
</div>
"""

st.components.v1.html(chart_html, height=400)
