from request_bybit import get_bybit_linear_tickers_usdt, get_bybit_last_kline_data
from func import trend_ai, round_time_down, ema_trend, generate_response


def main():
    try:
        for tiket in get_bybit_linear_tickers_usdt():
            kline = get_bybit_last_kline_data(tiket, interval=5, limit=50)
            dict_kline = trend_ai(kline)
            dict_kline['trend'] = ema_trend(kline)
            dict_kline['ticket'] = tiket
            dict_kline['time'] = round_time_down()
            dict_kline['kline'] = kline
            recommendation = generate_response(dict_kline)
            print(dict_kline)
            print(recommendation)


    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
