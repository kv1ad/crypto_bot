from core.logger import log_rejection

def is_signal_reliable(signal_data, market_data, news_list):
    if not signal_data["trend_confirmed"]:
        log_rejection(signal_data, "Тренд не подтвержден")
        return False, "bad trend"

    if signal_data["rsi"] < -30 or signal_data["rsi"] > 70:
        log_rejection(signal_data, "RSI вне допустимого диапазона")
        return False, "rsi"

    danger = ["hack", "lawsuit", "ban", "regulation", "delist"]
    for news in news_list:
        if any(word in news.lower() for word in danger):
            log_rejection(signal_data, "Обнаружены негативные новости")
            return False, "bad news"

    if signal_data["volume"] < signal_data["average_volume"] * 0.8:
        log_rejection(signal_data, "Низкий объем")
        return False, "low volume"

    return True, "ok"