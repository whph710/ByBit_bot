from request_bybit import get_bybit_linear_tickers_usdt, get_bybit_last_kline_data
from func import trend_ai, round_time_down, ema_trend


def main():
    try:
        # Достаем список тикеров
        tickets = get_bybit_linear_tickers_usdt()
        # Запускаем цикл для каждого тикера
        for ticket in tickets[::5]:
            # Достаем данные
            data = get_bybit_last_kline_data(ticket, interval=5, limit=110)
            trend_ema = ema_trend(data)
            # Анализ
            trend = trend_ai(data)
            if "up" in trend and trend_ema == 1:
                print(f"ticket: {ticket} | trend: UP | time: {round_time_down()}")
            elif "down" in trend and trend_ema == -1:
                print(f"ticket: {ticket} | trend: DOWN | time: {round_time_down()}")

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
