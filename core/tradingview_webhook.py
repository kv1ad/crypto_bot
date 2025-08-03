import os
from flask import Flask, request
from core.strategy import calculate_tp_sl
from core.messaging import send_signal
from core.news import fetch_news
from core.signal_filter import is_signal_reliable

app = Flask(__name__)

@app.route("/")
def index():
    return "Сервер запущен и работает!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Получены данные:", data)  # Для отладки в логах Render
    symbol = data.get("symbol", "BTC/USDT")
    direction = data.get("direction", "LONG")
    entry = float(data.get("price", 0))

    news = fetch_news()
    print("Новости:", news)  # Для отладки

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
    print("Надежность сигнала:", reliable)  # Для отладки

    if reliable:
        tp, sl = calculate_tp_sl(entry, direction)
        print(f"TP: {tp}, SL: {sl}")  # Для отладки
        send_signal(symbol, direction, entry, tp, sl, "Webhook", news)

    return "ok", 200

def start_webhook_server():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_webhook_server()
