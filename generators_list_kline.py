from request_bybit import get_bybit_last_kline_data


def analyze_timeframes(ticker):
    tf = 5
    candles = 50
    data = get_bybit_last_kline_data(ticker, str(tf), candles)
    return data
