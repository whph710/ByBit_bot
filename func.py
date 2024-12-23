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
        
        ### Методы и подходы
        **Методы**: Использование индикаторов технического анализа, анализ свечных паттернов и фигур технического 
        анализа.
        **Подходы**: Анализ исторических данных, поиск паттернов и индикаторов, прогнозирование будущих движений цены.
        
        ### Выходные данные
        **Формат выходных данных**: Направление движения цены (1 для роста, -1 для падения, 0 для отсутствия движения), 
        три числа: точка входа, тейк-профит, стоп-лосс.
        **Примеры выходных данных**: [ 1, 100, 110, 95]
        
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
        f"input: {data2}",
        "output: ",
    ])
    data1 = json.loads(response.text)
    # Вывод результата
    return data1


def ema_trend(data):
    # Извлечение значений закрытия
    closes = [float(row[4]) for row in data]

    # Функция для вычисления EMA
    def calculate_ema(prices, period):
        multiplier = 2 / (period + 1)
        ema = [sum(prices[:period]) / period]
        for price in prices[period:]:
            ema.append((price - ema[-1]) * multiplier + ema[-1])
        return ema

    # Вычисление EMA для периодов 20, 50 и 200
    ema20 = calculate_ema(closes, 20)
    ema50 = calculate_ema(closes, 50)
    ema100 = calculate_ema(closes, 100)

    # Функция для определения результата
    def determine_result(ema20, ema50, ema100):
        if ema20 > ema50 > ema100:
            return 1
        elif ema20 < ema50 < ema100:
            return -1
        else:
            return 0

    # Определение результата для последнего значения
    result = determine_result(ema20[0], ema50[0], ema100[0])

    return result


def print_and_save_to_file(data):

    # Красивый вывод в файл
    if isinstance(data['response'], list) and len(data['response']) >= 4:
        choice = f"limit: {data['response'][1]}, tp: {data['response'][2]}, sl: {data['response'][3]}"
        difference = abs(float(data['response'][1]) - float(data['response'][2]))
        percentage_difference = (difference / abs(float(data['response'][1]))) * 100
        # Преобразование данных в строку для записи в файл
        data_str = (f"Ticket: {data['ticket']} Time: {data['time']}, "
                    f"Trend: {data['response'][0]},{choice} stonks: {percentage_difference}")
        # Запись данных в файл
        with open(r'C:\Users\maxim\Documents\PycharmProjects\ByBit_bot\Trade.txt', 'a', encoding='utf-8') as file:
            file.write(data_str + '\n')
    else:
        choice = f"response: {data['response']}"
        print(choice)

