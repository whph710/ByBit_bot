import google.generativeai as genai
from config import API_KEY3
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
    genai.configure(api_key=API_KEY3)

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
        """
        ### Введение и контекст
        **Цель промпта**: Обеспечить точный и надежный анализ данных для прогнозирования резких движений цены на 
        фондовом рынке, используя методы технического анализа.
        **Контекст**: Использование технического анализа для принятия решений на финансовых рынках, включая анализ 
        графиков, свечных паттернов и других индикаторов.

        ### Описание задачи
        **Описание задачи**: Провести анализ данных через индикатор и использовать все доступные знания технического
        анализа, включая фигуры технического анализа и свечные паттерны, для прогнозирования направления резкого 
        движения цены на следующих пяти свечах. Если резкого движения не предвидится, указать это. Также предоставить
        три числа: точку входа в позицию, тейк-профит и стоп-лосс.
        **Критерии успеха**: Точность прогноза направления движения цены, обоснованность выбора точки входа,
        тейк-профита и стоп-лосса.
        
        ### Входные данные
        **Типы данных**: Исторические данные цен, индикаторы технического анализа, свечные паттерны.
        **Формат данных**: Графики и таблицы с историческими данными цен.
        **Примеры данных**: График цен акции компании XYZ за последний месяц.
        
        ### Ограничения и требования
        **Ограничения**: Ограничения по времени анализа и объему данных.
        **Требования**: Высокая точность прогноза, обоснованность выбора точки входа, тейк-профита и стоп-лосса.
        
        ### Стиль торговли : агрессивный, для получения максимальной прибыли на 5 минутном ТФ, учитывай волантильность актива
        и предварительный анализ свечных паттернов, ТОРГОВЛЯ ДОЛЖНА ПРОИСХОДИТЬ ОТ УРОВНЕЙ
        
        ### Методы и подходы
        **Методы**: Использование индикаторов технического анализа, анализ свечных паттернов и фигур технического 
        анализа.
        **Подходы**: Анализ исторических данных, поиск паттернов и индикаторов, прогнозирование будущих движений цены.
        
        ### Выходные данные
        **Формат выходных данных**: Направление движения цены (1 для роста, -1 для падения, 0 для отсутствия движения), 
        три числа: точка входа, тейк-профит, стоп-лосс.
        **Примеры выходных данных**: [1, 100, 110, 95], [ -1, 100, 95, 102]
        
        ### Оценка и валидация
        **Метрики оценки**: Точность прогноза, обоснованность выбора точки входа, тейк-профита и стоп-лосса.
        **Методы валидации**: Сравнение прогнозов с реальными данными, анализ точности предсказаний.
        
        ### Примеры использования
        **Примеры использования**: Прогнозирование движения цен акций, фьючерсов, валютных пар.
        **Результаты**: Повышение точности торговых решений, улучшение управления рисками.
        
        ### Заключение
        **Итоги**: Технический анализ должен предоставлять точные и обоснованные прогнозы направления движения цены, 
        а также рекомендации по точке входа, тейк-профиту и стоп-лоссу.
        """
        "input: {...}",
        "output: '1', 100, 105, 98",
        "input: {...}",
        "output: '-1', 100, 105, 98",
        # "input: {...}",
        # "output: '0', 0, 0, 0",
        f"input: {data2}",
        "output: ",
    ])
    data1 = json.loads(response.text)
    print(data1)
    # Вывод результата
    return data1


def calculate_trade_result(trade_info, candle_data):
    # Разбираем trade_info
    trend = int(trade_info[0])
    entry_price = float(trade_info[1])
    take_profit = float(trade_info[2])
    stop_loss = float(trade_info[3])

    # Определяем направление сделки
    if trend == 1:
        direction = "long"
    elif trend == -1:
        direction = "short"
    else:
        direction = "neutral"

    # Проверяем, достигла ли цена лимитной отметки
    limit_reached = False

    for candle in candle_data:
        high = float(candle[2])
        low = float(candle[3])

        if direction == "long":
            if low <= entry_price:
                limit_reached = True
                break
        elif direction == "short":
            if high >= entry_price:
                limit_reached = True
                break
        elif direction == "neutral":
            if high >= entry_price or low <= entry_price:
                limit_reached = True
                break

    # Если лимитная отметка не достигнута, возвращаем результат
    if not limit_reached:
        return ["-", 0.0]

    # Проверяем, отработала ли сделка
    trade_successful = False
    profit_percentage = 0.0

    for candle in candle_data:
        high = float(candle[2])
        low = float(candle[3])

        if direction == "long":
            if high >= take_profit:
                trade_successful = True
                profit_percentage = (take_profit - entry_price) / entry_price * 100
                break
            elif low <= stop_loss:
                trade_successful = False
                profit_percentage = (stop_loss - entry_price) / entry_price * 100
                break
        elif direction == "short":
            if low <= take_profit:
                trade_successful = True
                profit_percentage = (entry_price - take_profit) / entry_price * 100
                break
            elif high >= stop_loss:
                trade_successful = False
                profit_percentage = (entry_price - stop_loss) / entry_price * 100
                break
        elif direction == "neutral":
            if high >= take_profit:
                trade_successful = True
                profit_percentage = (take_profit - entry_price) / entry_price * 100
                break
            elif low <= stop_loss:
                trade_successful = False
                profit_percentage = (stop_loss - entry_price) / entry_price * 100
                break

    # Формируем результат
    result_sign = "+" if trade_successful else "-"
    result = [result_sign, profit_percentage]

    return result



import pandas as pd
import numpy as np


def analyze_candlestick_data_m5(data):
    # Преобразование данных в DataFrame
    columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_volume']
    df = pd.DataFrame(data, columns=columns)

    # Преобразование строковых данных в числовые
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    df[['open', 'high', 'low', 'close', 'volume', 'quote_volume']] = df[['open', 'high', 'low', 'close', 'volume', 'quote_volume']].astype(float)

    # Анализ уровней поддержки и сопротивления
    support_levels = df['low'].rolling(window=20).min()  # Уровни поддержки за окно в 20 периодов
    resistance_levels = df['high'].rolling(window=20).max()  # Уровни сопротивления за окно в 20 периодов

    # Определение самых актуальных уровней
    current_support_level = support_levels.dropna().iloc[-1]
    current_resistance_level = resistance_levels.dropna().iloc[-1]

    # Преобразование результатов в словарь
    result = {
        'support_level': current_support_level,
        'resistance_level': current_resistance_level
    }

    return result


