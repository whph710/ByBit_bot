from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes
from analiz import analyze_api_data
from func import analyze_trend_lines

print(get_bybit_linear_tickers_usdt())


# Пример использования функции
symbol = "CATIUSDT"
total = analyze_timeframes(symbol)
print(total)

kline = total['5min']
total2 = analyze_api_data(kline)
print(total2)

trend = analyze_trend_lines(total2)
print(trend)