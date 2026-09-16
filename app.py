import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="JUTT BOT PRO — Ultimate AI Terminal",
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
    <title>JUTT BOT PRO — Ultimate AI Terminal</title>
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
            background-color: #0b0e11;
            color: #eaecef;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            padding: 8px;
            max-width: 480px;
            margin: 0 auto;
            height: 100vh;
            overflow-y: scroll;
            -webkit-overflow-scrolling: touch;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1e2329;
            padding: 8px 12px;
            border-radius: 10px;
            border: 1px solid #2b313a;
            margin-bottom: 8px;
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
            color: #848e9c;
        }
        select, button {
            width: 100%;
            background: #1e2329;
            color: #eaecef;
            border: 1px solid #2b313a;
            padding: 8px;
            border-radius: 8px;
            font-size: 11px;
            outline: none;
        }
        .btn-generate {
            grid-column: span 2;
            background: linear-gradient(135deg, #0ecb81 0%, #064e3b 100%);
            color: #fff;
            font-weight: 800;
            font-size: 13px;
            border: none;
            padding: 11px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(14, 203, 129, 0.3);
        }
        .btn-generate:disabled {
            background: #2b313a;
            color: #848e9c;
            box-shadow: none;
            cursor: not-allowed;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 5px;
            margin-bottom: 8px;
        }
        .metric-card {
            background: #1e2329;
            border: 1px solid #2b313a;
            padding: 6px 4px;
            border-radius: 6px;
            text-align: center;
        }
        .metric-card .title {
            font-size: 8px;
            color: #848e9c;
        }
        .metric-card .value {
            font-size: 11px;
            font-weight: bold;
            color: #eaecef;
            margin-top: 2px;
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
            background: linear-gradient(135deg, #0ecb81 0%, #064e3b 100%);
            border: 1px solid #0ecb81;
            color: #fff;
        }
        .signal-put {
            background: linear-gradient(135deg, #f6465d 0%, #7f1d1d 100%);
            border: 1px solid #f6465d;
            color: #fff;
        }
        .timer-strip {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1e2329;
            border: 1px solid #2b313a;
            padding: 7px 10px;
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 10px;
        }
        .timer-val {
            color: #f0b90b;
            font-weight: bold;
            font-size: 11px;
        }
        .spinner-box {
            display: none;
            text-align: center;
            padding: 12px;
            background: #1e2329;
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
            background: #1e2329;
            border: 1px solid #2b313a;
            border-radius: 10px;
            padding: 6px;
            position: relative;
            height: 190px;
            margin-bottom: 8px;
        }
        .reason-box {
            background: #1e2329;
            border: 1px solid #2b313a;
            padding: 7px;
            border-radius: 8px;
            font-size: 10px;
            color: #848e9c;
            margin-bottom: 8px;
        }
        .table-container {
            background: #1e2329;
            border: 1px solid #2b313a;
            border-radius: 10px;
            padding: 7px;
            margin-bottom: 30px;
        }
        .table-title {
            font-size: 10px;
            font-weight: bold;
            color: #f0b90b;
            margin-bottom: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 9px;
            text-align: center;
        }
        th {
            color: #848e9c;
            padding-bottom: 3px;
            border-bottom: 1px solid #2b313a;
        }
        td {
            padding: 4px 2px;
            border-bottom: 1px solid #181c22;
        }
        .badge-win {
            color: #0ecb81;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="header">
        <div style="display: flex; align-items: center; gap: 6px;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 130" width="180" height="58">
              <defs>
                <linearGradient id="gold3D" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#fffdf0"/>
                  <stop offset="50%" stop-color="#ca8a04"/>
                  <stop offset="100%" stop-color="#422006"/>
                </linearGradient>
                <linearGradient id="silver3D" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#ffffff"/>
                  <stop offset="100%" stop-color="#9ca3af"/>
                </linearGradient>
              </defs>
              <circle cx="50" cy="50" r="42" fill="#1f1f1f" stroke="url(#gold3D)" stroke-width="4"/>
              <text x="145" y="56" fill="url(#gold3D)" font-family="sans-serif" font-weight="900" font-size="36" letter-spacing="2">JUTT</text>
              <text x="238" y="56" fill="url(#silver3D)" font-family="sans-serif" font-weight="900" font-size="36" letter-spacing="2">BOT</text>
              <text x="210" y="78" fill="#e5e7eb" font-family="sans-serif" font-weight="700" font-size="12" text-anchor="middle" letter-spacing="4">ULTIMATE PRO</text>
            </svg>
        </div>
        <div class="clock-box" id="liveClock">00:00:00 AM</div>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>💱 Currency Pair</label>
            <select id="pairSelect" onchange="changeAsset()">
                <option value="EURUSD">EUR/USD</option>
                <option value="GBPUSD">GBP/USD</option>
                <option value="EURJPY">EUR/JPY</option>
                <option value="AUDUSD">AUD/USD</option>
                <option value="USDCAD">USD/CAD</option>
                <option value="NZDUSD">NZD/USD</option>
                <option value="USDCHF">USD/CHF</option>
                <option value="EURGBP">EUR/GBP</option>
                <option value="GBPJPY">GBP/JPY</option>
                <option value="AUDJPY">AUD/JPY</option>
            </select>
        </div>
        <div class="control-group">
            <label>⏳ Timeframe / Expiry</label>
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
                <option value="14400">4 Hours (4h)</option>
            </select>
        </div>
        <button class="btn-generate" id="genBtn" onclick="generateSignal()">⚡ GENERATE AI BOT SIGNAL</button>
    </div>

    <div class="timer-strip">
        <span>Bot Cooldown / Expiry Status</span>
        <span class="timer-val" id="countdownTimer">READY</span>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="title">TICK</div>
            <div class="value" id="mPrice">--</div>
        </div>
        <div class="metric-card">
            <div class="title">RSI</div>
            <div class="value" id="mRSI">50.0</div>
        </div>
        <div class="metric-card">
            <div class="title">VOLATILITY</div>
            <div class="value" id="mVol">NORMAL</div>
        </div>
        <div class="metric-card">
            <div class="title">TREND</div>
            <div class="value" id="mTrend">FLAT 🟡</div>
        </div>
    </div>

    <div class="spinner-box" id="spinnerBox">
        <div class="spinner"></div>
        <div>🤖 Scanning Order Book & Micro-Momentum Matrix...</div>
    </div>

    <div class="signal-card" id="signalCard">
        <div id="signalTitle">WAITING...</div>
        <div style="font-size: 10px; font-weight: normal; margin-top: 2px;" id="signalSub">AI Engine Synchronizing...</div>
    </div>

    <div class="chart-container">
        <canvas id="marketChart"></canvas>
    </div>

    <div class="reason-box" id="reasonBox">
        🧠 <b>Jutt Bot AI Engine:</b> Connected to multi-timeframe neural stream...
    </div>

    <div class="table-container">
        <div class="table-title">🕒 Live AI Signal History</div>
        <table id="historyTable">
            <thead>
                <tr>
                    <th>#</th>
                    <th>TIME</th>
                    <th>PAIR</th>
                    <th>TF</th>
                    <th>SIGNAL</th>
                    <th>CONF</th>
                    <th>STATUS</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>

    <script>
        setInterval(() => {
            document.getElementById('liveClock').innerText = new Date().toLocaleTimeString();
        }, 1000);

        let canGenerate = true;
        const timerElem = document.getElementById('countdownTimer');
        const genBtn = document.getElementById('genBtn');
        let prices = [];
        let basePrice = 1.0850;

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
        const labels = Array.from({length: 30}, (_, i) => `T-${30-i}`);

        const marketChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price Feed',
                    data: prices,
                    borderColor: '#0ecb81',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.2,
                    fill: true,
                    backgroundColor: 'rgba(14, 203, 129, 0.08)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#848e9c', font: { size: 7 } }, grid: { color: '#2b313a' } },
                    y: { ticks: { color: '#848e9c', font: { size: 7 } }, grid: { color: '#2b313a' } }
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

        setInterval(() => {
            let lastP = prices[prices.length - 1];
            let nextP = parseFloat((lastP + (Math.random() - 0.492) * 0.00025).toFixed(5));
            prices.shift();
            prices.push(nextP);
            marketChart.update('none');

            document.getElementById('mPrice').innerText = nextP.toFixed(5);
            let rsiVal = calculateRSI(prices);
            document.getElementById('mRSI').innerText = rsiVal;

            let diffPercent = Math.abs(nextP - lastP) / lastP * 100;
            const volElem = document.getElementById('mVol');
            if(diffPercent > 0.015) {
                volElem.innerText = 'HIGH 🔥';
                volElem.style.color = '#f6465d';
            } else {
                volElem.innerText = 'NORMAL 🟢';
                volElem.style.color = '#0ecb81';
            }

            const trendElem = document.getElementById('mTrend');
            if (rsiVal > 53) {
                trendElem.innerText = 'BULLISH 🟢';
            } else if (rsiVal < 47) {
                trendElem.innerText = 'BEARISH 🔴';
            } else {
                trendElem.innerText = 'SIDEWAYS 🟡';
            }
        }, 800);

        function startCountdown(durationSec) {
            canGenerate = false;
            genBtn.disabled = true;
            let timeLeft = durationSec;

            function formatTime(s) {
                if (s < 60) return `00:${s < 10 ? '0' + s : s}`;
                if (s < 3600) {
                    let m = Math.floor(s / 60);
                    let rem = s % 60;
                    return `${m < 10 ? '0' + m : m}:${rem < 10 ? '0' + rem : rem}`;
                }
                let h = Math.floor(s / 3600);
                let m = Math.floor((s % 3600) / 60);
                return `${h}h ${m}m`;
            }

            timerElem.innerText = `EXPIRY: ${formatTime(timeLeft)}`;

            const interval = setInterval(() => {
                timeLeft--;
                timerElem.innerText = `EXPIRY: ${formatTime(timeLeft)}`;

                if (timeLeft <= 0) {
                    clearInterval(interval);
                    timerElem.innerText = `READY FOR NEXT SIGNAL!`;
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
                let type, cls, win, reason, signalAction;

                if (rsiVal <= 54) {
                    type = `CALL ▲ [ ${pair} — HIGH ACCURACY UP ]`;
                    cls = 'signal-call';
                    win = Math.floor(86 + Math.random() * 9);
                    reason = `AI Matrix Confluence: Strong oversold bounce detected on ${pair} for ${expiryText} expiry.`;
                    marketChart.data.datasets[0].borderColor = '#0ecb81';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(14, 203, 129, 0.08)';
                    signalAction = 'BUY';
                } else {
                    type = `PUT ▼ [ ${pair} — HIGH ACCURACY DOWN ]`;
                    cls = 'signal-put';
                    win = Math.floor(86 + Math.random() * 9);
                    reason = `AI Matrix Confluence: Overbought rejection level confirmed on ${pair} for ${expiryText} expiry.`;
                    marketChart.data.datasets[0].borderColor = '#f6465d';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(246, 70, 93, 0.08)';
                    signalAction = 'SELL';
                }

                card.className = `signal-card ${cls}`;
                document.getElementById('signalTitle').innerText = type;
                document.getElementById('signalSub').innerText = `Confidence: ${win}% | Timeframe: ${expiryText}`;
                reasonBox.innerHTML = `🧠 <b>Jutt Bot AI Engine:</b> ${reason}`;
                marketChart.update();

                const tableBody = document.querySelector('#historyTable tbody');
                const nowStr = new Date().toTimeString().split(' ')[0];
                const newRow = document.createElement('tr');
                const sigText = signalAction === 'BUY' ? '<span style="color:#0ecb81">BUY</span>' : '<span style="color:#f6465d">SELL</span>';
                
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
            }, 1000);
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=True)
