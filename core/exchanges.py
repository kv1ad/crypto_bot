import requests

def get_binance_usdt_futures_symbols():
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    res = requests.get(url)
    data = res.json()
    symbols = []
    for s in data['symbols']:
        if s['quoteAsset'] == 'USDT' and s['contractType'] == 'PERPETUAL' and s['status'] == 'TRADING':
            symbols.append(s['symbol'])
    return symbols

def get_bybit_usdt_futures_symbols():
    url = "https://api.bybit.com/v2/public/symbols"
    res = requests.get(url)
    data = res.json()
    symbols = []
    if data['ret_code'] == 0:
        for s in data['result']:
            if s['quote_currency'] == 'USDT' and s['status'] == 'Trading':
                symbols.append(s['name'])
    return symbols
