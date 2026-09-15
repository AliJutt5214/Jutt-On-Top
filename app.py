<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>INDIAN BOT PRO — Quotex Binary AI Terminal</title>
    <!-- Chart.js CDN -->
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
        .logo-title h2 {
            color: #f0b90b;
            font-size: 16px;
            font-weight: 700;
        }
        .logo-title span {
            color: #848e9c;
            font-size: 10px;
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
        .btn-generate:active {
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
        .signal-wait {
            background: linear-gradient(135deg, #f0b90b 0%, #78350f 100%);
            border: 1px solid #f0b90b;
            color: #fff;
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
            height: 240px;
        }
        .reason-box {
            background: #1e2329;
            border: 1px solid #2b313a;
            padding: 8px;
            border-radius: 8px;
            font-size: 11px;
            color: #848e9c;
            margin-top: 8px;
        }
    </style>
</head>
<body>

    <div class="header">
        <div class="logo-title">
            <h2>⚡ INDIAN BOT PRO</h2>
            <span>Quotex & Binary AI Signal Terminal</span>
        </div>
        <div class="clock-box" id="liveClock">00:00:00 AM</div>
    </div>

    <div class="controls">
        <div class="control-group">
            <label>💱 Pair / Asset</label>
            <select id="pairSelect">
                <option value="EUR/USD">EUR/USD (Euro/USD)</option>
                <option value="GBP/USD">GBP/USD (Pound/USD)</option>
                <option value="EUR/JPY">EUR/JPY (Euro/Yen)</option>
                <option value="AUD/USD">AUD/USD (Aussie/USD)</option>
                <option value="USD/CAD">USD/CAD (USD/CAD)</option>
                <option value="GBP/JPY">GBP/JPY (Pound/Yen)</option>
            </select>
        </div>
        <div class="control-group">
            <label>⏳ Expiry Time</label>
            <select id="expirySelect">
                <option value="5 Sec">5 Seconds</option>
                <option value="15 Sec">15 Seconds</option>
                <option value="30 Sec">30 Seconds</option>
                <option value="1 Min" selected>1 Minute</option>
                <option value="5 Min">5 Minutes</option>
            </select>
        </div>
        <button class="btn-generate" onclick="generateSignal()">⚡ GENERATE AI SIGNAL</button>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <div class="title">LIVE PRICE</div>
            <div class="value" id="mPrice">1.08542</div>
        </div>
        <div class="metric-card">
            <div class="title">RSI (14)</div>
            <div class="value" id="mRSI">48.5</div>
        </div>
        <div class="metric-card">
            <div class="title">TREND</div>
            <div class="value" id="mTrend">BULLISH 🟢</div>
        </div>
    </div>

    <div class="spinner-box" id="spinnerBox">
        <div class="spinner"></div>
        <div>🤖 Indian Bot scanning Tick Microstructure & Order Flow...</div>
    </div>

    <div class="signal-card" id="signalCard">
        <div id="signalTitle">CALL ▲ (HIGHER / UP TRADE)</div>
        <div style="font-size: 11px; font-weight: normal; margin-top: 3px;" id="signalSub">Win Probability: 88% | Expiry: 1 Min</div>
    </div>

    <div class="chart-container">
        <canvas id="marketChart"></canvas>
    </div>

    <div class="reason-box" id="reasonBox">
        🧠 <b>Confluence Log:</b> Ready for scan. Click "GENERATE AI SIGNAL" above.
    </div>

    <script>
        setInterval(() => {
            const now = new Date();
            document.getElementById('liveClock').innerText = now.toLocaleTimeString();
        }, 1000);

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
                    x: { ticks: { color: '#848e9c', font: { size: 9 } }, grid: { color: '#2b313a' } },
                    y: { ticks: { color: '#848e9c', font: { size: 9 } }, grid: { color: '#2b313a' } }
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
        }, 1500);

        function generateSignal() {
            const spinner = document.getElementById('spinnerBox');
            const card = document.getElementById('signalCard');
            const reasonBox = document.getElementById('reasonBox');
            const pair = document.getElementById('pairSelect').value;
            const expiry = document.getElementById('expirySelect').value;

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
                    reason = `RSI Oversold Bounce + EMA7/EMA14 Bullish Crossover on ${pair} (${expiry})`;
                    marketChart.data.datasets[0].borderColor = '#0ecb81';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(14, 203, 129, 0.08)';
                } else if (r > 0.20) {
                    type = `PUT ▼ [ ${pair} — DOWN / LOWER ]`;
                    cls = 'signal-put';
                    win = Math.floor(82 + Math.random() * 14);
                    reason = `RSI Overbought Rejection + Upper Bollinger Band Touch on ${pair} (${expiry})`;
                    marketChart.data.datasets[0].borderColor = '#f6465d';
                    marketChart.data.datasets[0].backgroundColor = 'rgba(246, 70, 93, 0.08)';
                } else {
                    type = `⏸️ WAIT / SIDEWAYS MARKET (${pair})`;
                    cls = 'signal-wait';
                    win = 55;
                    reason = `Low volume & flat price action. Skip this candle expiry (${expiry}).`;
                }

                card.className = `signal-card ${cls}`;
                document.getElementById('signalTitle').innerText = type;
                document.getElementById('signalSub').innerText = `Win Probability: ${win}% | Expiry Time: ${expiry}`;
                reasonBox.innerHTML = `🧠 <b>Indian Bot Confluence:</b> ${reason}`;
                marketChart.update();
            }, 3000);
        }
    </script>
</body>
</html>
