from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes


print(get_bybit_linear_tickers_usdt())


# Пример использования функции
symbol = "FUSDT"

print(analyze_timeframes(symbol))
