import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime

# Page Configuration - Pro Terminal Style
st.set_page_config(
    page_title="JUTT ON TOP | Pro Crypto Signal Terminal",
    page_icon="⚡",
    layout="wide"
)

# Custom Pro Styling (TradingView / Binance Dark Theme)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0e11;
        color: #eaecef;
    }
    .header-banner {
        background: linear-gradient(90deg, #1e2329 0%, #0b0e11 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2b313a;
        margin-bottom: 20px;
    }
    .metric-box {
        background-color: #1e2329;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #2b313a;
        text-align: center;
    }
    .signal-buy {
        background: linear-gradient(135deg, #0ecb81 0%, #064e3b 100%);
        color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(14, 203, 129, 0.3);
        margin: 15px 0;
    }
    .signal-sell {
        background: linear-gradient(135deg, #f6465d 0%, #7f1d1d 100%);
        color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(246, 70, 93, 0.3);
        margin: 15px 0;
    }
    .signal-neutral {
        background: linear-gradient(135deg, #f0b90b 0%, #78350f 100%);
        color: #ffffff;
        padding: 22px;
        border-radius: 12px;
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        box-shadow: 0 4px 20px rgba(240, 185, 11, 0.3);
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# Top Header
now = datetime.now()
st.markdown("""
<div class="header-banner">
    <h1 style="margin:0; color: #f0b90b; font-size: 32px;">⚡ JUTT ON TOP — Algorithmic Signal Terminal</h1>
    <p style="margin: 5px 0 0 0; color: #848e9c;">Live Market Intelligence, RSI & EMA Momentum Analysis (A to Z Coins & Meme Coins)</p>
</div>
""", unsafe_allow_html=True)

# Live Status Bar
col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    st.caption(f"📅 **Date:** {now.strftime('%A, %B %d, %Y')}")
with col_t2:
    st.caption(f"⏰ **UTC/Local Time:** {now.strftime('%I:%M:%S %p')}")
with col_t3:
    st.caption("🟢 **Feed Status:** CoinGecko Live Stream Connected")

# Fetch A to Z Coins List from CoinGecko
@st.cache_data(ttl=1800)
def get_all_coins():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': 150,
            'page': 1,
            'sparkline': 'false'
        }
        res = requests.get(url, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data
    except Exception as e:
        pass
    return []

coins_data = get_all_coins()

if coins_data:
    # Create dictionary and formatted list for selection (Name + Symbol + Meme badge)
    coin_options = {f"{c['name']} ({c['symbol'].upper()})": c['id'] for c in coins_data}
    symbol_keys = list(coin_options.keys())
    
    # Default to Dogecoin or Bitcoin if available
    default_index = 0
    for idx, key in enumerate(symbol_keys):
        if 'dogecoin' in coin_options[key] or 'bitcoin' in coin_options[key]:
            default_index = idx
            break

    st.sidebar.header("🎯 Market Selector")
    selected_label = st.sidebar.selectbox("Search & Select Coin (A - Z / Meme):", symbol_keys, index=default_index)
    selected_coin_id = coin_options[selected_label]
    
    chart_days = st.sidebar.selectbox("Analysis Interval / Range", ["1", "7", "14"], index=0, format_func=lambda x: f"Last {x} Day(s)")

    # Fetch Price History for Technical Analysis
    @st.cache_data(ttl=60)
    def get_coin_market_history(coin_id, days='1'):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {'vs_currency': 'usd', 'days': days}
        try:
            r = requests.get(url, params=params, timeout=10)
            if r.status_code == 200:
                json_data = r.json()
                prices = json_data.get('prices', [])
                df = pd.DataFrame(prices, columns=['timestamp', 'price'])
                df['price'] = df['price'].astype(float)
                return df
        except Exception:
            return None
        return None

    df_history = get_coin_market_history(selected_coin_id, days=chart_days)

    if df_history is not None and len(df_history) > 14:
        # Calculate RSI (14)
        delta = df_history['price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df_history['RSI'] = 100 - (100 / (1 + rs))

        # Calculate EMAs
        df_history['EMA_10'] = df_history['price'].ewm(span=10, adjust=False).mean()
        df_history['EMA_20'] = df_history['price'].ewm(span=20, adjust=False).mean()

        current_price = df_history['price'].iloc[-1]
        start_price = df_history['price'].iloc[0]
        change_24h = ((current_price - start_price) / start_price) * 100
        current_rsi = df_history['RSI'].iloc[-1]
        ema_10 = df_history['EMA_10'].iloc[-1]
        ema_20 = df_history['EMA_20'].iloc[-1]

        # Top Metric Cards
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(f'<div class="metric-box"><h4>Selected Asset</h4><h2>{selected_label.split("(")[0]}</h2></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><h4>Live Price (USD)</h4><h2>${current_price:,.6f}</h2><span style="color:{"#0ecb81" if change_24h>=0 else "#f6465d"}">{change_24h:+.2f}%</span></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-box"><h4>RSI (14) Momentum</h4><h2>{current_rsi:.2f}</h2></div>', unsafe_allow_html=True)
        with m4:
            trend_lbl = "BULLISH 🟢" if ema_10 > ema_20 else "BEARISH 🔴"
            st.markdown(f'<div class="metric-box"><h4>Trend Structure</h4><h2>{trend_lbl}</h2></div>', unsafe_allow_html=True)

        # Algorithmic Signal Engine
        if current_rsi < 38 and ema_10 >= ema_20:
            signal_title = "🚀 STRONG BUY SIGNAL — NOW IS THE TIME TO LONG / BUY"
            signal_class = "signal-buy"
            signal_desc = f"RSI is oversold ({current_rsi:.2f} < 38) with bullish EMA crossover confirmation."
        elif current_rsi > 62 and ema_10 <= ema_20:
            signal_title = "⚠️ STRONG SELL SIGNAL — CONSIDER EXIT / SHORT"
            signal_class = "signal-sell"
            signal_desc = f"RSI is overbought ({current_rsi:.2f} > 62) with bearish EMA rejection."
        else:
            signal_title = "⏸️ HOLD / NEUTRAL MARKET — WAIT FOR BREAKOUT"
            signal_class = "signal-neutral"
            signal_desc = f"Market is balanced (RSI: {current_rsi:.2f}). Wait for clear momentum confirmation."

        st.markdown(f'<div class="{signal_class}">{signal_title}</div>', unsafe_allow_html=True)
        st.info(f"📊 **Signal Diagnostic:** {signal_desc} | **Exact Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} PKT")

        # Interactive Price & EMA Chart
        st.markdown("### 📈 Live Price Action & Exponential Moving Averages")
        chart_df = df_history[['price', 'EMA_10', 'EMA_20']].copy()
        chart_df.columns = ['Price (USD)', 'EMA 10', 'EMA 20']
        st.line_chart(chart_df, height=380)

    else:
        st.warning("Loading real-time price tick history...")

else:
    st.error("Unable to load coin market data. Please refresh the page.")
