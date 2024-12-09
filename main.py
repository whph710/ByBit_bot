from request_bybit import get_bybit_linear_tickers_usdt, get_bybit_last_kline_data


print(get_bybit_linear_tickers_usdt())


# Пример использования функции
symbol = "BTCUSDT"
interval = "240"  # 4-часовой интервал в минутах (4 часа = 240 минут)

kline_data = get_bybit_last_kline_data(symbol, interval)
if kline_data:
    for kline in kline_data:
        print(kline)
else:
    print("No kline data found.")