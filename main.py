from request_bybit import get_bybit_linear_tickers_usdt, get_bybit_last_kline_data
from func import trend_ai, round_time_down, calculate_trade_result, analyze_candlestick_data_m5
import time


def main():
    try:
        tikets = get_bybit_linear_tickers_usdt()
        while tikets:
            for tiket in tikets[-1:]:
                kline = get_bybit_last_kline_data(tiket, interval=240, limit=200)
                dict_kline = trend_ai(kline[:-15])
                dict_kline['levels'] = analyze_candlestick_data_m5(kline)

                dict_kline['ticket'] = tiket
                dict_kline['time'] = round_time_down(minut=5)
                dict_kline['kline'] = kline
                tikets.remove(tiket)
                result = calculate_trade_result(trade_info=dict_kline['response'], candle_data=kline[-15:])
                print(result)
                with open(r'C:\Users\maxim\Documents\PycharmProjects\ByBit_bot\Trade.txt', 'a',
                          encoding='utf-8') as file:
                    file.write(tiket + ' ' + str(result) + '\n')
                print(dict_kline)
                time.sleep(5)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
