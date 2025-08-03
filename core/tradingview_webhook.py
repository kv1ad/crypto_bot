from flask import Flask, request
from core.strategy import calculate_tp_sl
from core.messaging import send_signal
from core.news import fetch_news
from core.signal_filter import is_signal_reliable

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    symbol = data.get("symbol", "BTC/USDT")
    direction = data.get("direction", "LONG")
    entry = float(data.get("price", 0))

    news = fetch_news()
    signal_data = {
        "symbol": symbol,
        "direction": direction,
        "entry": entry,
        "rsi": 50,
        "volume": 1000000,
        "average_volume": 1000000,
        "trend_confirmed": True
    }

    reliable, _ = is_signal_reliable(signal_data, {}, news)
    if reliable:
        tp, sl = calculate_tp_sl(entry, direction)
        send_signal(symbol, direction, entry, tp, sl, "Webhook", news)

    return "ok", 200

def start_webhook_server():
    app.run(port=8000)