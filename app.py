import ccxt
import pandas as pd
import numpy as np
import streamlit as st

# Page Config
st.set_page_config(page_title="Jutt On Top", page_icon="⚡", layout="centered")

st.title("⚡ Jutt On Top — Binance AI Signal Bot")
st.markdown("Real-time technical analysis & trading signals dashboard")

# Sidebar or main inputs
col1, col2 = st.columns(2)
with col1:
    symbol = st.selectbox(
        "Select Coin Symbol",
        ["DOGE/USDT", "PEPE/USDT", "SOL/USDT", "BTC/USDT", "ETH/USDT", "SHIB/USDT", "XRP/USDT"],
        index=0
    )
with col2:
    timeframe = st.selectbox(
        "Select Timeframe",
        ["1m", "3m", "5m", "10m", "15m", "30m", "1h"],
        index=4  # Default 15m
    )

analyze_btn = st.button("🔍 Analyze Market", use_container_width=True)

# Helper function for indicators
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def fetch_and_analyze(symbol, timeframe, limit=100):
    try:
        exchange = ccxt.binance()
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # EMAs
        df['ema9'] = df['close'].ewm(span=9, adjust=False).mean()
        df['ema21'] = df['close'].ewm(span=21, adjust=False).mean()
        df['ema50'] = df['close'].ewm(span=50, adjust=False).mean()
        
        # RSI
        df['rsi'] = calculate_rsi(df['close'], period=14)
        
        # MACD
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        up_score = 0
        down_score = 0
        reasons = []
        
        # EMA check
        if last['ema9'] > last['ema21'] > last['ema50']:
            up_score += 2
            reasons.append("EMA bullish stack")
        elif last['ema9'] < last['ema21'] < last['ema50']:
            down_score += 2
            reasons.append("EMA bearish stack")
            
        # Price vs EMA50
        if last['close'] > last['ema50']:
            up_score += 1
            reasons.append("Price above EMA50")
        else:
            down_score += 1
            reasons.append("Price below EMA50")
            
        # RSI check
        rsi_val = last['rsi']
        if rsi_val < 40:
            up_score += 1
            reasons.append(f"RSI oversold ({rsi_val:.1f})")
        elif rsi_val > 60:
            down_score += 1
            reasons.append(f"RSI overbought ({rsi_val:.1f})")
            
        # MACD check
        if last['macd'] > last['signal_line']:
            up_score += 2
            reasons.append("MACD bullish crossover")
        else:
            down_score += 2
            reasons.append("MACD bearish")
            
        # Candle check
        if last['close'] > last['open']:
            up_score += 1
            reasons.append("Closed candle bullish")
        else:
            down_score += 1
            reasons.append("Closed candle bearish")
            
        total_checks = 7
        if up_score > down_score and up_score >= 4:
            signal = "LONG / UP (BUY)"
            confidence = int((up_score / total_checks) * 100)
        elif down_score > up_score and down_score >= 4:
            signal = "SHORT / DOWN (SELL)"
            confidence = int((down_score / total_checks) * 100)
        else:
            signal = "NO TRADE / SIDEWAYS"
            confidence = 0
            reasons = ["No strong confirmation"]
            
        return {
            "price": last['close'],
            "rsi": rsi_val,
            "up_score": up_score,
            "down_score": down_score,
            "signal": signal,
            "confidence": confidence,
            "reasons": reasons
        }
    except Exception as e:
        return {"signal": "ERROR", "reasons": [str(e)]}

if analyze_btn:
    with st.spinner("Fetching live Binance data..."):
        res = fetch_and_assembled = fetch_and_analyze(symbol, timeframe)
        
        if res.get("signal") == "ERROR":
            st.error(f"Error: {res['reasons'][0]}")
        else:
            st.divider()
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Current Price", f"${res['price']:,.4f}")
            col_b.metric("RSI (14)", f"{res['rsi']:.2f}")
            col_c.metric("Confidence", f"{res['confidence']}%")
            
            st.info(f"**UP SCORE:** {res['up_score']}  |  **DOWN SCORE:** {res['down_score']}")
            
            # Display Signal Box
            if "LONG" in res['signal']:
                st.success(f"### SIGNAL: {res['signal']}")
            elif "SHORT" in res['signal']:
                st.error(f"### SIGNAL: {res['signal']}")
            else:
                st.warning(f"### SIGNAL: {res['signal']}")
                
            st.markdown("**Reasons:**")
            for r in res['reasons']:
                st.write(f"- {r}")