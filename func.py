import google.generativeai as genai
from config import API_KEY, API_KEY2, API_KEY3
from datetime import datetime
import json

def round_time_down(minut=5):
    # Извлекаем минуты
    minutes = datetime.now().minute

    # Округляем минуты в меньшую сторону кратно
    rounded_minutes = (minutes // minut) * minut

    # Формируем новое время
    rounded_time = datetime.now().replace(minute=rounded_minutes, second=0, microsecond=0)

    return rounded_time.strftime("%Y-%m-%d %H:%M")

def trend_ai(data2):
    # Настройка API
    genai.configure(api_key=API_KEY)

    # Создание конфигурации генерации
    generation_config = {
        "temperature": 0,
        "top_p": 0,
        "top_k": 1,
        "max_output_tokens": 500,
        "response_schema": {
            "type": "object",
            "properties": {
                "response": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                },
            },
        },
        "response_mime_type": "application/json",
    }

    # Создание модели
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # Генерация контента
    response = model.generate_content([
        f"""
        
        Analyze a candlestick chart using technical analysis to detect more profitable trades.
                
                You are tasked with examining a candlestick chart based on technical analysis encompassing 200 candles. The goal is to identify more profitable trading opportunities.
                
                ## Input Data
                
                - **Ticker**: `str` - The symbol representing the asset being analyzed.
                - **Time**: `str` - The time at which the analysis is conducted.
                - **Kline**: `list[list[float]]` - A list containing sublists of [timestamp, open, high, low, close, volume] for each candle.
                
                ## Technical Analysis
                
                1. **Trend Lines**:
                   - Construct trend lines based on key High/Low points.
                   - Analyze trend strength via the angle of inclination.
                   - Identify breakouts and bounces.
                
                2. **Price Patterns**:
                   - Detect reversal patterns (head and shoulders, double bottom/top).
                   - Identify continuation patterns (flags, triangles, channels).
                   - Recognize candlestick patterns for signals.
                
                3. **Support/Resistance Levels**:
                   - Identify strong support and resistance levels.
                   - Observe round numbers and zones of consolidation.
                
                4. **Additional Signals**: *(To enhance profitable trade detection)*
                   - Incorporate volume analysis to confirm price movements.
                   - Utilize indicators like RSI, MACD for additional confirmation.
                   - Examine historical volatility to evaluate risk and timing.
                
                ## Entry Signals
                
                - **Long**:
                  - Breakout above descending trendlines.
                  - Bounce from strong support levels.
                  - Formation of upward reversal patterns.
                
                - **Short**:
                  - Breakdown below ascending trendlines.
                  - Rejection at strong resistance levels.
                  - Formation of downward reversal patterns.
                
                ## Risk Management
                
                - **Stop Loss**: Place beyond the nearest level/pattern.
                - **Take Profit**: Target the next strong level.
                - **Risk-Reward Ratio (R:R)**: Minimum of 1:2.
                
                # Output Format
                
                Provide a detailed analysis summary highlighting detected trading opportunities, including entry point suggestions, expected risk levels, and potential profit targets.
                
                # Notes
                
                Consider all relevant factors mentioned to enhance the accuracy in detecting profitable trades. Incorporating additional technical indicators and ensuring thorough risk evaluation will maximize success potential.
                Формат ответа: [направление, вход, тейк-профит, стоп-лосс]
                мне нужен только список, без рассуждений, максимально кратко, 
                ни одного лишнего слова у меня мало денег на счету мне нужны короткие ответы , в виде списка,
                [1, 100, 105, 98] или [-1, 100, 105, 98] или [0, 0, 0, 0]
                только так и никаким образом больше , эти данные пойдут дальше в обработку , не нарушай структуру ответа

            
            "input: ... output: '1', '100', '105', '98'",
            "input: ... output: '-1', '100', '105', '98'",
            "input: ... output: '0', '0', '0', '0'",
        
        "input: ...",
        "output: '1', '100', '105', '98'",
        "input: ...",
        "output: '-1', '100', '105', '98'",
        "input: ...",
        "output: '0', '0', '0', '0'",
        f"input: {data2}",
        "output: ",
       """
    ])

    # Преобразование ответа в JSON
    data1 = json.loads(response.text)

    # Вывод результата
    return data1['response']