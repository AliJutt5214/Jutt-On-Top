import json
import threading
import time
from datetime import datetime
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import websocket
import streamlit as st
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Jutt On Top - Binance",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
html, body, [class*="css"] { font-family: Arial, sans-serif; }
header { visibility: hidden; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.main-title { font-size: 34px; font-weight: 900; letter-spacing: 1px; }
.sub-title { color: #888; margin-bottom: 20px; }
.card { background: #11151a; border: 1px solid #292f36; border-radius: 15px; padding: 18px; margin-bottom: 15px; }
.signal-call { color: #00d084; font-size: 46px; font-weight: 900; text-align: center; }
.signal-put { color: #ff5555; font-size: 46px; font-weight: 900; text-align: center; }
.signal-none { color: #f0c75e; font-size: 42px; font-weight: 900; text-align: center; }
.reason { padding: 7px 0; border-bottom: 1px solid #222; }
</style>
""",
    unsafe_allow_html=True,
)

PAIR_LIST = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "DOTUSDT",
    "MATICUSDT",
]

# ============================================================
# BINANCE LIVE ENGINE
# ============================================================


class BinanceLiveEngine:

  def __init__(self):
    self.connected = False
    self.error = ""
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
        item = {"time": float(data["T"]) / 1000.0, "price": float(data["p"])}
        with self.lock:
          self.ticks.append(item)
          if len(self.ticks) > 1000:
            self.ticks.pop(0)
          self.last_update = time.time()
          self.connected = True

      def on_open(ws):
        self.connected = True

      def on_close(ws, close_status_code, close_msg):
        self.connected = False

      ws = websocket.WebSocketApp(
          socket_url, on_open=on_open, on_message=on_message, on_close=on_close
      )
      ws.run_forever()

    threading.Thread(target=run, daemon=True).start()

  def get_candles(self, symbol, interval="1m", limit=100):
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
        })
      return candles
    except Exception as e:
      self.error = str(e)
      return []

  def get_ticks(self, limit=100):
    with self.lock:
      return list(self.ticks)[-limit:]


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "engine" not in st.session_state:
  st.session_state.engine = BinanceLiveEngine()
  st.session_state.engine.start_socket("SOLUSDT")

if "history" not in st.session_state:
  st.session_state.history = []

engine = st.session_state.engine

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">⚡ JUTT BOT PRO TRADER — BINANCE</div>
<div class="sub-title">LIVE FUTURES & SCALPING MARKET ANALYZER</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# CONTROLS
# ============================================================

c1, c2, c3 = st.columns([1.5, 1, 1])

with c1:
  pair = st.selectbox("PAIR", PAIR_LIST, index=2)
  if pair.lower() != engine.current_symbol.upper():
    engine.start_socket(pair)

with c2:
  expiry = st.selectbox(
      "TIMEFRAME", ["1m", "3m", "5m", "15m", "30m", "1h"], index=2
  )

with c3:
  generate = st.button("⚡ GENERATE LIVE SIGNAL", use_container_width=True)

# ============================================================
# STATUS METRICS
# ============================================================

s1, s2, s3, s4 = st.columns(4)

with s1:
  if engine.connected:
    st.success("● LIVE CONNECTED")
  else:
    st.error("● RECONNECTING...")

with s2:
  ticks = engine.get_ticks(10)
  live_price = ticks[-1]["price"] if ticks else None
  st.metric(
      "LIVE PRICE", f"{live_price:.2f}" if live_price is not None else "--"
  )

with s3:
  candles = engine.get_candles(pair, expiry, 50)
  df_temp = pd.DataFrame(candles)
  rsi_val = (
      RSIIndicator(close=df_temp["close"], window=14).rsi().iloc[-1]
      if not df_temp.empty
      else None
  )
  st.metric(
      "RSI 14", f"{rsi_val:.1f}" if rsi_val is not None and not np.isnan(rsi_val) else "--"
  )

with s4:
  st.metric("LIVE TICKS", len(engine.get_ticks(500)))

# ============================================================
# LIVE CHART
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader(f"Live Market — {pair}")

if candles:
  df_chart = pd.DataFrame(candles)
  fig = go.Figure(
      data=[
          go.Candlestick(
              x=pd.to_datetime(df_chart["time"], unit="s"),
              open=df_chart["open"],
              high=df_chart["high"],
              low=df_chart["low"],
              close=df_chart["close"],
              name=pair,
          )
      ]
  )
  fig.update_layout(
      height=450,
      margin=dict(l=10, r=10, t=20, b=10),
      paper_bgcolor="#0e1117",
      plot_bgcolor="#0e1117",
      font=dict(color="white"),
      xaxis_rangeslider_visible=False,
  )
  st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
else:
  st.info("Loading chart data from Binance...")
st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# SIGNAL & ANALYSIS
# ============================================================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("AI MARKET & FUTURES ANALYSIS")

if generate:
  if candles and len(candles) >= 30:
    df_ana = pd.DataFrame(candles)
    df_ana["RSI"] = RSIIndicator(close=df_ana["close"], window=14).rsi()
    df_ana["EMA_9"] = EMAIndicator(close=df_ana["close"], window=9).ema_indicator()
    df_ana["EMA_21"] = EMAIndicator(
        close=df_ana["close"], window=21
    ).ema_indicator()
    atr = AverageTrueRange(
        high=df_ana["high"], low=df_ana["low"], close=df_ana["close"], window=14
    ).average_true_range().iloc[-1]

    close_p = df_ana["close"].iloc[-1]
    rsi_p = df_ana["RSI"].iloc[-1]
    ema9_p = df_ana["EMA_9"].iloc[-1]
    ema21_p = df_ana["EMA_21"].iloc[-1]

    signal = "NO SIGNAL"
    reasons = []

    if rsi_p < 40 and ema9_p > ema21_p:
      signal = "CALL"
      reasons.append("RSI is in oversold/accumulating zone with Bullish EMA support")
    elif rsi_p > 60 and ema9_p < ema21_p:
      signal = "PUT"
      reasons.append("RSI is in overbought zone with Bearish EMA pressure")
    else:
      reasons.append("Market is sideways or indicators are neutral")

    st.session_state.last_analysis = {
        "signal": signal,
        "rsi": rsi_p,
        "price": close_p,
        "atr": atr,
        "reasons": reasons,
    }

analysis = st.session_state.get("last_analysis")

if analysis:
  sig = analysis["signal"]
  if sig == "CALL":
    st.markdown('<div class="signal-call">BUY / LONG (CALL)</div>', unsafe_allow_html=True)
    st.info(
        f"Stop-Loss: {analysis['price'] - (1.5 * analysis['atr']):.2f} |"
        f" Take-Profit: {analysis['price'] + (2.5 * analysis['atr']):.2f}"
    )
  elif sig == "PUT":
    st.markdown('<div class="signal-put">SELL / SHORT (PUT)</div>', unsafe_allow_html=True)
    st.info(
        f"Stop-Loss: {analysis['price'] + (1.5 * analysis['atr']):.2f} |"
        f" Take-Profit: {analysis['price'] - (2.5 * analysis['atr']):.2f}"
    )
  else:
    st.markdown('<div class="signal-none">NO CLEAR SETUP</div>', unsafe_allow_html=True)

  for r in analysis["reasons"]:
    st.markdown(f'<div class="reason">• {r}</div>', unsafe_allow_html=True)
else:
    st.info("Click **GENERATE LIVE SIGNAL** to analyze current Binance market data.")

st.markdown("</div>", unsafe_allow_html=True)

# Auto refresh to keep live ticks updated
time.sleep(2)
st.rerun()
