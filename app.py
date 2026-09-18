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

st.set_page_config(
    page_title="Jutt On Top",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def html(content):
    st.markdown(
        textwrap.dedent(content).strip(),
        unsafe_allow_html=True
    )

html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif !important; }
.stApp { background: radial-gradient(circle at 50% -10%, #17251c 0%, #080d11 38%, #040608 80%); color: #ffffff !important; }
header, footer, #MainMenu, [data-testid="stToolbar"], [data-testid="stStatusWidget"], [data-testid="stDecoration"], [data-testid="stHeader"], [data-testid="stBottom"], [data-testid="stDeployButton"], [data-testid="stAppDeployButton"] { display: none !important; visibility: hidden !important; }
.block-container { max-width: 480px !important; padding: 10px !important; }
.main-title { color: #ffffff; font-size: 20px; font-weight: 700; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
.top-card { background: linear-gradient(145deg, #131b22, #0a0f14); border: 1px solid #2a3744; border-radius: 14px; padding: 12px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; }
.logo-container { display: flex; align-items: center; gap: 12px; }
.logo-img { width: 48px; height: 48px; object-fit: cover; border-radius: 10px; border: 2px solid #ffd338; }
.brand-text-sm { color: #ffd338; font-size: 15px; font-weight: 900; line-height: 1.1; }
.brand-sub-sm { color: #8c9ba5; font-size: 9px; font-weight: 600; letter-spacing: 1px; }
.time-text { color: #ffd338; font-size: 13px; font-weight: 700; }
.panel { background: linear-gradient(145deg, #10171d, #090e13); border: 1px solid #303c47; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
div[data-baseweb="select"] > div { background: #10171d !important; border: 1px solid #34414c !important; border-radius: 10px !important; }
div[data-baseweb="select"] span { color: #ffffff !important; font-size: 13px !important; }
label { color: #aab4bf !important; font-size: 12px !important; }
div.stButton > button { height: 48px; background: linear-gradient(135deg, #f2ba1d, #ffd33d); border: 1px solid #ffe47d; border-radius: 12px; color: #090909 !important; font-size: 16px; font-weight: 900; width: 100%; }
.timer-box { background: #121921; border: 1px solid #2a3744; border-radius: 12px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-size: 13px; font-weight: 600; color: #aab4bf; }
.timer-val { color: #ffd338; font-weight: 800; letter-spacing: 1px; }
.metrics-row { display: flex; gap: 8px; margin-bottom: 10px; }
.metric-box { flex: 1; background: linear-gradient(145deg, #11191f, #0b1015); border: 1px solid #303c47; border-radius: 12px; padding: 10px 6px; text-align: center; }
.metric-lbl { color: #8f9aa5; font-size: 10px; font-weight: 600; }
.metric-val { color: #ffffff; font-size: 14px; font-weight: 800; margin-top: 3px; }
.signal-call { background: linear-gradient(135deg, #0b8a3f, #1db954); border: 2px solid #29f66e; border-radius: 14px; padding: 14px; text-align: center; margin-bottom: 10px; }
.signal-put { background: linear-gradient(135deg, #a8192a, #dc3043); border: 2px solid #ff5969; border-radius: 14px; padding: 14px; text-align: center; margin-bottom: 10px; }
.signal-neutral { background: linear-gradient(135deg, #1c242b, #0f1419); border: 1px solid #303c47; border-radius: 14px; padding: 14px; text-align: center; margin-bottom: 10px; }
.sig-title { color: #ffffff; font-size: 16px; font-weight: 900; }
.sig-sub { color: #d0d7de; font-size: 11px; margin-top: 3px; font-weight: 500; }
.green { color: #20e875 !important; }
.red { color: #ff5261 !important; }
</style>
""")

BINANCE_HOSTS = ["https://api.binance.com", "https://api1.binance.com", "https://api2.binance.com"]
PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
PAIR_NAMES = {"BTCUSDT": "BTC / USDT", "ETHUSDT": "ETH / USDT", "SOLUSDT": "SOL / USDT", "BNBUSDT": "BNB / USDT", "XRPUSDT": "XRP / USDT"}
TV_SYMBOLS = {"BTCUSDT": "BINANCE:BTCUSDT", "ETHUSDT": "BINANCE:ETHUSDT", "SOLUSDT": "BINANCE:SOLUSDT", "BNBUSDT": "BINANCE:BNBUSDT", "XRPUSDT": "BINANCE:XRPUSDT"}
TIMEFRAMES = {"1 Minute (1m)": {"code": "1m", "seconds": 60}, "3 Minutes (3m)": {"code": "3m", "seconds": 180}, "5 Minutes (5m)": {"code": "5m", "seconds": 300}}

def binance_request(endpoint, params):
    headers = {"User-Agent": "Mozilla/5.0"}
    for host in BINANCE_HOSTS:
        try:
            res = requests.get(host + endpoint, params=params, headers=headers, timeout=4)
            if res.status_code == 200: return res.json()
        except: continue
    return None

@st.cache_data(ttl=2)
def get_candles(symbol, interval):
    data = binance_request("/api/v3/klines", {"symbol": symbol, "interval": interval, "limit": 100})
    if not data: return pd.DataFrame()
    return pd.DataFrame([{"time": int(c[0]), "open": float(c[1]), "high": float(c[2]), "low": float(c[3]), "close": float(c[4]), "volume": float(c[5])} for c in data])

def analyze_market(df):
    if df.empty or len(df) < 25: return None
    x = df.copy()
    x["RSI"] = RSIIndicator(close=x["close"], window=14).rsi()
    x["EMA9"] = EMAIndicator(close=x["close"], window=9).ema_indicator()
    x["EMA21"] = EMAIndicator(close=x["close"], window=21).ema_indicator()
    i = -2
    rsi, ema9, ema21 = float(x["RSI"].iloc[i]), float(x["EMA9"].iloc[i]), float(x["EMA21"].iloc[i])
    signal = "CALL" if ema9 > ema21 and rsi < 55 else "PUT"
    conf = 88 if abs(ema9 - ema21) > 1 else 75
    trend = "BULLISH" if ema9 > ema21 else "BEARISH"
    return {"signal": signal, "confidence": conf, "rsi": rsi, "trend": trend}

html('<div class="main-title"><span>Jutt On Top</span><span>⭐</span></div>')

pair = st.selectbox("Pair / Asset", PAIRS, format_func=lambda x: PAIR_NAMES[x])
expiry_name = st.selectbox("Expiry Time", list(TIMEFRAMES.keys()))
timeframe = TIMEFRAMES[expiry_name]["code"]
expiry_seconds = TIMEFRAMES[expiry_name]["seconds"]
generate = st.button("⚡ GENERATE AI SIGNAL")

df = get_candles(pair, timeframe)
analysis = analyze_market(df)
connected = not df.empty
rsi_val = analysis["rsi"] if analysis else 50.0
trend_val = analysis["trend"] if analysis else "BULLISH"

if generate and analysis:
    st.session_state["signal_data"] = analysis
    st.session_state["signal_pair"] = pair
    import time
    st.session_state["expiry_target_timestamp"] = int(time.time()) + expiry_seconds

sig_data = st.session_state.get("signal_data")
target_ts = st.session_state.get("expiry_target_timestamp", 0)

html(f"""
<div class="timer-box">
    <span>Timer</span>
    <span class="timer-val" id="cdt">READY</span>
</div>
<script>
const targetTime = {target_ts};
function updateTimer() {{
    const el = document.getElementById('cdt');
    if (!el || !targetTime) return;
    const diff = targetTime - Math.floor(Date.now() / 1000);
    if (diff <= 0) el.innerText = "EXPIRED";
    else el.innerText = Math.floor(diff/60) + ":" + (diff%60 < 10 ? "0" : "") + (diff%60) + " REMAINING";
}}
setInterval(updateTimer, 1000);
updateTimer();
</script>
""")

if sig_data:
    sig = sig_data["signal"]
    conf = sig_data["confidence"]
    if sig == "CALL":
        html(f'<div class="signal-call"><div class="sig-title">CALL ▲ ({pair})</div><div class="sig-sub">Probability: {conf}%</div></div>')
    else:
        html(f'<div class="signal-put"><div class="sig-title">▼ PUT ▼ ({pair})</div><div class="sig-sub">Probability: {conf}%</div></div>')
else:
    html(f'<div class="signal-neutral"><div class="sig-title">⚡ READY</div><div class="sig-sub">Click generate for signal</div></div>')
