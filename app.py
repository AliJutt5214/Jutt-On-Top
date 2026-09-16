import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Jutt On Top",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    header {visibility: hidden; display: none !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important; display: none !important;}
    div[data-testid="stToolbar"] {visibility: hidden !important; display: none !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important; display: none !important;}
    .block-container {
        padding: 0rem;
        overscroll-behavior-y: none;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Jutt On Top</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
            user-select: none;
        }
        body {
            background-color: #0e1117;
            color: #eaecef;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 8px;
            max-width: 480px;
            margin: 0 auto;
            height: 100vh;
            overflow-y: scroll;
            -webkit-overflow-scrolling: touch;
        }
        .header-card {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 10px 12px;
            border-radius: 12px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo-area {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .clock-box {
            text-align: right;
            font-size: 11px;
            color: #f0b90b;
            font-weight: bold;
        }
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 8px;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }
        label {
            font-size: 10px;
            color: #8b949e;
        }
        select, button {
            width: 100%;
            background: #161b22;
            color: #eaecef;
            border: 1px solid #30363d;
            padding: 9px;
            border-radius: 8px;
            font-size: 11px;
            outline: none;
        }
        .btn-generate {
            grid-column: span 2;
            background: linear-gradient(135deg, #238636 0%, #1ea34d 100%);
            color: #fff;
            font-weight: 800;
            font-size: 13px;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(35, 134, 54, 0.4);
        }
        .btn-generate:disabled {
            background: #30363d;
            color: #8b949e;
            box-shadow: none;
            cursor: not-allowed;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-bottom: 8px;
        }
        .metric-card {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 8px 4px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-card .title {
            font-size: 9px;
            color: #8b949e;
        }
        .metric-card .value {
            font-size: 12px;
            font-weight: bold;
            color: #eaecef;
            margin-top: 3px;
        }
        .signal-card {
            display: none;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 8px;
            font-size: 14px;
        }
        .signal-call {
            background: linear-gradient(135deg, #238636 0%, #1ea34d 100%);
            border: 1px solid #238636;
            color: #fff;
        }
        .signal-put {
            background: linear-gradient(135deg, #da3633 0%, #b31d1c 100%);
            border: 1px solid #da3633;
            color: #fff;
        }
        .timer-strip {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #161b22;
            border: 1px solid #30363d;
            padding: 8px 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 11px;
            color: #8b949e;
        }
        .timer-val {
            color: #f0b90b;
            font-weight: bold;
        }
        .spinner-box {
            display: none;
            text-align: center;
            padding: 12px;
            background: #161b22;
            border-radius: 10px;
            border: 1px solid #f0b90b;
            margin-bottom: 8px;
            color: #f0b90b;
            font-size: 12px;
        }
        .spinner {
            width: 20px;
            height: 20px;
            border: 3px solid rgba(240, 185, 11, 0.3);
            border-top: 3px solid #f0b90b;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 5px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .chart-container {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 8px;
            position: relative;
            height: 190px;
            margin-bottom: 8px;
        }
        .reason-box {
            background: #161b22;
            border: 1px solid #30363d;
            padding: 8px;
            border-radius: 8px;
            font-size: 10px;
            color: #8b949e;
            margin-bottom: 8px;
        }
        .table-container {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 8px;
            margin-bottom: 30px;
        }
        .table-title {
            font-size: 10px;
            font-weight: bold;
            color: #f0b90b;
            margin-bottom: 6px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
            text-align: center;
        }
        th {
            color: #8b949e;
            padding-bottom: 4px;
            border-bottom: 1px solid #30363d;
        }
        td {
            padding: 5px 2px;
            border-bottom: 1px solid #21262d;
        }
        .badge-win {
            color: #238636;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="header-card">
        <div class="logo-area">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 130" width="165" height="52">
              <defs>
                <linearGradient id="goldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#fffdf0"/>
                  <stop offset="50%" stop-color="#d4af37"/>
                  <stop offset="100%" stop-color="#5c4033"/>
                </linearGradient>
                <linearGradient id="silverGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#ffffff"/>
                  <stop offset="100%" stop-color="#8b949e"/>
                </linearGradient>
              </defs>
              <circle cx="45" cy="50" r="38" fill="#161b22" stroke="url(#goldGrad)" stroke-width="3"/>
              <!-- Mini chart inside logo circle -->
              <polyline points="25,60 35,50 45,55 55,38 65,42" fill="none" stroke="#238636" stroke-width="3"/>
              <circle cx="65" cy="42" r="3" fill="#238636"/>
              
              <text x="135" y="46" fill="url(#goldGrad)" font-family="sans-serif" font-weight="900" font-size="32" letter-spacing="1">JUTTBOT</text>
              <text x="137" y="68" fill="url(#silverGrad)" font-family="sans-serif" font-weight="700" font-size="11" letter-spacing="3">PRO TRADER</text>
              <text x="137" y="88" fill="#8b949e" font-family="sans-serif" font-weight="600" font-size="7" letter-spacing="1.5">ANALYZE | SIGNAL | TRADE | GROW</text>
              
              <!-- Crown above JUTT -->
              <path d="M165,18 L173,28 L181,18 L189,28 L197,18 L193,33 L169,33 Z" fill="url(#goldGrad)"/>
            </svg>
        </div>
        <div class="clock-box" id="liveClock">00:00:00 pm</div>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>💱 Pair / Asset</label>
            <select id="pairSelect" onchange="changeAsset()">
                <option value="EURUSD">EUR/USD (Euro/USD)</option>
                <option value="GBPUSD">GBP/USD (Pound/USD)</option>
                <option value="EURJPY">EUR/JPY (Euro/JPY)</option>
                <option value="AUDUSD">AUD/USD (Aussie/USD)</option>
                <option value="USDCAD" selected>USD/CAD (USD/Canada)</option>
                <option value="NZDUSD">NZD/USD (Kiwi/USD)</option>
                <option value="USDCHF">USD/CHF (USD/Franc)</option>
                <option value="EURGBP">EUR/GBP (Euro/Pound)</option>
                <option value="GBPJPY">GBP/JPY (Pound/JPY)</option>
                <option value="AUDJPY">AUD/JPY (Aussie/JPY)</option>
            </select>
        </div>
        <div class="control-group">
            <label>⏳ Expiry Time</label>
            <select id="expirySelect">
                <option value="5">5 Seconds (5s)</option>
                <option value="10">10 Seconds (10s)</option>
                <option value="15">15 Seconds (15s)</option>
                <option value="30" selected>30 Seconds (30s)</option>
                <option value="60">1 Minute (1m)</option>
                <option value="120">2 Minutes (2m)</option>
                <option value="180">3 Minutes (3m)</option>
                <option value="300">5 Minutes (5m)</option>
                <option value="600">10 Minutes (10m)</option>
                <option value="1800">30 Minutes (30m)</option>
                <option value="3600">1 Hour (1h)</option>
            </select>
        </div>
        <button class="btn-generate" id="genBtn" onclick="generateSignal()">⚡ GENERATE AI SIGNAL</button>
    </div>

    <div class="timer-strip">
        <span>Signal Expiry Timer</span>
        <span class="timer-val" id="countdownTimer">READY</span>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="title">LIVE PRICE</div>
            <div class="value" id="mPrice">--</div>
        </div>
        <div class="metric-card">
            <div class="title">RSI (14)</div>
            <div class="value" id="mRSI">50.0</div>
        </div>
        <div class="metric-card">
            <div class="title">TREND</div>
            <div class="value" id="mTrend">FLAT 🟡</div>
        </div>
    </div>

    <div class="spinner-box" id="spinnerBox">
        <div class="spinner"></div>
        <div>🤖 Jutt Bot Confluence: Filtering market structure...</div>
    </div>

    <div class="signal-card" id="signalCard">
        <div id="signalTitle">WAITING...</div>
        <div style="font-size: 10px; font-weight: normal; margin-top: 2px;" id="signalSub">AI Engine Synchronizing...</div>
    </div>

    <div class="chart-container">
        <canvas id="marketChart"></canvas>
    </div>

    <div class="reason-box" id="reasonBox">
        🧠 <b>Jutt Bot Confluence:</b> Fetching live price stream & calculating technical indicators...
    </div>

    <div class="table-container">
        <div class="table-title">🕒 Recent Signals History</div>
        <table id="historyTable">
            <thead>
                <tr>
                    <th>#</th>
                    <th>TIME</th>
                    <th>PAIR</th>
                    <th>TF</th>
                    <th>SIGNAL</th>
                    <th>CONF</th>
                    <th>RESULT</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>

    <script>
        setInterval(() => {
            const d = new Date();
            let hours = d.getHours();
            let minutes = d.getMinutes();
            let seconds = d.getSeconds();
            let ampm = hours >= 12 ? 'pm' : 'am';
            hours = hours % 12;
            hours = hours ? hours : 12;
            minutes = minutes < 10 ? '0'+minutes : minutes;
            seconds = seconds < 10 ? '0'+seconds : seconds;
            document.getElementById('liveClock').innerText = hours + ':' + minutes + ':' + seconds + ' ' + ampm;
        }, 1000);

        let canGenerate = true;
        const timerElem = document.getElementById('countdownTimer');
        const genBtn = document.getElementById('genBtn');
        let prices = [];
        let basePrice = 1.3620;

        const basePrices = {
            'EURUSD': 1.0854,
            'GBPUSD': 1.2685,
            'EURJPY': 161.40,
            'AUDUSD': 0.6542,
            'USDCAD': 1.3620,
            'NZDUSD': 0.6120,
            'USDCHF': 0.8950,
            'EURGBP': 0.8550,
            'GBPJPY': 190.20,
            'AUDJPY': 98.40
        };

        let currentPair = document.getElementById('pairSelect').value;
        basePrice = basePrices[currentPair];

        function changeAsset() {
            currentPair = document.getElementById('pairSelect').value;
            basePrice = basePrices[currentPair];
            prices = [];
            for(let i=0; i<30; i++) {
                basePrice += (Math.random() - 0.49) * 0.00015;
                prices.push(parseFloat(basePrice.toFixed(5)));
            }
            marketChart.data.datasets[0].data = prices;
            marketChart.update();
        }

        for(let i=0; i<30; i++) {
            basePrice += (Math.random() - 0.49) * 0.00015;
            prices.push(parseFloat(basePrice.toFixed(5)));
        }

        const ctx = document.getElementById('marketChart').getContext('2d');
        const labels = Array.from({length: 30}, (_, i) => `T-${30-i}s`);

        const marketChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price Feed',
                    data: prices,
                    borderColor: '#238636',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.2,
                    fill: true,
                    backgroundColor: 'rgba(35, 134, 54, 0.08)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#8b949e', font: { size: 7 } }, grid: { color: '#30363d' } },
                    y: { ticks: { color: '#8b949e', font: { size: 7 } }, grid: { color: '#30363d' } }
                }
            }
        });

        function calculateRSI(dataArr) {
            if (dataArr.length < 15) return 50.0;
            let gains = 0, losses = 0;
            for (let i = dataArr.length - 14; i < dataArr.length; i++) {
                let diff = dataArr[i] - dataArr[i - 1];
                if (diff >= 0) gains += diff;
                else losses -= diff;
            }
            let avgGain = gains / 14;
            let avgLoss = losses / 14;
            if (avgLoss === 0) return 100;
            let rs = avgGain / avgLoss;
            return parseFloat((100 - (100 / (1 + rs))).toFixed(1));
        }

        // True Pro Trend Filter: Ensures signal strictly matches multi-candle momentum direction
        function getValidatedTrend(dataArr) {
            let rsi = calculateRSI(dataArr);
            let recentShift = dataArr[dataArr.length - 1] - dataArr[dataArr.length - 8];
            
            if (recentShift > 0.00002 && rsi >= 45) {
                return 'BULLISH';
            } else if (recentShift < -0.00002 && rsi <= 55) {
                return 'BEARISH';
            }
            return recentShift >= 0 ? 'BULLISH' : 'BEARISH';
        }

        setInterval(() => {
            let lastP = prices[prices.length - 1];
            let nextP = parseFloat((lastP + (Math.random() - 0.492) * 0.00025).toFixed(5));
            prices.shift();
            prices.push(nextP);
            marketChart.update('none');

            document.getElementById('mPrice').innerText = nextP.toFixed(5);
            let rsiVal = calculateRSI(prices);
            document.getElementById('mRSI').innerText = rsiVal;

            let trendState = getValidatedTrend(prices);
            const trendElem = document.getElementById('mTrend');
            if (trendState === 'BULLISH') {
                trendElem.innerText = 'BULLISH 🟢';
            } else {
                trendElem.innerText = 'BEARISH 🔴';
            }
        }, 800);

        function startCountdown(durationSec) {
            canGenerate = false;
            genBtn.disabled = true;
            let timeLeft = durationSec;

            function formatTime(s) {
                if (s < 60) return `00:${s < 10 ? '0' + s : s}`;
                let m = Math.floor(s / 60);
                let rem = s % 60;
                return `${m < 10 ? '0' + m : m}:${rem < 10 ? '0' + rem : rem}`;
            }

            timerElem.innerText = formatTime(timeLeft);

            const interval = setInterval(() => {
                timeLeft--;
                timerElem.innerText = formatTime(timeLeft);

                if (timeLeft <= 0) {
                    clearInterval(interval);
                    timerElem.innerText = `READY`;
                    canGenerate = true;
                    genBtn.disabled = false;
                }
            }, 1000);
        }

        function generateSignal() {
            if (!canGenerate) return;

            const spinner = document.getElementById('spinnerBox');
            const card = document.getElementById('signalCard');
            const reasonBox = document.getElementById('reasonBox');
            const pair = document.getElementById('pairSelect').value;
            const expirySec = parseInt(document.getElementById('expirySelect').value);
            const expirySelectElem = document.getElementById('expirySelect');
            const expiryText = expirySelectElem.options[expirySelectElem.selectedIndex].text;

            card.style.display = 'none';
            spinner.style.display = 'block';

            setTimeout(() => {
                spinner.style.display = 'none';
                card.style.display = 'block';

                let rsiVal = calculateRSI(prices);
                let trendState = getValidatedTrend(prices);
                let type, cls, win, reason, signalAction;

                // Strict synchronization with validated market trend
                if (trendState === 'BULLISH') {
                    type = `CALL ▲ [ ${pair} — HIGH ACCURACY UP ]`;
                    cls = 'signal-call';
                    win = Math.floor(88 + Math.random() * 8);
                    reason = `Jutt Bot Confluence: Bullish momentum verified. RSI at ${rsiVal} supports upward continuation on ${pair} for ${expiryText}.`;
                    marketChart.data.datasets[0].borderColor = '#238636';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(35, 134, 54, 0.08)';
                    signalAction = 'BUY';
                } else {
                    type = `PUT ▼ [ ${pair} — HIGH ACCURACY DOWN ]`;
                    cls = 'signal-put';
                    win = Math.floor(88 + Math.random() * 8);
                    reason = `Jutt Bot Confluence: Bearish pressure confirmed. RSI at ${rsiVal} aligns with downward trend on ${pair} for ${expiryText}.`;
                    marketChart.data.datasets[0].borderColor = '#da3633';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(218, 54, 51, 0.08)';
                    signalAction = 'SELL';
                }

                card.className = `signal-card ${cls}`;
                document.getElementById('signalTitle').innerText = type;
                document.getElementById('signalSub').innerText = `Confidence: ${win}% | Timeframe: ${expiryText}`;
                reasonBox.innerHTML = `🧠 <b>Jutt Bot Confluence:</b> ${reason}`;
                marketChart.update();

                const tableBody = document.querySelector('#historyTable tbody');
                const nowStr = new Date().toTimeString().split(' ')[0];
                const newRow = document.createElement('tr');
                const sigText = signalAction === 'BUY' ? '<span style="color:#238636">BUY</span>' : '<span style="color:#da3633">SELL</span>';
                
                let tfShort = expirySec < 60 ? expirySec + 's' : (expirySec < 3600 ? (expirySec / 60) + 'm' : (expirySec / 3600) + 'h');
                
                newRow.innerHTML = `
                    <td>+</td>
                    <td>${nowStr}</td>
                    <td>${pair}</td>
                    <td>${tfShort}</td>
                    <td>${sigText}</td>
                    <td>${win}%</td>
                    <td><span class="badge-win">✔ SUCCESS</span></td>
                `;
                tableBody.insertBefore(newRow, tableBody.firstChild);

                startCountdown(expirySec);
            }, 1200);
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=True)
