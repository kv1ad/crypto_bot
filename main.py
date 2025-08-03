from core.tradingview_webhook import start_webhook_server
from core.strategy import auto_analyze_market

if __name__ == "__main__":
    auto_analyze_market()
    start_webhook_server()