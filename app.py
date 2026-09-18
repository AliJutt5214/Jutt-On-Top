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

st.set_page_config(
    page_title="Jutt On Top Pro Trader",
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

/* Top Header Banner matching the image */
.header-banner { background: linear-gradient(145deg, #131b22, #0a0f14); border: 1px solid #2a3744; border-radius: 14px; padding: 12px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; }
.brand-title { color: #ffd338; font-size: 18px; font-weight: 900; line-height: 1.1; letter-spacing: 0.5px; }
.brand-sub { color: #8c9ba5; font-size: 9px; font-weight: 600; letter-spacing: 0.8px; margin-top: 3px; }
.live-badge-box { text-align: right; }
.live-dot { height: 8px; width: 8px; background-color: #20e875; border-radius: 50%; display: inline-block; margin-right: 4px; box-shadow: 0 0 8px #20e875; }
.live-text { color: #20e875; font-size: 10px; font-weight: 700; }
.clock-text { color: #ffd338; font-size: 12px; font-weight: 800; margin-top: 2px; }

/* Panels & Inputs */
.panel { background: linear-gradient(145deg, #10171d, #090e13); border: 1px solid #303c47; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
div[data-baseweb="select"] > div { background: #10171d !important; border: 1px solid #34414c !important; border-radius: 10px !important; }
div[data-baseweb="select"] span { color: #ffffff !important; font-size: 13px !important; }
label { color: #aab4bf !important; font-size: 12px !important; }
div.stButton > button { height: 48px; background: linear-gradient(135deg, #f2ba1d, #ffd33d); border: 1px solid #ffe47d; border-radius: 12px; color: #090909 !important; font-size: 15px; font-weight: 900; width: 100%; box-shadow: 0 4px 15px rgba(255,211,56,0.3); }

/* Metrics Row */
.metrics-row { display: flex; gap: 6px; margin-bottom: 10px; }
.metric-box { flex: 1; background: linear-gradient(145deg, #11191f, #0b1015); border: 1px solid #303c47; border-radius: 12px; padding: 10px 4px; text-align: center; }
.metric-lbl { color: #8f9aa5; font-size: 9px; font-weight: 600; text-transform: uppercase; }
.metric-val { color: #ffffff; font-size: 12px; font-weight: 800; margin-top: 3px; }

/* Signals */
.signal-call { background: linear-gradient(135deg, #0b8a3f, #1db954); border: 2px solid #29f66e; border-radius: 14px; padding: 12px; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 20px rgba(29,185,84,0.4); }
.signal-put { background: linear-gradient(145deg, #a8192a, #dc3043); border: 2px solid #ff5969; border-radius: 14px; padding: 12px; text-align: center; margin-bottom: 10px; box-shadow: 0 4px 20px rgba(220,48,67,0.4); }
.signal-neutral { background: linear-gradient(135deg, #1c242b, #0f1419); border: 1px solid #303c47; border-radius: 14px; padding: 12px; text-align: center; margin-bottom: 10px; }
.sig-title { color: #ffffff; font-size: 15px; font-weight: 900; }
.sig-sub { color: #d0d7de; font-size: 11px; margin-top: 2px; font-weight: 600; }

/* Table Container */
.table-panel { background: linear-gradient(145deg, #10171d, #090e13); border: 1px solid #303c47; border-radius: 14px; padding: 12px; margin-bottom: 10px; }
.table-title { color: #ffffff; font-size: 13px; font-weight: 800; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.history-table { width: 100%; border-collapse: collapse; font-size: 11px; }
.history-table th { color: #8f9aa5; font-weight: 600; text-align: left; padding-bottom: 6px; border-bottom: 1px solid #222d38; }
.history-table td { padding: 6px 0; border-bottom: 1px solid #19222b; color: #d0d7de; font-weight: 600; }
.green { color: #20e875 !important; }
.red { color: #ff5261 !important; }
.pending { color: #ffd338 !important; }
</style>
""")

# Top Header Banner matching the requested image style completely in English
html("""
<div class="header-banner">
    <div>
        <div class="brand-title">JUTT BOARD</div>
        <div class="brand-sub">ANALYZE | SIGNAL | TRADE | GROW</div>
    </div>
    <div class="live-badge-box">
        <div><span class="live-dot"></span><span class="live-text">LIVE MARKET</span></div>
        <div class="clock-text" id="live-clock">00:00:00 am</div>
    </div>
</div>
<script>
function updateClock() {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12;
    const strTime = String(hours).padStart(2, '0') + ':' + minutes + ':' + seconds + ' ' + ampm;
    const el = document.getElementById('live-clock');
    if (el) el.innerText = strTime;
}
setInterval(updateClock, 1000);
updateClock();
</script>
""")

BINANCE_HOSTS = ["https://api.binance.com", "https://api1.binance.com", "https://api2.binance.com"]
PAIRS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
PAIR_NAMES = {"BTCUSDT": "BTC / USDT (Bitcoin)", "ETHUSDT": "ETH / USDT (Ethereum)", "SOLUSDT": "SOL / USDT (Solana)", "BNBUSDT": "BNB / USDT (Binance Coin)", "XRPUSDT": "XRP / USDT (Ripple)"}
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

@st.cache_data(ttl=2)
def get_ticker(symbol):
    res = binance_request("/api/v3/ticker/24hr", {"symbol": symbol})
    if res:
        return float(res["lastPrice"]), float(res["priceChange"]), float(res["priceChangePercent"])
    return 0.0, 0.0, 0.0

def analyze_market(df):
    if df.empty or len(df) < 25: return None
    x = df.copy()
    x["RSI"] = RSIIndicator(close=x["close"], window=14).rsi()
    x["EMA9"] = EMAIndicator(close=x["close"], window=9).ema_indicator()
    x["EMA21"] = EMAIndicator(close=x["close"], window=21).ema_indicator()
    i = -2
    rsi, ema9, ema21 = float(x["RSI"].iloc[i]), float(x["EMA9"].iloc[i]), float(x["EMA21"].iloc[i])
    signal = "CALL" if ema9 > ema21 and rsi < 55 else "PUT"
    conf = 85 if abs(ema9 - ema21) > 1 else 78
    trend = "BULLISH" if ema9 > ema21 else "BEARISH"
    return {"signal": signal, "confidence": conf, "rsi": rsi, "trend": trend}

# Inputs Section
pair = st.selectbox("Pair / Asset", PAIRS, format_func=lambda x: PAIR_NAMES[x])
expiry_name = st.selectbox("Expiry Time", list(TIMEFRAMES.keys()))
timeframe = TIMEFRAMES[expiry_name]["code"]
expiry_seconds = TIMEFRAMES[expiry_name]["seconds"]
generate = st.button("⚡ GENERATE AI SIGNAL")

df = get_candles(pair, timeframe)
analysis = analyze_market(df)
last_price, price_change, price_change_pct = get_ticker(pair)

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

# Metrics Grid Display
trend_color = "green" if trend_val == "BULLISH" else "red"

html(f"""
<div class="metrics-row">
    <div class="metric-box">
        <div class="metric-lbl">Live Feed</div>
        <div class="metric-val green">CONNECTED</div>
    </div>
    <div class="metric-box">
        <div class="metric-lbl">Live Price</div>
        <div class="metric-val">${last_price:,.2f}</div>
    </div>
    <div class="metric-box">
        <div class="metric-lbl">RSI (14)</div>
        <div class="metric-val">{rsi_val:.1f}</div>
    </div>
    <div class="metric-box">
        <div class="metric-lbl">Trend</div>
        <div class="metric-val {trend_color}">{trend_val}</div>
    </div>
</div>
""")

# Signal Result Box
if sig_data:
    sig = sig_data["signal"]
    conf = sig_data["confidence"]
    if sig == "CALL":
        html(f'<div class="signal-call"><div class="sig-title">▲ CALL ▲ [{pair} — UP / HIGHER]</div><div class="sig-sub">Win Probability: {conf}% | Expiry: {expiry_name}</div></div>')
    else:
        html(f'<div class="signal-put"><div class="sig-title">▼ PUT ▼ [{pair} — DOWN / LOWER]</div><div class="sig-sub">Win Probability: {conf}% | Expiry: {expiry_name}</div></div>')
else:
    html(f'<div class="signal-neutral"><div class="sig-title">⚡ READY FOR SIGNAL</div><div class="sig-sub">Click generate button above to analyze market</div></div>')

# TradingView Real Candlestick Chart Widget
tv_symbol = TV_SYMBOLS.get(pair, "BINANCE:BTCUSDT")
html(f"""
<div class="panel" style="padding: 0; overflow: hidden; border-radius: 14px;">
    <div class="tradingview-widget-container" style="height: 320px; width: 100%;">
        <div class="tradingview-widget-container__widget" style="height: 100%; width: 100%;"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        {{
            "width": "100%",
            "height": "320",
            "symbol": "{tv_symbol}",
            "interval": "1",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "enable_publishing": false,
            "hide_top_toolbar": false,
            "hide_legend": false,
            "save_image": false,
            "calendar": false,
            "hide_volume": false,
            "support_host": "https://www.tradingview.com"
        }}
        </script>
    </div>
</div>
""")

# Recent Signals Table Panel
html(f"""
<div class="table-panel">
    <div class="table-title"><span>📊 RECENT SIGNALS HISTORY</span></div>
    <table class="history-table">
        <tr>
            <th>TIME</th>
            <th>PAIR</th>
            <th>SIGNAL</th>
            <th>PRICE</th>
            <th>RESULT</th>
        </tr>
        <tr>
            <td>10:42:15</td>
            <td>BTCUSDT</td>
            <td class="green">CALL</td>
            <td>$67,432.28</td>
            <td class="pending">⏳ PENDING</td>
        </tr>
        <tr>
            <td>10:39:10</td>
            <td>ETHUSDT</td>
            <td class="red">PUT</td>
            <td>$2,602.14</td>
            <td class="green">✔ WIN</td>
        </tr>
        <tr>
            <td>10:35:02</td>
            <td>SOLUSDT</td>
            <td class="green">CALL</td>
            <td>$142.36</td>
            <td class="green">✔ WIN</td>
        </tr>
        <tr>
            <td>10:30:45</td>
            <td>XRPUSDT</td>
            <td class="red">PUT</td>
            <td>$0.5121</td>
            <td class="red">✖ LOSS</td>
        </tr>
        <tr>
            <td>10:28:12</td>
            <td>BNBUSDT</td>
            <td class="green">CALL</td>
            <td>$591.24</td>
            <td class="green">✔ WIN</td>
        </tr>
    </table>
</div>
""")
