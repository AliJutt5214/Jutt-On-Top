import os
import json
import time
import urllib.request
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# JUTT BOT PRO — LIVE MARKET TERMINAL
# ============================================================
# Firebase removed.
# No fake/random prices.
# No fake accuracy.
#
# Set your REAL/AUTHORIZED market feed in:
#
# MARKET_FEED_URL
#
# Expected JSON:
#
# {
#   "pair": "NZD/CHF (OTC)",
#   "price": 0.12345,
#   "timestamp": 1760000000000,
#   "candles": [
#       {
#           "time": 1760000000000,
#           "open": 0.12340,
#           "high": 0.12350,
#           "low": 0.12335,
#           "close": 0.12345
#       }
#   ]
# }
#
# ============================================================


st.set_page_config(
    page_title="JUTT BOT PRO — Live Market Terminal",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CONFIG
# ============================================================

MARKET_FEED_URL = os.getenv("MARKET_FEED_URL", "").strip()

PAIRS = [
    "NZD/CHF (OTC)",
    "USD/INR (OTC)",
    "NZD/JPY (OTC)",
    "USD/COP (OTC)",
    "USD/IDR (OTC)",
    "EUR/GBP",
    "USD/PHP (OTC)",
    "NZD/CAD (OTC)",
    "EUR/NZD (OTC)",
    "USD/BRL (OTC)",
    "CAD/JPY",
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "AUD/USD",
    "USD/CAD",
]


EXPIRIES = {
    "5 Seconds": 5,
    "10 Seconds": 10,
    "15 Seconds": 15,
    "30 Seconds": 30,
    "1 Minute": 60,
    "2 Minutes": 120,
    "5 Minutes": 300,
}


# ============================================================
# HIDE STREAMLIT UI
# ============================================================

hide_streamlit_style = """
<style>

#MainMenu,
footer,
header,
.stDeployButton,
[data-testid="stStatusWidget"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
.viewerBadge_container__1QSob,
a[href*="streamlit.io"],
div[class*="viewerBadge"] {
    display:none !important;
    visibility:hidden !important;
}

.block-container {
    padding:0 !important;
    max-width:100% !important;
}

</style>
"""

st.markdown(
    hide_streamlit_style,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "pair" not in st.session_state:
    st.session_state.pair = PAIRS[0]

if "expiry" not in st.session_state:
    st.session_state.expiry = 30

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# LIVE FEED
# ============================================================

def get_live_feed(pair):

    if not MARKET_FEED_URL:

        return None, "LIVE MARKET FEED NOT CONFIGURED"

    try:

        separator = "&" if "?" in MARKET_FEED_URL else "?"

        url = (
            MARKET_FEED_URL
            + separator
            + "pair="
            + quote(pair)
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "JUTT-BOT-PRO/1.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=5
        ) as response:

            raw = response.read().decode("utf-8")

        data = json.loads(raw)

        if not isinstance(data, dict):

            return None, "INVALID FEED RESPONSE"

        price = data.get("price")

        if price is None:

            return None, "PRICE NOT RECEIVED"

        price = float(price)

        candles = data.get("candles", [])

        clean_candles = []

        if isinstance(candles, list):

            for candle in candles:

                try:

                    clean_candles.append({

                        "time": float(
                            candle.get(
                                "time",
                                0
                            )
                        ),

                        "open": float(
                            candle["open"]
                        ),

                        "high": float(
                            candle["high"]
                        ),

                        "low": float(
                            candle["low"]
                        ),

                        "close": float(
                            candle["close"]
                        )

                    })

                except (
                    KeyError,
                    TypeError,
                    ValueError
                ):

                    continue

        if len(clean_candles) < 20:

            return None, (
                "AT LEAST 20 LIVE CANDLES "
                "ARE REQUIRED"
            )

        return {

            "pair": str(
                data.get(
                    "pair",
                    pair
                )
            ),

            "price": price,

            "timestamp": data.get(
                "timestamp",
                int(time.time() * 1000)
            ),

            "candles": clean_candles

        }, None

    except Exception as error:

        return None, (
            "LIVE FEED ERROR: "
            + str(error)
        )


# ============================================================
# RSI
# ============================================================

def calculate_rsi(
    closes,
    period=14
):

    if len(closes) < period + 1:

        return None

    gains = []
    losses = []

    start = len(closes) - period

    for i in range(
        start,
        len(closes)
    ):

        difference = (
            closes[i]
            - closes[i - 1]
        )

        if difference >= 0:

            gains.append(
                difference
            )

            losses.append(0)

        else:

            gains.append(0)

            losses.append(
                abs(difference)
            )

    average_gain = (
        sum(gains) / period
    )

    average_loss = (
        sum(losses) / period
    )

    if average_loss == 0:

        return 100.0

    relative_strength = (
        average_gain
        / average_loss
    )

    value = (
        100
        - (
            100
            / (
                1
                + relative_strength
            )
        )
    )

    return round(value, 1)


# ============================================================
# EMA
# ============================================================

def calculate_ema(
    values,
    period
):

    if len(values) < period:

        return None

    multiplier = (
        2 / (period + 1)
    )

    ema_value = (
        sum(values[:period])
        / period
    )

    for value in values[period:]:

        ema_value = (
            (
                value
                - ema_value
            )
            * multiplier
        ) + ema_value

    return ema_value


# ============================================================
# ATR
# ============================================================

def calculate_atr(
    candles,
    period=14
):

    if len(candles) < period + 1:

        return None

    true_ranges = []

    for i in range(
        1,
        len(candles)
    ):

        current = candles[i]

        previous_close = (
            candles[i - 1]["close"]
        )

        true_range = max(

            current["high"]
            - current["low"],

            abs(
                current["high"]
                - previous_close
            ),

            abs(
                current["low"]
                - previous_close
            )

        )

        true_ranges.append(
            true_range
        )

    return (
        sum(
            true_ranges[-period:]
        )
        / period
    )


# ============================================================
# MARKET ANALYSIS
# ============================================================

def analyze_market(candles):

    closes = [
        candle["close"]
        for candle in candles
    ]

    if len(closes) < 22:

        return {

            "signal": "WAIT",

            "confidence": 0,

            "rsi": None,

            "trend": "WAITING",

            "reason": (
                "Not enough live candles."
            ),

            "price": (
                closes[-1]
                if closes
                else None
            )

        }

    current_price = closes[-1]

    previous_price = closes[-2]

    rsi_value = calculate_rsi(
        closes
    )

    ema9 = calculate_ema(
        closes,
        9
    )

    ema21 = calculate_ema(
        closes,
        21
    )

    atr_value = calculate_atr(
        candles
    )

    score = 0

    reasons = []

    # --------------------------------------------------------
    # TREND
    # --------------------------------------------------------

    if ema9 > ema21:

        score += 2

        trend = "BULLISH"

        reasons.append(
            "EMA9 above EMA21"
        )

    elif ema9 < ema21:

        score -= 2

        trend = "BEARISH"

        reasons.append(
            "EMA9 below EMA21"
        )

    else:

        trend = "SIDEWAYS"


    # --------------------------------------------------------
    # RSI
    # --------------------------------------------------------

    if rsi_value < 30:

        score += 1

        reasons.append(
            "RSI oversold"
        )

    elif rsi_value > 70:

        score -= 1

        reasons.append(
            "RSI overbought"
        )

    elif (
        50 <= rsi_value <= 65
        and current_price > previous_price
    ):

        score += 1

        reasons.append(
            "RSI supports upward momentum"
        )

    elif (
        35 <= rsi_value <= 50
        and current_price < previous_price
    ):

        score -= 1

        reasons.append(
            "RSI supports downward momentum"
        )


    # --------------------------------------------------------
    # MOMENTUM
    # --------------------------------------------------------

    lookback = min(
        5,
        len(closes) - 1
    )

    momentum = (
        closes[-1]
        - closes[
            -1 - lookback
        ]
    )

    if momentum > 0:

        score += 1

        reasons.append(
            "Positive short momentum"
        )

    elif momentum < 0:

        score -= 1

        reasons.append(
            "Negative short momentum"
        )


    # --------------------------------------------------------
    # SIGNAL
    # --------------------------------------------------------

    if score >= 4:

        signal = "CALL"

        confidence = min(
            95,
            60 + abs(score) * 6
        )

    elif score <= -4:

        signal = "PUT"

        confidence = min(
            95,
            60 + abs(score) * 6
        )

    else:

        signal = "WAIT"

        confidence = min(
            59,
            50 + abs(score) * 3
        )


    if not reasons:

        reason = (
            "No strong market confluence."
        )

    else:

        reason = " + ".join(
            reasons
        )


    return {

        "signal": signal,

        "confidence": confidence,

        "rsi": rsi_value,

        "trend": trend,

        "reason": reason,

        "price": current_price,

        "atr": atr_value,

        "ema9": ema9,

        "ema21": ema21,

    }


# ============================================================
# LOAD DATA
# ============================================================

feed, feed_error = get_live_feed(
    st.session_state.pair
)


if feed:

    analysis = analyze_market(
        feed["candles"]
    )

    live_price = feed["price"]

    candles = feed["candles"]

    feed_status = "LIVE"

else:

    analysis = {

        "signal": "WAIT",

        "confidence": 0,

        "rsi": None,

        "trend": "OFFLINE",

        "reason": (
            "Real market feed is not connected."
        ),

        "price": None,

        "atr": None

    }

    live_price = None

    candles = []

    feed_status = "OFFLINE"


# ============================================================
# VALUES
# ============================================================

pair = st.session_state.pair

signal = analysis["signal"]

confidence = analysis["confidence"]

rsi_value = analysis["rsi"]

trend = analysis["trend"]

reason = analysis["reason"]


if live_price is not None:

    price_text = (
        f"{live_price:.8f}"
    )

else:

    price_text = "NO LIVE DATA"


if rsi_value is not None:

    rsi_text = str(
        rsi_value
    )

else:

    rsi_text = "--"


if confidence:

    confidence_text = (
        f"{confidence}%"
    )

else:

    confidence_text = "--"


chart_values = [

    candle["close"]

    for candle in candles[-40:]

]


chart_json = json.dumps(
    chart_values
)


# ============================================================
# PAIR OPTIONS
# ============================================================

pair_options = ""

for selected_pair in PAIRS:

    selected = ""

    if selected_pair == pair:

        selected = "selected"

    pair_options += f"""
    <option
        value="{selected_pair}"
        {selected}
    >
        {selected_pair}
    </option>
    """


# ============================================================
# EXPIRY OPTIONS
# ============================================================

expiry_options = ""

for label, seconds in EXPIRIES.items():

    selected = ""

    if seconds == st.session_state.expiry:

        selected = "selected"

    expiry_options += f"""
    <option
        value="{seconds}"
        {selected}
    >
        {label}
    </option>
    """


# ============================================================
# SIGNAL CSS CLASS
# ============================================================

if signal == "CALL":

    signal_class = "call"

elif signal == "PUT":

    signal_class = "put"

else:

    signal_class = "wait"


# ============================================================
# HTML
# ============================================================

html_code = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width,
initial-scale=1.0,
maximum-scale=1.0,
user-scalable=no"
>

<script
src="https://cdn.jsdelivr.net/npm/chart.js">
</script>


<style>

* {{

    box-sizing:border-box;

    margin:0;

    padding:0;

    user-select:none;

    -webkit-tap-highlight-color:
    transparent;

}}


body {{

    background:#0b0e11;

    color:#eaecef;

    font-family:
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Arial;

    padding:10px;

    max-width:520px;

    margin:auto;

}}


.card {{

    background:#1e2329;

    border:
    1px solid #2b313a;

    border-radius:10px;

    padding:10px;

    margin-bottom:10px;

}}


.header {{

    display:flex;

    justify-content:
    space-between;

    align-items:center;

}}


.logo {{

    font-size:22px;

    font-weight:900;

    color:#f0b90b;

}}


.status {{

    font-size:10px;

    font-weight:900;

}}


.live {{

    color:#0ecb81;

}}


.offline {{

    color:#f6465d;

}}


.controls {{

    display:grid;

    grid-template-columns:
    1fr 1fr;

    gap:8px;

}}


label {{

    display:block;

    color:#848e9c;

    font-size:10px;

    margin-bottom:4px;

}}


select,
button {{

    width:100%;

    background:#11161c;

    color:#eaecef;

    border:
    1px solid #2b313a;

    border-radius:8px;

    padding:10px;

    font-size:12px;

    outline:none;

}}


button {{

    grid-column:
    span 2;

    background:
    linear-gradient(
        135deg,
        #0ecb81,
        #065f46
    );

    border:0;

    color:white;

    font-weight:900;

}}


.metrics {{

    display:grid;

    grid-template-columns:
    repeat(3,1fr);

    gap:7px;

}}


.metric {{

    background:#11161c;

    border:
    1px solid #2b313a;

    border-radius:8px;

    padding:9px 3px;

    text-align:center;

}}


.metric small {{

    color:#848e9c;

    font-size:8px;

}}


.metric strong {{

    display:block;

    margin-top:3px;

    font-size:11px;

}}


.signal {{

    text-align:center;

    padding:16px;

    border-radius:10px;

    margin-bottom:10px;

    font-size:21px;

    font-weight:900;

}}


.call {{

    background:#064e3b;

    border:
    1px solid #0ecb81;

    color:#0ecb81;

}}


.put {{

    background:#7f1d1d;

    border:
    1px solid #f6465d;

    color:#f6465d;

}}


.wait {{

    background:#78350f;

    border:
    1px solid #f0b90b;

    color:#f0b90b;

}}


.timer {{

    display:flex;

    justify-content:
    space-between;

    font-size:10px;

    color:#848e9c;

}}


.timer strong {{

    color:#f0b90b;

}}


.chart {{

    height:220px;

}}


.reason {{

    color:#aab2bd;

    font-size:10px;

    line-height:1.5;

}}


.table-title {{

    color:#f0b90b;

    font-size:11px;

    font-weight:900;

    margin-bottom:7px;

}}


table {{

    width:100%;

    border-collapse:
    collapse;

    font-size:9px;

    text-align:center;

}}


th {{

    color:#848e9c;

    padding:5px 2px;

    border-bottom:
    1px solid #2b313a;

}}


td {{

    padding:5px 2px;

    border-bottom:
    1px solid #181c22;

}}


.notice {{

    color:#f0b90b;

    font-size:10px;

    line-height:1.5;

}}

</style>

</head>


<body>


<div class="card header">

    <div class="logo">

        JUTT BOT PRO

    </div>

    <div
        class="status {
            'live'
            if feed
            else
            'offline'
        }"
    >

        ● {feed_status}

    </div>

</div>


<div class="card">

    <div class="controls">


        <div>

            <label>
                PAIR / ASSET
            </label>

            <select
                id="pairSelect"
            >

                {pair_options}

            </select>

        </div>


        <div>

            <label>
                EXPIRY
            </label>

            <select
                id="expirySelect"
            >

                {expiry_options}

            </select>

        </div>


        <button
            onclick="generateSignal()"
        >

            ⚡ ANALYZE & GENERATE SIGNAL

        </button>


    </div>

</div>


<div class="metrics card">


    <div class="metric">

        <small>
            LIVE PRICE
        </small>

        <strong>
            {price_text}
        </strong>

    </div>


    <div class="metric">

        <small>
            RSI (14)
        </small>

        <strong>
            {rsi_text}
        </strong>

    </div>


    <div class="metric">

        <small>
            TREND
        </small>

        <strong>
            {trend}
        </strong>

    </div>


</div>


<div
class="signal {signal_class}"
>

    {signal}

    <div
    style="
    font-size:10px;
    margin-top:5px;
    font-weight:600;
    "
    >

        Model Strength:
        {confidence_text}

    </div>

</div>


<div class="card timer">

    <span>
        LAST CALL / EXPIRY
    </span>

    <strong id="timer">
        READY
    </strong>

</div>


<div class="card chart">

    <canvas
        id="marketChart">
    </canvas>

</div>


<div class="card reason">

    <b>
        Analysis:
    </b>

    {reason}

</div>


<div class="card">

    <div class="table-title">

        🕒 RECENT SIGNALS

    </div>


    <table>

        <thead>

            <tr>

                <th>
                    TIME
                </th>

                <th>
                    PAIR
                </th>

                <th>
                    TF
                </th>

                <th>
                    SIGNAL
                </th>

                <th>
                    CONF
                </th>

            </tr>

        </thead>


        <tbody>

            <tr>

                <td>
                    --
                </td>

                <td>
                    {pair}
                </td>

                <td>
                    --
                </td>

                <td>
                    {signal}
                </td>

                <td>
                    {confidence_text}
                </td>

            </tr>

        </tbody>

    </table>

</div>


<div class="card notice">

    ⚠️ No fake prices are generated.
    No random accuracy is displayed.
    Signals are calculated only from
    the live market candles supplied
    by the configured market-data feed.

</div>


<script>


const chartValues =
{chart_json};


const chartContext =
document
.getElementById(
    "marketChart"
)
.getContext("2d");


new Chart(
    chartContext,
    {{

        type:"line",

        data:{{

            labels:
            chartValues.map(
                (_,i)=>i+1
            ),

            datasets:[{{

                data:chartValues,

                borderColor:
                "#0ecb81",

                backgroundColor:
                "rgba(14,203,129,.08)",

                fill:true,

                borderWidth:2,

                pointRadius:0,

                tension:.25

            }}]

        }},

        options:{{

            responsive:true,

            maintainAspectRatio:false,

            plugins:{{

                legend:{{
                    display:false
                }}

            }},

            scales:{{

                x:{{

                    display:false

                }},

                y:{{

                    ticks:{{

                        color:
                        "#848e9c",

                        font:{{
                            size:8
                        }}

                    }},

                    grid:{{

                        color:
                        "#2b313a"

                    }}

                }}

            }}

        }}

    }}
);


let countdownInterval = null;


function generateSignal() {{

    const expiry =
    parseInt(
        document
        .getElementById(
            "expirySelect"
        )
        .value
    );


    if (countdownInterval) {{

        clearInterval(
            countdownInterval
        );

    }}


    let remaining =
    expiry;


    const timer =
    document
    .getElementById(
        "timer"
    );


    timer.innerText =
    formatTime(
        remaining
    );


    countdownInterval =
    setInterval(
        function() {{

            remaining--;

            timer.innerText =
            formatTime(
                Math.max(
                    remaining,
                    0
                )
            );


            if (
                remaining <= 0
            ) {{

                clearInterval(
                    countdownInterval
                );

                timer.innerText =
                "READY";

            }}

        }},
        1000
    );

}}


function formatTime(
    seconds
) {{

    const minutes =
    Math.floor(
        seconds / 60
    );


    const remainingSeconds =
    seconds % 60;


    return (
        String(minutes)
        .padStart(2,"0")
        + ":"
        +
        String(
            remainingSeconds
        ).padStart(2,"0")
    );

}}

</script>


</body>

</html>
"""


components.html(
    html_code,
    height=900,
    scrolling=True
)
