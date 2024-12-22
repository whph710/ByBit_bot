from request_bybit import get_bybit_linear_tickers_usdt, get_bybit_last_kline_data
from func import trend_ai, round_time_down, ema_trend, print_and_save_to_file
import time


def main():
    try:
        tikets = get_bybit_linear_tickers_usdt()
        while tikets:
            for tiket in tikets:
                kline = get_bybit_last_kline_data(tiket, interval=5, limit=100)
                dict_kline = trend_ai(kline)
                dict_kline['trend'] = ema_trend(kline)
                dict_kline['ticket'] = tiket
                dict_kline['time'] = round_time_down()
                dict_kline['kline'] = kline
                tikets.remove(tiket)
                print_and_save_to_file(dict_kline)
                time.sleep(10)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
