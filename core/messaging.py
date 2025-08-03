import json
import asyncio
from telegram import Bot

# Загрузка конфигурации
with open("config.json", "r") as f:
    config = json.load(f)

bot = Bot(token=config["telegram_token"])
CHAT_ID = config["telegram_user_id"]

async def _send_async(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

def send_signal(symbol, direction, entry, take_profits, stop_loss, trend, news_list):
    text = f"""🚨 Сигнал на {symbol}
📈 Направление: {direction}
💰 Вход: {entry}
🛑 Стоп: {stop_loss}
🎯 Тейки:
 - {take_profits[0]}
 - {take_profits[1]}
 - {take_profits[2]}
📊 Тренд: {trend}
📰 Новости:"""

    if news_list:
        text += "\n" + "\n".join([f" - {n}" for n in news_list[:3]])
    else:
        text += "\n - нет важных новостей"

    try:
        asyncio.run(_send_async(text))
    except RuntimeError:
        # Если event loop уже запущен (например, в FastAPI), используем другой подход
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(_send_async(text))
        else:
            loop.run_until_complete(_send_async(text))
