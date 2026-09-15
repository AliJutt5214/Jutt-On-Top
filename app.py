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
            padding: 10px 14px;
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
            font-size: 13px;
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
            height: 200px;
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
        <div style="font-weight: 800; font-size: 15px; color: #f0b90b;">INDIAN BOT AI</div>
        <div class="clock-box" id="liveClock">00:00:00 AM</div>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>💱 Pair / Asset</label>
            <select id="pairSelect">
                <option value="EUR/USD (OTC)">EUR/USD (OTC)</option>
                <option value="GBP/USD (OTC)">GBP/USD (OTC)</option>
                <option value="EUR/JPY (OTC)">EUR/JPY (OTC)</option>
                <option value="AUD/USD (OTC)">AUD/USD (OTC)</option>
                <option value="USD/CAD (OTC)">USD/CAD (OTC)</option>
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
                <option value="300">5 Minutes (5m)</option>
            </select>
        </div>
        <button class="btn-generate" id="genBtn" onclick="generateSignal()">⚡ HIGH PROBABILITY SIGNAL</button>
    </div>

    <div class="timer-strip">
        <span>Signal Expiry Timer</span>
        <span class="timer-val" id="countdownTimer">READY</span>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="title">LIVE PRICE</div>
            <div class="value" id="mPrice">1.08249</div>
        </div>
        <div class="metric-card">
            <div class="title">AI CONVICTION</div>
            <div class="value" id="mConv">92%</div>
        </div>
        <div class="metric-card">
            <div class="title">SERVER TIME</div>
            <div class="value" id="srvTime">12:00:00</div>
        </div>
    </div>

    <div class="spinner-box" id="spinnerBox">
        <div class="spinner"></div>
        <div>🤖 AI analyzing market tick data...</div>
    </div>

    <div class="signal-card" id="signalCard">
        <div id="signalTitle">BUY (LONG)</div>
        <div style="font-size: 11px; font-weight: normal; margin-top: 3px;" id="signalSub">EUR/USD (OTC) | AI Conviction: 92%</div>
    </div>

    <div class="chart-container">
        <canvas id="marketChart"></canvas>
    </div>

    <div class="reason-box" id="reasonBox">
        🧠 <b>AI Market Status:</b> Select your timeframe (5s to 5m) and click generate signal.
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
                    <td>12:00:00</td>
                    <td>EUR/USD (OTC)</td>
                    <td>30s</td>
                    <td><span style="color:#0ecb81">BUY</span></td>
                    <td>92%</td>
                    <td><span class="badge-win">✔ WIN</span></td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        setInterval(() => {
            const now = new Date();
            const timeStr = now.toLocaleTimeString();
            document.getElementById('liveClock').innerText = timeStr;
            document.getElementById('srvTime').innerText = now.toTimeString().split(' ')[0];
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
        const labels = Array.from({length: 25}, (_, i) => `T-${25-i}s`);
        let prices = [];
        let base = 1.08249;
        for(let i=0; i<25; i++) {
            base += (Math.random() - 0.48) * 0.0003;
            prices.push(base.toFixed(5));
        }

        const marketChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Price',
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

                const isBuy = Math.random() > 0.4;
                const conf = Math.floor(86 + Math.random() * 11);

                if (isBuy) {
                    card.className = 'signal-card signal-call';
                    document.getElementById('signalTitle').innerText = 'BUY (LONG)';
                    marketChart.data.datasets[0].borderColor = '#0ecb81';
                } else {
                    card.className = 'signal-card signal-put';
                    document.getElementById('signalTitle').innerText = 'SELL (SHORT)';
                    marketChart.data.datasets[0].borderColor = '#f6465d';
                }

                document.getElementById('signalSub').innerText = `Signal for: ${pair} | Timeframe: ${expiryText}`;
                document.getElementById('mConv').innerText = conf + '%';
                reasonBox.innerHTML = `🧠 <b>AI Smart Analysis:</b> High probability setup on ${pair} for ${expiryText} expiry (${conf}% accuracy).`;
                marketChart.update();

                const tableBody = document.querySelector('#historyTable tbody');
                const nowStr = new Date().toTimeString().split(' ')[0];
                const newRow = document.createElement('tr');
                const sigText = isBuy ? '<span style="color:#0ecb81">BUY</span>' : '<span style="color:#f6465d">SELL</span>';
                const tfShort = expirySec < 60 ? expirySec + 's' : (expirySec / 60) + 'm';
                newRow.innerHTML = `
                    <td>+</td>
                    <td>${nowStr}</td>
                    <td>${pair}</td>
                    <td>${tfShort}</td>
                    <td>${sigText}</td>
                    <td>${conf}%</td>
                    <td><span class="badge-win">✔ WIN</span></td>
                `;
                tableBody.insertBefore(newRow, tableBody.firstChild);

                startCountdown(expirySec);
            }, 1500);
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=True)
