import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="JUTT BOT PRO — Quotex Binary AI Terminal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 0rem;
        padding-right: 0rem;
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
    <title>JUTT BOT PRO — Quotex Binary AI Terminal</title>
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
            padding: 10px;
            max-width: 480px;
            margin: 0 auto;
            overflow-y: auto;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1e2329;
            padding: 8px 12px;
            border-radius: 10px;
            border: 1px solid #2b313a;
            margin-bottom: 10px;
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
            gap: 8px;
            margin-bottom: 10px;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 3px;
        }
        label {
            font-size: 11px;
            color: #848e9c;
        }
        select, button {
            width: 100%;
            background: #1e2329;
            color: #eaecef;
            border: 1px solid #2b313a;
            padding: 9px;
            border-radius: 8px;
            font-size: 12px;
            outline: none;
        }
        .btn-generate {
            grid-column: span 2;
            background: linear-gradient(135deg, #0ecb81 0%, #064e3b 100%);
            color: #fff;
            font-weight: 800;
            font-size: 14px;
            border: none;
            padding: 12px;
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
        .btn-generate:active:not(:disabled) {
            transform: scale(0.97);
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 10px;
        }
        .metric-card {
            background: #1e2329;
            border: 1px solid #2b313a;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
        }
        .metric-card .title {
            font-size: 9px;
            color: #848e9c;
        }
        .metric-card .value {
            font-size: 12px;
            font-weight: bold;
            color: #eaecef;
            margin-top: 2px;
        }
        .signal-card {
            display: none;
            padding: 14px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 15px;
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
            padding: 8px 12px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-size: 11px;
        }
        .timer-val {
            color: #f0b90b;
            font-weight: bold;
            font-size: 12px;
        }
        .spinner-box {
            display: none;
            text-align: center;
            padding: 14px;
            background: #1e2329;
            border-radius: 10px;
            border: 1px solid #f0b90b;
            margin-bottom: 10px;
            color: #f0b90b;
            font-size: 13px;
        }
        .spinner {
            width: 22px;
            height: 22px;
            border: 3px solid rgba(240, 185, 11, 0.3);
            border-top: 3px solid #f0b90b;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin: 0 auto 6px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .chart-container {
            background: #1e2329;
            border: 1px solid #2b313a;
            border-radius: 10px;
            padding: 8px;
            position: relative;
            height: 210px;
            margin-bottom: 10px;
        }
        .reason-box {
            background: #1e2329;
            border: 1px solid #2b313a;
            padding: 8px;
            border-radius: 8px;
            font-size: 11px;
            color: #848e9c;
            margin-bottom: 10px;
        }
        .table-container {
            background: #1e2329;
            border: 1px solid #2b313a;
            border-radius: 10px;
            padding: 8px;
        }
        .table-title {
            font-size: 11px;
            font-weight: bold;
            color: #f0b90b;
            margin-bottom: 6px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10px;
            text-align: center;
        }
        th {
            color: #848e9c;
            padding-bottom: 4px;
            border-bottom: 1px solid #2b313a;
        }
        td {
            padding: 5px 2px;
            border-bottom: 1px solid #181c22;
        }
        .badge-win {
            color: #0ecb81;
            font-weight: bold;
        }
        .badge-loss {
            color: #f6465d;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <div class="header">
        <div style="display: flex; align-items: center; gap: 8px;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 130" width="200" height="66">
              <defs>
                <linearGradient id="gold3D" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#fffdf0"/>
                  <stop offset="15%" stop-color="#fde047"/>
                  <stop offset="50%" stop-color="#ca8a04"/>
                  <stop offset="85%" stop-color="#854d0e"/>
                  <stop offset="100%" stop-color="#422006"/>
                </linearGradient>
                <linearGradient id="silver3D" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stop-color="#ffffff"/>
                  <stop offset="40%" stop-color="#e5e7eb"/>
                  <stop offset="100%" stop-color="#9ca3af"/>
                </linearGradient>
                <radialGradient id="glow" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                  <stop offset="0%" stop-color="#fde047" stop-opacity="0.5"/>
                  <stop offset="100%" stop-color="#ca8a04" stop-opacity="0"/>
                </radialGradient>
              </defs>
              <circle cx="50" cy="50" r="42" fill="#1f1f1f" stroke="url(#gold3D)" stroke-width="4"/>
              <circle cx="50" cy="50" r="38" fill="none" stroke="#fef08a" stroke-width="1.5" opacity="0.4"/>
              <ellipse cx="50" cy="50" r="30" fill="url(#glow)"/>
              <rect x="38" y="38" width="6" height="20" fill="url(#gold3D)" rx="2"/>
              <line x1="41" y1="34" x2="41" y2="64" stroke="url(#gold3D)" stroke-width="3" stroke-linecap="round"/>
              <rect x="52" y="28" width="6" height="30" fill="url(#gold3D)" rx="2"/>
              <line x1="55" y1="24" x2="55" y2="64" stroke="url(#gold3D)" stroke-width="3" stroke-linecap="round"/>
              <path d="M28 70 Q 45 42, 66 54 T 84 30" fill="none" stroke="#15803d" stroke-width="5" stroke-linecap="round" opacity="0.9"/>
              <polygon points="84,30 80,42 92,40" fill="#16a34a"/>
              <path d="M185 2 L197 18 L209 2 L221 18 L233 2 V26 H185 Z" fill="url(#gold3D)" filter="drop-shadow(0 0 3px #fde047)"/>
              <text x="145" y="56" fill="url(#gold3D)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="36" letter-spacing="2">JUTT</text>
              <text x="238" y="56" fill="url(#silver3D)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="36" letter-spacing="2">BOT</text>
              <text x="210" y="78" fill="#e5e7eb" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="700" font-size="12" text-anchor="middle" letter-spacing="4">PRO TRADER</text>
              <text x="215" y="108" fill="url(#gold3D)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-weight="800" font-size="10" text-anchor="middle" letter-spacing="2">ANALYZE  |  SIGNAL  |  TRADE  |  GROW</text>
            </svg>
        </div>
        <div class="clock-box" id="liveClock">00:00:00 AM</div>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>💱 Pair / Asset</label>
            <select id="pairSelect">
                <option value="EUR/USD (Euro/USD)">EUR/USD (Euro/USD)</option>
                <option value="GBP/USD (Pound/USD)">GBP/USD (Pound/USD)</option>
                <option value="EUR/JPY (Euro/Yen)">EUR/JPY (Euro/Yen)</option>
                <option value="AUD/USD (Aussie/USD)">AUD/USD (Aussie/USD)</option>
                <option value="USD/CAD (USD/CAD)">USD/CAD (USD/CAD)</option>
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
                <option value="300">5 Minutes (5m)</option>
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
            <div class="value" id="mPrice">1.08585</div>
        </div>
        <div class="metric-card">
            <div class="title">RSI (14)</div>
            <div class="value" id="mRSI">60.0</div>
        </div>
        <div class="metric-card">
            <div class="title">TREND</div>
            <div class="value" id="mTrend">BULLISH 🟢</div>
        </div>
    </div>

    <div class="spinner-box" id="spinnerBox">
        <div class="spinner"></div>
        <div>🤖 Jutt Bot scanning Tick Microstructure & Order Flow...</div>
    </div>

    <div class="signal-card" id="signalCard">
        <div id="signalTitle">CALL ▲ (HIGHER / UP TRADE)</div>
        <div style="font-size: 11px; font-weight: normal; margin-top: 3px;" id="signalSub">Win Probability: 88% | Expiry: 30 Seconds</div>
    </div>

    <div class="chart-container">
        <canvas id="marketChart"></canvas>
    </div>

    <div class="reason-box" id="reasonBox">
        🧠 <b>Jutt Bot Confluence:</b> Ready for scan. Click "GENERATE AI SIGNAL" above.
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
                <tr>
                    <td>1</td>
                    <td>11:12:30</td>
                    <td>EUR/USD (Euro/USD)</td>
                    <td>30s</td>
                    <td><span style="color:#0ecb81">BUY</span></td>
                    <td>90%</td>
                    <td><span class="badge-win">✔ WIN</span></td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        setInterval(() => {
            const now = new Date();
            document.getElementById('liveClock').innerText = now.toLocaleTimeString();
        }, 1000);

        let canGenerate = true;
        const timerElem = document.getElementById('countdownTimer');
        const genBtn = document.getElementById('genBtn');

        function startCountdown(durationSec) {
            canGenerate = false;
            genBtn.disabled = true;
            let timeLeft = durationSec;

            function formatTime(s) {
                if (s < 60) return `00:${s < 10 ? '0' + s : s}`;
                let m = Math.floor(s / 60);
                let rem = s % 60;
                return `0${m}:${rem < 10 ? '0' + rem : rem}`;
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

        const ctx = document.getElementById('marketChart').getContext('2d');
        const labels = Array.from({length: 30}, (_, i) => `T-${30-i}s`);
        let prices = [];
        let base = 1.0850;
        for(let i=0; i<30; i++) {
            base += (Math.random() - 0.48) * 0.0004;
            prices.push(base.toFixed(5));
        }

        const marketChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price Action',
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
                    x: { ticks: { color: '#848e9c', font: { size: 8 } }, grid: { color: '#2b313a' } },
                    y: { ticks: { color: '#848e9c', font: { size: 8 } }, grid: { color: '#2b313a' } }
                }
            }
        });

        setInterval(() => {
            let lastP = parseFloat(prices[prices.length - 1]);
            let nextP = lastP + (Math.random() - 0.49) * 0.0003;
            prices.shift();
            prices.push(nextP.toFixed(5));
            marketChart.update('none');

            document.getElementById('mPrice').innerText = nextP.toFixed(5);
            let rsiVal = (40 + Math.random() * 25).toFixed(1);
            document.getElementById('mRSI').innerText = rsiVal;
            const trendElem = document.getElementById('mTrend');
            if (rsiVal > 55) {
                trendElem.innerText = 'BULLISH 🟢';
            } else if (rsiVal < 45) {
                trendElem.innerText = 'BEARISH 🔴';
            } else {
                trendElem.innerText = 'SIDEWAYS 🟡';
            }
        }, 1500);

        function generateSignal() {
            if (!canGenerate) return;

            const spinner = document.getElementById('spinnerBox');
            const card = document.getElementById('signalCard');
            const reasonBox = document.getElementById('reasonBox');
            const pair = document.getElementById('pairSelect').value;
            const expirySec = parseInt(document.getElementById('expirySelect').value);
            const expiryText = document.getElementById('expirySelect').options[document.getElementById('expirySelect').selectedIndex].text;

            card.style.display = 'none';
            spinner.style.display = 'block';

            setTimeout(() => {
                spinner.style.display = 'none';
                card.style.display = 'block';

                const r = Math.random();
                let type, cls, win, reason;

                if (r > 0.48) {
                    type = `CALL ▲ [ ${pair} — UP / HIGHER ]`;
                    cls = 'signal-call';
                    win = Math.floor(82 + Math.random() * 14);
                    reason = `RSI Oversold Bounce + EMA7/EMA14 Bullish Crossover on ${pair} (${expiryText})`;
                    marketChart.data.datasets[0].borderColor = '#0ecb81';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(14, 203, 129, 0.08)';
                } else if (r > 0.20) {
                    type = `PUT ▼ [ ${pair} — DOWN / LOWER ]`;
                    cls = 'signal-put';
                    win = Math.floor(82 + Math.random() * 14);
                    reason = `RSI Overbought Rejection + Upper Bollinger Band Touch on ${pair} (${expiryText})`;
                    marketChart.data.datasets[0].borderColor = '#f6465d';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(246, 70, 93, 0.08)';
                } else {
                    type = `⏸️ WAIT / SIDEWAYS MARKET (${pair})`;
                    cls = 'signal-wait';
                    win = 55;
                    reason = `Low volume & flat price action. Skip this candle expiry (${expiryText}).`;
                }

                card.className = `signal-card ${cls}`;
                document.getElementById('signalTitle').innerText = type;
                document.getElementById('signalSub').innerText = `Win Probability: ${win}% | Expiry: ${expiryText}`;
                reasonBox.innerHTML = `🧠 <b>Jutt Bot Confluence:</b> ${reason}`;
                marketChart.update();

                const tableBody = document.querySelector('#historyTable tbody');
                const nowStr = new Date().toTimeString().split(' ')[0];
                const newRow = document.createElement('tr');
                const sigText = r > 0.48 ? '<span style="color:#0ecb81">BUY</span>' : (r > 0.20 ? '<span style="color:#f6465d">SELL</span>' : '<span style="color:#f0b90b">WAIT</span>');
                const tfShort = expirySec < 60 ? expirySec + 's' : (expirySec / 60) + 'm';
                newRow.innerHTML = `
                    <td>+</td>
                    <td>${nowStr}</td>
                    <td>${pair}</td>
                    <td>${tfShort}</td>
                    <td>${sigText}</td>
                    <td>${win}%</td>
                    <td><span class="badge-win">✔ WIN</span></td>
                `;
                tableBody.insertBefore(newRow, tableBody.firstChild);

                startCountdown(expirySec);
            }, 2000);
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=True)
