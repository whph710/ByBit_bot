import asyncio
from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes
from gpt_analyze import gemini_analyze, gpt_text


async def main():
    try:
        for ticket in get_bybit_linear_tickers_usdt():
            print(ticket, end=' ')
            data = analyze_timeframes(ticket)
            print(await gpt_text(data))
    except Exception as e:
        print(e)

# Запуск асинхронной функции main
if __name__ == "__main__":
    asyncio.run(main())

