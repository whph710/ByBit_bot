from request_bybit import get_bybit_linear_tickers_usdt, get_bybit_last_kline_data
from func import gpt_analyze, round_time_down


def main():
    try:
        # Достаем список тикеров
        tickets = get_bybit_linear_tickers_usdt()
        # Запускаем цикл для каждого тикера
        for ticket in tickets:
            # Достаем данные
            data = get_bybit_last_kline_data(ticket, interval=5, limit=50)
            # Анализ
            a = gpt_analyze(data)
            # Сохраняем в файл
            trade_recommendation = a['trade_recommendation']
            if int(trade_recommendation['strength']) > 6:
                with open(r'C:\Users\maxim\Documents\PycharmProjects\ByBit_bot\Trade.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{ticket} => {round_time_down()}\n')
                    file.write(f'{trade_recommendation}\n')
                    file.write('********************************************************************************************\n')
                print(ticket, round_time_down())
                print(a['trade_recommendation'])
                print('********************************************************************************************')
            print(ticket, 'done')

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
