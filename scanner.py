import asyncio
from core.exchanges import get_top_symbols, get_price
from core.signal_filter import is_signal_reliable
from core.strategy import calculate_tp_sl
from core.messaging import send_signal
from core.news import fetch_news

async def scan_and_send_signals():
    print("🔍 Начинаю сканирование рынка...")
    all_symbols = await get_top_symbols(limit=100)  # Топ-100 монет
    news = fetch_news()

    for symbol_info in all_symbols:
        symbol = symbol_info["symbol"]
        exchange_name = symbol_info["exchange"]
        entry_price = await get_price(symbol, exchange_name)

        if entry_price is None:
            continue

        signal_data = {
            "symbol": symbol,
            "direction": "LONG",  # Пока фиксировано
            "entry": entry_price,
            "rsi": 50,
            "volume": 1000000,
            "average_volume": 1000000,
            "trend_confirmed": True
        }

        reliable, reason = is_signal_reliable(signal_data, {}, news)
        if reliable:
            tp, sl = calculate_tp_sl(entry_price, signal_data["direction"])
            send_signal(symbol, signal_data["direction"], entry_price, tp, sl, f"Авто ({exchange_name})", news)

if __name__ == "__main__":
    asyncio.run(scan_and_send_signals())
