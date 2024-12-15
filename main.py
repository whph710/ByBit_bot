from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes
from analiz import analyze_api_data
from datetime import datetime
from func import analyze_trends


def round_minutes(time_str):
    # Преобразуем строку в объект datetime
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

    # Извлекаем минуты
    minutes = dt.minute

    # Округление до ближайшего числа, кратного 5, в меньшую сторону
    rounded_minutes = (minutes // 5) * 5

    return rounded_minutes


# Пример использования функции
print(get_bybit_linear_tickers_usdt())


# Пример использования функции
symbol = "CATIUSDT"
total = analyze_timeframes(symbol)
print(total)

kline = total['5min']
total2 = analyze_api_data(kline)
print(total2)

try:
    for ticket in get_bybit_linear_tickers_usdt():
        print(ticket)
        data = analyze_timeframes(ticket)
        kline = data['5min']
        data2 = analyze_api_data(kline)
        trend_lines, cross_signal = analyze_trends(data2)
        if cross_signal is not None:
            print("Trend Lines:", trend_lines)
            print("Cross Signal:", cross_signal)
        #df =
        #print(df)
except Exception as e:
    print(e)


