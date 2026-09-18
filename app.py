import streamlit as st
import pandas as pd
import requests
import json
import os
import base64
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="JUTT BOT PRO TRADER",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CONFIG
# ============================================================

BINANCE_HOSTS = [
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com"
]

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

PAIR_NAMES = {
    "BTCUSDT": "BTCUSDT (Bitcoin)",
    "ETHUSDT": "ETHUSDT (Ethereum)",
    "SOLUSDT": "SOLUSDT (Solana)",
    "BNBUSDT": "BNBUSDT (BNB)",
    "XRPUSDT": "XRPUSDT (XRP)",
    "ADAUSDT": "ADAUSDT (Cardano)",
    "DOGEUSDT": "DOGEUSDT (Dogecoin)",
    "AVAXUSDT": "AVAXUSDT (Avalanche)",
    "LINKUSDT": "LINKUSDT (Chainlink)",
    "LTCUSDT": "LTCUSDT (Litecoin)"
}

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

@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background:
    radial-gradient(
        circle at 50% -15%,
        #1d2920 0%,
        #0a0f13 38%,
        #05070a 78%
    );
    color:#fff !important;
}

/* REMOVE STREAMLIT UI */

header,
footer,
#MainMenu,
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
[class*="stChatFloating"],
[class*="stActionButton"] {
    display:none !important;
    visibility:hidden !important;
    opacity:0 !important;
    pointer-events:none !important;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 12px !important;
    padding-bottom: 20px !important;
}

/* ============================================================
HEADER
============================================================ */

.hero {
    position:relative;
    overflow:hidden;

    min-height:220px;

    background:
    radial-gradient(
        circle at 52% 45%,
        rgba(255,200,40,.15),
        transparent 34%
    ),
    linear-gradient(
        120deg,
        #05080b,
        #10171a,
        #080c0f
    );

    border:2px solid #d6aa2c;
    border-radius:22px;

    padding:22px;

    margin-bottom:14px;

    box-shadow:
    0 0 35px rgba(255,193,7,.13),
    inset 0 0 40px rgba(255,193,7,.025);
}

.hero-grid {
    display:grid;
    grid-template-columns:240px 1fr 180px;
    gap:20px;
    align-items:center;
    min-height:175px;
}

/* LOGO */

.logo-box {
    width:210px;
    height:175px;
    display:flex;
    justify-content:center;
    align-items:center;
}

.logo-box img {
    width:100%;
    height:100%;
    object-fit:contain;
    border-radius:20px;
}

/* BRAND */

.brand-area {
    text-align:center;
}

.brand-main {
    color:#ffd338;
    font-size:55px;
    font-weight:900;
    letter-spacing:3px;
    line-height:1;
    text-shadow:0 0 18px rgba(255,193,7,.20);
}

.brand-pro {
    color:#ffffff;
    font-size:23px;
    font-weight:800;
    letter-spacing:7px;
    margin-top:8px;
}

.brand-tag {
    color:#ffd02f;
    font-size:15px;
    font-weight:800;
    letter-spacing:4px;
    margin-top:13px;
}

.brand-sub {
    color:#9faab5;
    font-size:11px;
    letter-spacing:3px;
    margin-top:10px;
}

/* LIVE */

.live-card {
    background:#10171c;
    border:1px solid #394650;
    border-radius:16px;
    padding:17px;
    text-align:center;
}

.live-title {
    color:#a9b2bc;
    font-size:13px;
}

.live-dot {
    color:#16e96d;
    font-size:20px;
}

.live-time {
    color:#ffd02f;
    font-size:20px;
    font-weight:900;
    margin-top:7px;
}

/* ============================================================
PANELS
============================================================ */

.panel {
    background:
    linear-gradient(
        145deg,
        #10171d,
        #090e13
    );

    border:1px solid #303b45;
    border-radius:17px;

    padding:16px;

    margin-bottom:14px;

    box-shadow:
    0 5px 20px rgba(0,0,0,.20);
}

/* ============================================================
SELECT
============================================================ */

label {
    color:#aab4bf !important;
    font-weight:600 !important;
}

div[data-baseweb="select"] > div {
    background:#10171d !important;
    border:1px solid #34414c !important;
    border-radius:12px !important;
    color:#fff !important;
}

div[data-baseweb="select"] span {
    color:#fff !important;
}

/* ============================================================
BUTTON
============================================================ */

div.stButton > button {
    height:58px;

    background:
    linear-gradient(
        135deg,
        #f2ba1d,
        #ffd33d
    );

    border:1px solid #ffe47d;
    border-radius:15px;

    color:#090909 !important;

    font-size:20px;
    font-weight:900;

    box-shadow:
    0 0 25px rgba(255,193,7,.15);
}

/* ============================================================
METRICS
============================================================ */

.metric-card {
    background:
    linear-gradient(
        145deg,
        #11191f,
        #0b1015
    );

    border:1px solid #303c47;
    border-radius:16px;

    min-height:108px;

    padding:15px 8px;

    text-align:center;
}

.metric-title {
    color:#8f9aa5;
    font-size:12px;
    letter-spacing:1px;
}

.metric-value {
    color:#fff;
    font-size:22px;
    font-weight:900;
    margin-top:8px;
}

.green {
    color:#20e875 !important;
}

.red {
    color:#ff5261 !important;
}

.yellow {
    color:#ffd02f !important;
}

/* ============================================================
SIGNAL
============================================================ */

.signal-call {
    background:
    linear-gradient(
        135deg,
        #087d38,
        #20b953
    );

    border:2px solid #29f66e;

    border-radius:18px;

    padding:19px;

    text-align:center;

    margin:15px 0;

    box-shadow:
    0 0 25px rgba(20,220,90,.14);
}

.signal-put {
    background:
    linear-gradient(
        135deg,
        #981727,
        #dc3043
    );

    border:2px solid #ff5969;

    border-radius:18px;

    padding:19px;

    text-align:center;

    margin:15px 0;
}

.signal-neutral {
    background:
    linear-gradient(
        135deg,
        #242b31,
        #12181d
    );

    border:1px solid #56616b;

    border-radius:18px;

    padding:19px;

    text-align:center;

    margin:15px 0;
}

.signal-title {
    color:#fff;
    font-size:27px;
    font-weight:900;
}

.signal-sub {
    color:#fff;
    font-size:14px;
    margin-top:6px;
}

/* ============================================================
CHART
============================================================ */

.chart-panel {
    background:#080d12;
    border:1px solid #2d3943;
    border-radius:17px;
    padding:10px;
    margin-bottom:14px;
}

.chart-heading {
    color:#dce3e8;
    font-size:15px;
    font-weight:800;
    padding:8px;
}

/* ============================================================
RECENT SIGNALS
============================================================ */

.recent-title {
    color:#e5ebef;
    font-size:16px;
    font-weight:900;
}

.footer {
    text-align:center;
    color:#65717c;
    font-size:10px;
    letter-spacing:3px;
    padding:18px;
}

/* MOBILE */

@media(max-width:900px) {

    .hero-grid {
        grid-template-columns:1fr;
        text-align:center;
    }

    .logo-box {
        margin:auto;
        width:170px;
        height:140px;
    }

    .brand-main {
        font-size:40px;
    }

    .brand-pro {
        font-size:17px;
    }

    .brand-tag {
        font-size:10px;
    }

    .live-card {
        width:180px;
        margin:auto;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# BINANCE API
# ============================================================

def binance_request(endpoint, params):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    for host in BINANCE_HOSTS:

        try:

            r = requests.get(
                host + endpoint,
                params=params,
                headers=headers,
                timeout=7
            )

            if r.status_code == 200:
                return r.json()

        except Exception:
            continue

    return None


# ============================================================
# LIVE PRICE
# ============================================================

@st.cache_data(ttl=1)
def get_live_price(symbol):

    data = binance_request(
        "/api/v3/ticker/price",
        {"symbol":symbol}
    )

    if data and "price" in data:
        return float(data["price"])

    return None


# ============================================================
# 24H CHANGE
# ============================================================

@st.cache_data(ttl=2)
def get_24h(symbol):

    data = binance_request(
        "/api/v3/ticker/24hr",
        {"symbol":symbol}
    )

    if data:

        return (
            float(data.get("priceChange",0)),
            float(data.get("priceChangePercent",0))
        )

    return 0,0


# ============================================================
# CANDLES
# ============================================================

@st.cache_data(ttl=2)
def get_candles(symbol, interval):

    data = binance_request(
        "/api/v3/klines",
        {
            "symbol":symbol,
            "interval":interval,
            "limit":200
        }
    )

    if not data:
        return pd.DataFrame()

    rows=[]

    for c in data:

        rows.append({

            "time":int(c[0]),

            "open":float(c[1]),

            "high":float(c[2]),

            "low":float(c[3]),

            "close":float(c[4]),

            "volume":float(c[5])

        })

    return pd.DataFrame(rows)


# ============================================================
# TECHNICAL ANALYSIS
# ============================================================

def analyze_market(df):

    if df.empty or len(df)<50:
        return None

    x=df.copy()

    x["RSI"]=RSIIndicator(
        x["close"],
        window=14
    ).rsi()

    x["EMA9"]=EMAIndicator(
        x["close"],
        window=9
    ).ema_indicator()

    x["EMA21"]=EMAIndicator(
        x["close"],
        window=21
    ).ema_indicator()

    x["ATR"]=AverageTrueRange(
        x["high"],
        x["low"],
        x["close"],
        window=14
    ).average_true_range()

    # CLOSED CANDLE
    i=-2
    p=-3

    price=float(x["close"].iloc[i])
    rsi=float(x["RSI"].iloc[i])

    ema9=float(x["EMA9"].iloc[i])
    ema21=float(x["EMA21"].iloc[i])

    prev9=float(x["EMA9"].iloc[p])
    prev21=float(x["EMA21"].iloc[p])

    atr=float(x["ATR"].iloc[i])

    call_score=0
    put_score=0

    reasons=[]

    # EMA
    if ema9>ema21:

        call_score+=30
        reasons.append("EMA 9 is above EMA 21")

    elif ema9<ema21:

        put_score+=30
        reasons.append("EMA 9 is below EMA 21")

    # CROSS
    if prev9<=prev21 and ema9>ema21:

        call_score+=30
        reasons.append("Bullish EMA crossover")

    if prev9>=prev21 and ema9<ema21:

        put_score+=30
        reasons.append("Bearish EMA crossover")

    # RSI
    if rsi<35:

        call_score+=20
        reasons.append("RSI is in oversold zone")

    elif rsi>65:

        put_score+=20
        reasons.append("RSI is in overbought zone")

    # CANDLE MOMENTUM
    candle_open=float(x["open"].iloc[i])
    candle_close=float(x["close"].iloc[i])

    if candle_close>candle_open:

        call_score+=10

    elif candle_close<candle_open:

        put_score+=10

    # SIGNAL
    if call_score>=60 and call_score>put_score:

        signal="CALL"
        confidence=min(call_score,95)

    elif put_score>=60 and put_score>call_score:

        signal="PUT"
        confidence=min(put_score,95)

    else:

        signal="NO SIGNAL"
        confidence=max(call_score,put_score)

    # TREND
    if ema9>ema21:
        trend="BULLISH"

    elif ema9<ema21:
        trend="BEARISH"

    else:
        trend="NEUTRAL"

    return {
        "signal":signal,
        "confidence":confidence,
        "price":price,
        "rsi":rsi,
        "ema9":ema9,
        "ema21":ema21,
        "atr":atr,
        "trend":trend,
        "reasons":reasons
    }


# ============================================================
# LOGO
# ============================================================

logo_path="jutt_bot_logo.png"

if os.path.exists(logo_path):

    with open(logo_path,"rb") as f:

        logo_b64=base64.b64encode(
            f.read()
        ).decode()

    logo_html=f"""
    <img src="data:image/png;base64,{logo_b64}">
    """

else:

    logo_html="""
    <div style="
        color:#ffd338;
        font-size:45px;
        font-weight:900;
        text-align:center;
    ">
        ⭐
    </div>
    """


# ============================================================
# HEADER
# ============================================================

clock=datetime.now().strftime("%I:%M:%S %p")

st.markdown(f"""

<div class="hero">

    <div class="hero-grid">

        <div class="logo-box">
            {logo_html}
        </div>

        <div class="brand-area">

            <div class="brand-main">
                JUTT BOT
            </div>

            <div class="brand-pro">
                PRO TRADER
            </div>

            <div class="brand-tag">
                ANALYZE &nbsp;|&nbsp;
                SIGNAL &nbsp;|&nbsp;
                TRADE &nbsp;|&nbsp;
                GROW
            </div>

            <div class="brand-sub">
                DISCIPLINE TODAY &nbsp; • &nbsp;
                BIGGER TOMORROW
            </div>

        </div>

        <div class="live-card">

            <div class="live-title">
                <span class="live-dot">●</span>
                LIVE MARKET
            </div>

            <div class="live-time">
                {clock}
            </div>

        </div>

    </div>

</div>

""",unsafe_allow_html=True)


# ============================================================
# CONTROLS
# ============================================================

st.markdown(
    '<div class="panel">',
    unsafe_allow_html=True
)

c1,c2=st.columns(2)

with c1:

    pair=st.selectbox(
        "📊 Pair / Asset",
        PAIRS,
        format_func=lambda x:PAIR_NAMES[x]
    )

with c2:

    timeframe_name=st.selectbox(
        "⏳ Expiry Time",
        list(TIMEFRAMES.keys())
    )

timeframe=TIMEFRAMES[timeframe_name]

generate=st.button(
    "⚡ GENERATE AI SIGNAL",
    use_container_width=True
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# MARKET DATA
# ============================================================

live_price=get_live_price(pair)

change,change_percent=get_24h(pair)

df=get_candles(
    pair,
    timeframe
)

analysis=analyze_market(df)


# ============================================================
# METRICS
# ============================================================

if analysis:

    rsi=analysis["rsi"]
    trend=analysis["trend"]

else:

    rsi=0
    trend="OFFLINE"

connected=(
    live_price is not None
    and not df.empty
)

m1,m2,m3,m4=st.columns(4)


# LIVE FEED

with m1:

    status="CONNECTED" if connected else "OFFLINE"

    cls="green" if connected else "red"

    st.markdown(f"""

    <div class="metric-card">

        <div class="metric-title">
            LIVE FEED
        </div>

        <div class="metric-value {cls}">
            ● {status}
        </div>

    </div>

    """,unsafe_allow_html=True)


# PRICE

with m2:

    price_text=(
        f"${live_price:,.2f}"
        if live_price is not None
        else "--"
    )

    change_cls="green" if change_percent>=0 else "red"

    st.markdown(f"""

    <div class="metric-card">

        <div class="metric-title">
            LIVE PRICE
        </div>

        <div class="metric-value">
            {price_text}
        </div>

        <div class="{change_cls}">
            {change:+,.2f}
            &nbsp;
            ({change_percent:+.2f}%)
        </div>

    </div>

    """,unsafe_allow_html=True)


# RSI

with m3:

    st.markdown(f"""

    <div class="metric-card">

        <div class="metric-title">
            RSI (14)
        </div>

        <div class="metric-value">
            {rsi:.2f}
        </div>

    </div>

    """,unsafe_allow_html=True)


# TREND

with m4:

    if trend=="BULLISH":

        trend_html="""
        <span class="green">
            BULLISH 🟢
        </span>
        """

    elif trend=="BEARISH":

        trend_html="""
        <span class="red">
            BEARISH 🔴
        </span>
        """

    else:

        trend_html="""
        <span class="yellow">
            NEUTRAL 🟡
        </span>
        """

    st.markdown(f"""

    <div class="metric-card">

        <div class="metric-title">
            TREND
        </div>

        <div class="metric-value">
            {trend_html}
        </div>

    </div>

    """,unsafe_allow_html=True)


# ============================================================
# GENERATE SIGNAL
# ============================================================

if generate:

    if analysis:

        st.session_state["signal_data"]=analysis
        st.session_state["signal_pair"]=pair
        st.session_state["signal_tf"]=timeframe

    else:

        st.error(
            "Binance live market data is unavailable."
        )


signal_data=st.session_state.get(
    "signal_data"
)

if signal_data:

    if (
        st.session_state.get("signal_pair") != pair
        or
        st.session_state.get("signal_tf") != timeframe
    ):

        signal_data=None


# ============================================================
# SIGNAL CARD
# ============================================================

if signal_data:

    signal=signal_data["signal"]

    entry=(
        live_price
        if live_price is not None
        else signal_data["price"]
    )

    confidence=signal_data["confidence"]

    atr=signal_data["atr"]


    if signal=="CALL":

        sl=entry-(1.5*atr)
        tp=entry+(2.5*atr)

        st.markdown(f"""

        <div class="signal-call">

            <div class="signal-title">
                ▲ CALL ▲
                [ {pair} — UP / HIGHER ]
            </div>

            <div class="signal-sub">
                Technical Signal Strength:
                {confidence}%
                &nbsp; | &nbsp;
                Timeframe: {timeframe_name}
            </div>

        </div>

        """,unsafe_allow_html=True)

        a,b,c=st.columns(3)

        with a:
            st.metric(
                "ENTRY",
                f"{entry:,.2f}"
            )

        with b:
            st.metric(
                "STOP LOSS",
                f"{sl:,.2f}"
            )

        with c:
            st.metric(
                "TAKE PROFIT",
                f"{tp:,.2f}"
            )


    elif signal=="PUT":

        sl=entry+(1.5*atr)
        tp=entry-(2.5*atr)

        st.markdown(f"""

        <div class="signal-put">

            <div class="signal-title">
                ▼ PUT ▼
                [ {pair} — DOWN / LOWER ]
            </div>

            <div class="signal-sub">
                Technical Signal Strength:
                {confidence}%
                &nbsp; | &nbsp;
                Timeframe: {timeframe_name}
            </div>

        </div>

        """,unsafe_allow_html=True)

        a,b,c=st.columns(3)

        with a:
            st.metric(
                "ENTRY",
                f"{entry:,.2f}"
            )

        with b:
            st.metric(
                "STOP LOSS",
                f"{sl:,.2f}"
            )

        with c:
            st.metric(
                "TAKE PROFIT",
                f"{tp:,.2f}"
            )


    else:

        st.markdown(f"""

        <div class="signal-neutral">

            <div class="signal-title">
                ⏳ NO CLEAR SETUP — WAIT
            </div>

            <div class="signal-sub">
                {pair} • {timeframe_name}
            </div>

        </div>

        """,unsafe_allow_html=True)


else:

    st.markdown(f"""

    <div class="signal-neutral">

        <div class="signal-title">
            ⚡ GENERATE AI SIGNAL
        </div>

        <div class="signal-sub">
            {pair} • {timeframe_name}
            • Binance Live Market
        </div>

    </div>

    """,unsafe_allow_html=True)


# ============================================================
# LIVE CHART
# ============================================================

if not df.empty:

    chart_df=df.tail(80).copy()

    candle_data=[]

    volume_data=[]

    for _,row in chart_df.iterrows():

        candle_data.append({

            "time":int(row["time"]/1000),

            "open":float(row["open"]),

            "high":float(row["high"]),

            "low":float(row["low"]),

            "close":float(row["close"])

        })

        volume_data.append({

            "time":int(row["time"]/1000),

            "value":float(row["volume"]),

            "color":
            "#16c784"
            if row["close"]>=row["open"]
            else "#ef4056"

        })

    candle_json=json.dumps(candle_data)

    volume_json=json.dumps(volume_data)

    chart_html=f"""

    <div class="chart-panel">

        <div class="chart-heading">
            ₿ {pair} • {timeframe_name}
            • Binance Live Market
        </div>

        <div id="chart"
             style="width:100%;height:470px;">
        </div>

    </div>

    <script src="
    https://cdn.jsdelivr.net/npm/lightweight-charts@4.2.0/dist/lightweight-charts.standalone.production.min.js
    "></script>

    <script>

    const candleData={candle_json};

    const volumeData={volume_json};

    const container=
        document.getElementById("chart");

    const chart=
        LightweightCharts.createChart(
            container,
            {{

                width:container.clientWidth,

                height:455,

                layout:{{
                    background:{{color:"#080d12"}},
                    textColor:"#aab4bf"
                }},

                grid:{{
                    vertLines:{{color:"#182128"}},
                    horzLines:{{color:"#182128"}}
                }},

                rightPriceScale:{{
                    borderColor:"#34414b"
                }},

                timeScale:{{
                    borderColor:"#34414b",
                    timeVisible:true,
                    secondsVisible:false
                }}

            }}
        );

    const candles=
        chart.addCandlestickSeries({{

            upColor:"#16c784",

            downColor:"#ef4056",

            borderUpColor:"#16c784",

            borderDownColor:"#ef4056",

            wickUpColor:"#16c784",

            wickDownColor:"#ef4056"

        }});

    candles.setData(candleData);


    const volume=
        chart.addHistogramSeries({{

            priceFormat:{{
                type:"volume"
            }},

            priceScaleId:""

        }});


    volume.priceScale().applyOptions({{

        scaleMargins:{{
            top:0.78,
            bottom:0
        }}

    }});


    volume.setData(volumeData);

    chart.timeScale().fitContent();


    window.addEventListener(
        "resize",
        function(){{
            chart.applyOptions({{
                width:container.clientWidth
            }});
        }}
    );

    </script>

    """

    st.components.v1.html(
        chart_html,
        height=485,
        scrolling=False
    )


# ============================================================
# RECENT SIGNALS
# ============================================================

st.markdown(
    '<div class="panel">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="recent-title">📋 RECENT SIGNALS</div>',
    unsafe_allow_html=True
)

if "recent_signals" not in st.session_state:

    st.session_state.recent_signals=[]


if generate and signal_data:

    new_signal={

        "TIME":
        datetime.now().strftime("%H:%M:%S"),

        "PAIR":
        pair,

        "SIGNAL":
        signal_data["signal"],

        "PRICE":
        signal_data["price"],

        "STRENGTH":
        f"{signal_data['confidence']}%"

    }

    st.session_state.recent_signals.insert(
        0,
        new_signal
    )

    st.session_state.recent_signals=\
        st.session_state.recent_signals[:10]


if st.session_state.recent_signals:

    recent_df=pd.DataFrame(
        st.session_state.recent_signals
    )

    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No signals generated yet."
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# TECHNICAL ANALYSIS
# ============================================================

if analysis:

    st.markdown(
        '<div class="panel">',
        unsafe_allow_html=True
    )

    st.markdown(
        "### 🧠 JUTT BOT TECHNICAL ANALYSIS"
    )

    for reason in analysis["reasons"]:

        st.write(
            "•",
            reason
        )

    st.write(
        f"EMA 9: `{analysis['ema9']:.6f}`  |  "
        f"EMA 21: `{analysis['ema21']:.6f}`  |  "
        f"ATR: `{analysis['atr']:.6f}`"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    JUTT BOT PRO • ANALYZE | SIGNAL | TRADE | GROW
</div>
""", unsafe_allow_html=True)
