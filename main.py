import asyncio
from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes
from gpt_analyze import  gpt_text
from func import process_ifish_data


async def main():
    try:
        for ticket in get_bybit_linear_tickers_usdt():
            data = analyze_timeframes(ticket)
            total_text = process_ifish_data(data)
            print(total_text)

    except Exception as e:
        print(e)

# Запуск асинхронной функции main
if __name__ == "__main__":
    asyncio.run(main())

