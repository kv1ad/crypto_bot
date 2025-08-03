from telegram import Bot
import json
import asyncio  # Добавлено

with open("config.json", "r") as f:
    config = json.load(f)

bot = Bot(token=config["telegram_token"])
CHAT_ID = config["telegram_user_id"]

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

    # Исправлено: ожидаем асинхронно
    asyncio.run(bot.send_message(chat_id=CHAT_ID, text=text))
