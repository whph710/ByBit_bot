import asyncio
from request_bybit import get_bybit_linear_tickers_usdt
from generators_list_kline import analyze_timeframes
from gpt_analyze import  gemini_analyze, gpt_text
from func import calculate_moving_averages, calculate_rsi, calculate_adx,calculate_stochastic_oscillator, promt


async def main():
    try:
        for ticket in get_bybit_linear_tickers_usdt():
            data = analyze_timeframes(ticket)
            print(ticket)
            a = (str(promt([calculate_moving_averages(data),
                   calculate_rsi(data),
                   calculate_adx(data),
                   calculate_stochastic_oscillator(data)])))
            with open('result.txt', 'a', encoding='utf-8') as file:
                file.write(ticket + a + '\n')
            # print(await gpt_text(str(promt([calculate_moving_averages(data),
            #        calculate_rsi(data),
            #        calculate_adx(data),
            #        calculate_stochastic_oscillator(data)]))))

    except Exception as e:
        print(e)

# Запуск асинхронной функции main
if __name__ == "__main__":
    asyncio.run(main())

