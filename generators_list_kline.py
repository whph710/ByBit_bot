from request_bybit import get_bybit_last_kline_data


def analyze_timeframes(ticker):
    timeframes = [5, 15, 60]
    timeframe_candles = {
        5: 100,  # 5-минутный таймфрейм (M5)
        15: 50,  # 15-минутный таймфрейм (M15)
        60: 30  # 60-минутный таймфрейм (H1)
    }

    results = {}

    for tf in timeframes:
        data = get_bybit_last_kline_data(ticker, str(tf), timeframe_candles[tf])
        results[str(tf)+'min'] = data

    return results
