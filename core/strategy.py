import ccxt
import pandas as pd
from ta.trend import EMAIndicator
from core.signal_filter import is_signal_reliable
from core.messaging import send_signal
from core.news import fetch_news

import json

with open("config.json", "r") as f:
    config = json.load(f)

binance = ccxt.binance()

def calculate_tp_sl(entry_price, direction):
    if direction == "LONG":
        take_profits = [round(entry_price * x, 2) for x in [1.015, 1.03, 1.045]]
        stop_loss = round(entry_price * 0.977, 2)
    else:
        take_profits = [round(entry_price * x, 2) for x in [0.985, 0.97, 0.955]]
        stop_loss = round(entry_price * 1.023, 2)
    return take_profits, stop_loss

def auto_analyze_market():
    symbols = config["symbols"]
    for symbol in symbols:
        try:
            ohlcv = binance.fetch_ohlcv(symbol, timeframe="1h", limit=200)
            df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
            ema50 = EMAIndicator(df["close"], window=50).ema_indicator()
            ema200 = EMAIndicator(df["close"], window=200).ema_indicator()
            trend = "UPTREND" if ema50.iloc[-1] > ema200.iloc[-1] else "DOWNTREND"
            direction = "LONG" if trend == "UPTREND" else "SHORT"
            rsi = df["close"].pct_change().rolling(14).mean().iloc[-1] * 100
            entry = df["close"].iloc[-1]
            volume = df["volume"].iloc[-1]
            avg_volume = df["volume"].rolling(20).mean().iloc[-1]
            news = fetch_news()
            signal_data = {
                "symbol": symbol,
                "direction": direction,
                "entry": entry,
                "rsi": rsi,
                "volume": volume,
                "average_volume": avg_volume,
                "trend_confirmed": True
            }
            reliable, _ = is_signal_reliable(signal_data, {}, news)
            if reliable:
                tp, sl = calculate_tp_sl(entry, direction)
                send_signal(symbol, direction, entry, tp, sl, trend, news)
        except Exception as e:
            print(f"Ошибка анализа {symbol}: {e}")