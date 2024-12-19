from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes
from func import gpt_analyze


def main():
    try:
        for ticket in get_bybit_linear_tickers_usdt():
            data = analyze_timeframes(ticket)
            a = gpt_analyze(data)
            print(ticket)
            print(a)

    except Exception as e:
        print(e)


# Запуск асинхронной функции main
if __name__ == "__main__":
    main()

