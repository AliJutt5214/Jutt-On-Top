import streamlit as st
import pandas as pd
import requests
import time
import json
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange

# ============================================================
# JUTT BOT PRO — BINANCE LIVE MARKET ANALYZER
# ============================================================

st.set_page_config(
    page_title="JUTT BOT PRO TRADER",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BINANCE_API = "https://api.binance.com"

PAIRS = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "LTCUSDT"
]

TIMEFRAMES = {
    "1 Minute (1m)": "1m",
    "3 Minutes (3m)": "3m",
    "5 Minutes (5m)": "5m",
    "15 Minutes (15m)": "15m",
    "30 Minutes (30m)": "30m",
    "1 Hour (1h)": "1h"
}

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 50% -15%, #222b23 0%, #0b1014 38%, #05070a 100%);
    color: white;
}

header,
#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
[data-testid="stDecoration"],
[data-testid="stHeader"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"],
[data-testid="stDeployButton"],
[data-testid="stAppDeployButton"],
.viewerBadge_container__1QSob,
[class*="viewerBadge"],
[class*="stFloating"],
[class*="stChatFloating"] {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    max-width: 1250px !important;
    padding-top: 12px !important;
    padding-bottom: 20px !important;
}

.hero {
    background:
        radial-gradient(circle at 50% 30%, rgba(255,193,7,.14), transparent 38%),
        linear-gradient(135deg,#141a1d,#070b0e);
    border: 1px solid #d0a326;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 0 30px rgba(255,193,7,.10);
}

.logo-row {
    display:flex;
    align-items:center;
    gap:16px;
}

.logo {
    width:86px;
    height:86px;
    border-radius:50%;
    border:2px solid #e8b72b;
    background:#080b0d;
    display:flex;
    align-items:center;
    justify-content:center;
    box-shadow:0 0 20px rgba(255,193,7,.20);
}

.logo svg {
    width:70px;
    height:70px;
}

.brand {
    font-size:34px;
    font-weight:900;
    letter-spacing:2px;
    line-height:1;
    background:linear-gradient(90deg,#ffd83d,#fff4a8,#d9a414);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.pro {
    color:#fff;
    font-size:13px;
    font-weight:800;
    letter-spacing:4px;
    margin-top:7px;
}

.tagline {
    color:#e9bd31;
    font-size:10px;
    font-weight:700;
    letter-spacing:2px;
    margin-top:7px;
}

.live-box {
    margin-left:auto;
    text-align:right;
    color:#ffc928;
    font-weight:800;
    font-size:14px;
}

.panel {
    background:linear-gradient(145deg,#151b20,#0d1217);
    border:1px solid #29343e;
    border-radius:17px;
    padding:16px;
    margin-bottom:14px;
}

.metric {
    background:#11171c;
    border:1px solid #29343e;
    border-radius:15px;
    padding:14px 8px;
    text-align:center;
    min-height:82px;
}

.metric-title {
    color:#8d98a4;
    font-size:11px;
    letter-spacing:1px;
}

.metric-value {
    color:#fff;
    font-size:20px;
    font-weight:800;
    margin-top:6px;
}

.green {
    color:#20e873 !important;
}

.red {
    color:#ff5362 !important;
}

.yellow {
    color:#ffc928 !important;
}

.signal-call {
    background:linear-gradient(135deg,#118d42,#20b950);
    border:1px solid #39f274;
    border-radius:17px;
    padding:18px;
    text-align:center;
    margin:15px 0;
    box-shadow:0 0 25px rgba(20,220,90,.15);
}

.signal-put {
    background:linear-gradient(135deg,#a91829,#df3042);
    border:1px solid #ff5969;
    border-radius:17px;
    padding:18px;
    text-align:center;
    margin:15px 0;
    box-shadow:0 0 25px rgba(230,30,60,.15);
}

.signal-wait {
    background:linear-gradient(135deg,#30343a,#171c21);
    border:1px solid #555d66;
    border-radius:17px;
    padding:18px;
    text-align:center;
    margin:15px 0;
}

.signal-title {
    color:#fff;
    font-size:24px;
    font-weight:900;
}

.signal-sub {
    color:#fff;
    font-size:13px;
    margin-top:5px;
}

div.stButton > button {
    height:52px;
    border-radius:14px;
    border:1px solid #e2b32b;
    background:linear-gradient(135deg,#f4bf22,#ffcf3b);
    color:#111 !important;
    font-weight:900;
    font-size:16px;
}

div[data-baseweb="select"] > div {
    background:#11171c !important;
    border-color:#303b45 !important;
    border-radius:12px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# BINANCE DATA
# ============================================================

@st.cache_data(ttl=1)
def get_price(symbol):

    try:
        response = requests.get(
            f"{BINANCE_API}/api/v3/ticker/price",
            params={"symbol": symbol},
            timeout=5
        )

        response.raise_for_status()

        return float(response.json()["price"])

    except Exception:
        return None


@st.cache_data(ttl=2)
def get_klines(symbol, interval, limit=200):

    try:

        response = requests.get(
            f"{BINANCE_API}/api/v3/klines",
            params={
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            },
            timeout=7
        )

        response.raise_for_status()

        rows = response.json()

        result = []

        for row in rows:

            result.append({
                "time": int(row[0]),
                "open": float(row[1]),
                "high": float(row[2]),
                "low": float(row[3]),
                "close": float(row[4]),
                "volume": float(row[5])
            })

        return pd.DataFrame(result)

    except Exception:
        return pd.DataFrame()


# ============================================================
# TECHNICAL ANALYSIS
# ============================================================

def analyze(df):

    if df.empty or len(df) < 50:
        return None

    x = df.copy()

    x["RSI"] = RSIIndicator(
        x["close"],
        window=14
    ).rsi()

    x["EMA9"] = EMAIndicator(
        x["close"],
        window=9
    ).ema_indicator()

    x["EMA21"] = EMAIndicator(
        x["close"],
        window=21
    ).ema_indicator()

    x["ATR"] = AverageTrueRange(
        x["high"],
        x["low"],
        x["close"],
        window=14
    ).average_true_range()

    # CLOSED candle
    current = -2
    previous = -3

    close_price = float(x["close"].iloc[current])
    rsi = float(x["RSI"].iloc[current])
    ema9 = float(x["EMA9"].iloc[current])
    ema21 = float(x["EMA21"].iloc[current])
    atr = float(x["ATR"].iloc[current])

    previous_ema9 = float(x["EMA9"].iloc[previous])
    previous_ema21 = float(x["EMA21"].iloc[previous])

    bullish_cross = (
        previous_ema9 <= previous_ema21
        and ema9 > ema21
    )

    bearish_cross = (
        previous_ema9 >= previous_ema21
        and ema9 < ema21
    )

    call_score = 0
    put_score = 0

    reasons = []

    # EMA TREND
    if ema9 > ema21:

        call_score += 30
        reasons.append("EMA 9 is above EMA 21.")

    elif ema9 < ema21:

        put_score += 30
        reasons.append("EMA 9 is below EMA 21.")

    # EMA CROSS
    if bullish_cross:

        call_score += 30
        reasons.append("Bullish EMA crossover confirmed.")

    if bearish_cross:

        put_score += 30
        reasons.append("Bearish EMA crossover confirmed.")

    # RSI
    if rsi < 35:

        call_score += 20
        reasons.append("RSI is oversold.")

    elif rsi > 65:

        put_score += 20
        reasons.append("RSI is overbought.")

    elif 45 <= rsi <= 58:

        call_score += 10

    elif 42 <= rsi <= 55:

        put_score += 10

    # CANDLE MOMENTUM
    candle_open = float(x["open"].iloc[current])
    candle_close = float(x["close"].iloc[current])

    if candle_close > candle_open:

        call_score += 10

    elif candle_close < candle_open:

        put_score += 10

    # SIGNAL
    if call_score >= 60 and call_score > put_score:

        signal = "CALL"
        confidence = min(call_score, 95)

    elif put_score >= 60 and put_score > call_score:

        signal = "PUT"
        confidence = min(put_score, 95)

    else:

        signal = "NO SIGNAL"
        confidence = max(call_score, put_score)

    if ema9 > ema21:
        trend = "BULLISH"
    elif ema9 < ema21:
        trend = "BEARISH"
    else:
        trend = "NEUTRAL"

    return {
        "signal": signal,
        "confidence": confidence,
        "price": close_price,
        "rsi": rsi,
        "ema9": ema9,
        "ema21": ema21,
        "atr": atr,
        "trend": trend,
        "reasons": reasons,
        "data": x
    }


# ============================================================
# HEADER / LOGO
# ============================================================

clock = datetime.now().strftime("%I:%M:%S %p")

st.markdown(f"""
<div class="hero">

<div class="logo-row">

<div class="logo">

<svg viewBox="0 0 100 100">

<circle cx="50" cy="50" r="42"
fill="none"
stroke="#e8b72b"
stroke-width="3"/>

<rect x="27" y="48" width="8" height="22"
rx="2" fill="#ffd54a"/>

<rect x="43" y="37" width="8" height="33"
rx="2" fill="#ffd54a"/>

<rect x="59" y="26" width="8" height="44"
rx="2" fill="#ffd54a"/>

<path d="M18 73 C34 59,43 63,53 51 C64 38,73 42,85 22"
fill="none"
stroke="#15ef63"
stroke-width="5"/>

<path d="M73 23 L87 20 L82 35"
fill="none"
stroke="#15ef63"
stroke-width="5"/>

</svg>

</div>

<div>

<div class="brand">JUTT BOT</div>

<div class="pro">
PRO TRADER
</div>

<div class="tagline">
ANALYZE &nbsp;|&nbsp; SIGNAL &nbsp;|&nbsp; TRADE &nbsp;|&nbsp; GROW
</div>

</div>

<div class="live-box">
🟢 LIVE MARKET<br>
{clock}
</div>

</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CONTROLS
# ============================================================

st.markdown('<div class="panel">', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:

    pair = st.selectbox(
        "📊 Pair / Asset",
        PAIRS
    )

with c2:

    timeframe_name = st.selectbox(
        "⏳ Timeframe",
        list(TIMEFRAMES.keys())
    )

timeframe = TIMEFRAMES[timeframe_name]

generate = st.button(
    "⚡ GENERATE AI SIGNAL",
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# LIVE DATA
# ============================================================

live_price = get_price(pair)

df = get_klines(
    pair,
    timeframe,
    200
)

result = analyze(df)


# ============================================================
# METRICS
# ============================================================

if result:

    rsi_value = result["rsi"]
    trend = result["trend"]

else:

    rsi_value = 0
    trend = "OFFLINE"


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.markdown("""
    <div class="metric">
        <div class="metric-title">LIVE FEED</div>
        <div class="metric-value green">
            ● CONNECTED
        </div>
    </div>
    """, unsafe_allow_html=True)


with m2:

    price_text = (
        f"${live_price:,.6f}"
        if live_price is not None
        else "OFFLINE"
    )

    st.markdown(f"""
    <div class="metric">
        <div class="metric-title">LIVE PRICE</div>
        <div class="metric-value">
            {price_text}
        </div>
    </div>
    """, unsafe_allow_html=True)


with m3:

    st.markdown(f"""
    <div class="metric">
        <div class="metric-title">RSI (14)</div>
        <div class="metric-value">
            {rsi_value:.2f}
        </div>
    </div>
    """, unsafe_allow_html=True)


with m4:

    if trend == "BULLISH":

        trend_html = '<span class="green">BULLISH 🟢</span>'

    elif trend == "BEARISH":

        trend_html = '<span class="red">BEARISH 🔴</span>'

    else:

        trend_html = '<span class="yellow">NEUTRAL 🟡</span>'

    st.markdown(f"""
    <div class="metric">
        <div class="metric-title">TREND</div>
        <div class="metric-value">
            {trend_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# GENERATE SIGNAL
# ============================================================

if generate and result:

    st.session_state["signal"] = result
    st.session_state["signal_pair"] = pair
    st.session_state["signal_tf"] = timeframe


signal_data = st.session_state.get("signal")

if signal_data:

    if (
        st.session_state.get("signal_pair") != pair
        or
        st.session_state.get("signal_tf") != timeframe
    ):
        signal_data = None


# ============================================================
# SIGNAL DISPLAY
# ============================================================

if signal_data:

    signal = signal_data["signal"]

    entry = (
        live_price
        if live_price is not None
        else signal_data["price"]
    )

    atr = signal_data["atr"]

    confidence = signal_data["confidence"]


    if signal == "CALL":

        sl = entry - (1.5 * atr)
        tp = entry + (2.5 * atr)

        st.markdown(f"""
        <div class="signal-call">

            <div class="signal-title">
                ▲ CALL [ {pair} — UP / HIGHER ]
            </div>

            <div class="signal-sub">
                Signal Confidence: {confidence}%
                &nbsp; | &nbsp;
                Expiry: {timeframe_name}
            </div>

        </div>
        """, unsafe_allow_html=True)

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "ENTRY",
                f"{entry:,.6f}"
            )

        with b:
            st.metric(
                "STOP LOSS",
                f"{sl:,.6f}"
            )

        with c:
            st.metric(
                "TAKE PROFIT",
                f"{tp:,.6f}"
            )


    elif signal == "PUT":

        sl = entry + (1.5 * atr)
        tp = entry - (2.5 * atr)

        st.markdown(f"""
        <div class="signal-put">

            <div class="signal-title">
                ▼ PUT [ {pair} — DOWN / LOWER ]
            </div>

            <div class="signal-sub">
                Signal Confidence: {confidence}%
                &nbsp; | &nbsp;
                Expiry: {timeframe_name}
            </div>

        </div>
        """, unsafe_allow_html=True)

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "ENTRY",
                f"{entry:,.6f}"
            )

        with b:
            st.metric(
                "STOP LOSS",
                f"{sl:,.6f}"
            )

        with c:
            st.metric(
                "TAKE PROFIT",
                f"{tp:,.6f}"
            )


    else:

        st.markdown(f"""
        <div class="signal-wait">

            <div class="signal-title">
                ⏳ NO CLEAR SETUP — WAIT
            </div>

            <div class="signal-sub">
                {pair} • {timeframe_name}
            </div>

        </div>
        """, unsafe_allow_html=True)


else:

    st.markdown(f"""
    <div class="signal-wait">

        <div class="signal-title">
            ⚡ GENERATE AI SIGNAL
        </div>

        <div class="signal-sub">
            {pair} • {timeframe_name}
            &nbsp; | &nbsp;
            Binance Live Market
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TECHNICAL ANALYSIS
# ============================================================

if result:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        "### 🧠 JUTT BOT TECHNICAL ANALYSIS"
    )

    for reason in result["reasons"]:

        st.write("•", reason)

    st.markdown(
        f"""
        **EMA 9:** `{result["ema9"]:.6f}`  
        **EMA 21:** `{result["ema21"]:.6f}`  
        **ATR:** `{result["atr"]:.6f}`
        """
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# BINANCE LIVE CANDLE CHART
# ============================================================

if not df.empty:

    chart_df = df.tail(80).copy()

    candles = []

    volumes = []

    for _, row in chart_df.iterrows():

        candles.append({
            "time": int(row["time"] / 1000),
            "open": float(row["open"]),
            "high": float(row["high"]),
            "low": float(row["low"]),
            "close": float(row["close"])
        })

        volumes.append({
            "time": int(row["time"] / 1000),
            "value": float(row["volume"]),
            "color": (
                "#16c784"
                if row["close"] >= row["open"]
                else "#ef4056"
            )
        })

    candles_json = json.dumps(candles)
    volumes_json = json.dumps(volumes)

    chart = f"""

    <div style="
        background:#090d11;
        border:1px solid #29343e;
        border-radius:17px;
        padding:8px;
    ">

        <div style="
            color:#d8dee5;
            padding:8px 12px;
            font-size:13px;
            font-weight:700;
        ">
            📈 {pair} • {timeframe_name} • BINANCE LIVE MARKET
        </div>

        <div id="chart" style="width:100%;height:440px;"></div>

    </div>

    <script src="https://cdn.jsdelivr.net/npm/lightweight-charts@4.2.0/dist/lightweight-charts.standalone.production.min.js"></script>

    <script>

    const data = {candles_json};
    const volumeData = {volumes_json};

    const container = document.getElementById("chart");

    const chart = LightweightCharts.createChart(
        container,
        {{
            width: container.clientWidth,
            height: 430,

            layout: {{
                background: {{ color: "#090d11" }},
                textColor: "#9ba5af"
            }},

            grid: {{
                vertLines: {{ color: "#182028" }},
                horzLines: {{ color: "#182028" }}
            }},

            rightPriceScale: {{
                borderColor: "#33404b"
            }},

            timeScale: {{
                borderColor: "#33404b",
                timeVisible: true,
                secondsVisible: false
            }},

            crosshair: {{
                mode: 0
            }}
        }}
    );

    const candleSeries = chart.addCandlestickSeries({{
        upColor: "#16c784",
        downColor: "#ef4056",
        borderUpColor: "#16c784",
        borderDownColor: "#ef4056",
        wickUpColor: "#16c784",
        wickDownColor: "#ef4056"
    }});

    candleSeries.setData(data);

    const volumeSeries = chart.addHistogramSeries({{
        priceFormat: {{
            type: "volume"
        }},
        priceScaleId: ""
    }});

    volumeSeries.priceScale().applyOptions({{
        scaleMargins: {{
            top: 0.82,
            bottom: 0
        }}
    }});

    volumeSeries.setData(volumeData);

    chart.timeScale().fitContent();

    window.addEventListener("resize", function() {{
        chart.applyOptions({{
            width: container.clientWidth
        }});
    }});

    </script>
    """

    st.components.v1.html(
        chart,
        height=470,
        scrolling=False
    )


# ============================================================
# LIVE MARKET TABLE
# ============================================================

st.markdown('<div class="panel">', unsafe_allow_html=True)

st.markdown(
    "### 📊 LIVE MARKET DATA"
)

if not df.empty:

    table = df.tail(12).copy()

    table["TIME"] = pd.to_datetime(
        table["time"],
        unit="ms"
    ).dt.strftime("%H:%M:%S")

    table["OPEN"] = table["open"].map(
        lambda x: f"{x:,.6f}"
    )

    table["HIGH"] = table["high"].map(
        lambda x: f"{x:,.6f}"
    )

    table["LOW"] = table["low"].map(
        lambda x: f"{x:,.6f}"
    )

    table["CLOSE"] = table["close"].map(
        lambda x: f"{x:,.6f}"
    )

    table["VOLUME"] = table["volume"].map(
        lambda x: f"{x:,.2f}"
    )

    table = table[
        [
            "TIME",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "VOLUME"
        ]
    ]

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

else:

    st.error(
        "Binance live market data connection failed."
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div style="
text-align:center;
padding:18px;
color:#68727d;
font-size:10px;
letter-spacing:2px;
">
JUTT BOT PRO • ANALYZE | SIGNAL | TRADE | GROW
</div>
""", unsafe_allow_html=True)


# ============================================================
# AUTO REFRESH
# ============================================================

time.sleep(2)
st.rerun()
