import pandas as pd


def calculate_moving_averages(data, short_period=9, long_period=21):
    # Извлекаем только цены закрытия из данных
    close_prices = [float(entry[4]) for entry in data]

    # Функция для расчета скользящей средней
    def moving_average(prices, period):
        return [sum(prices[i:i+period]) / period for i in range(len(prices) - period + 1)]

    # Рассчитываем 9-периодную скользящую среднюю
    short_ma = [round(value, 8) for value in moving_average(close_prices, short_period)]

    # Рассчитываем 21-периодную скользящую среднюю
    long_ma = [round(value, 8) for value in moving_average(close_prices, long_period)]
    moving_average_result = {
        "moving_averages": f"{short_period}-{long_period}",
        "short_ma": short_ma,
        "long_ma": long_ma}

    return moving_average_result


def calculate_rsi(data, period=14):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'other'])

    # Преобразуем столбец 'close' в числовой формат
    df['close'] = df['close'].astype(float)

    # Вычисляем изменения цен
    df['delta'] = df['close'].diff(1)

    # Разделяем изменения на положительные и отрицательные
    df['gain'] = df['delta'].apply(lambda x: x if x > 0 else 0)
    df['loss'] = df['delta'].apply(lambda x: -x if x < 0 else 0)

    # Вычисляем средние значения для периода
    df['avg_gain'] = df['gain'].rolling(window=period).mean()
    df['avg_loss'] = df['loss'].rolling(window=period).mean()

    # Вычисляем RS (Relative Strength)
    df['rs'] = df['avg_gain'] / df['avg_loss']

    # Вычисляем RSI
    df['rsi'] = 100 - (100 / (1 + df['rs']))

    # Возвращаем список значений RSI
    rsi_values = df['rsi'].dropna().apply(lambda x: round(x, 8)).tolist()

    # Формируем результат в виде словаря
    rsi_result = {
        "rsi_param": f"period={period}",
        "rsi": rsi_values}

    return rsi_result


def calculate_adx(data, period=14):
    # Преобразование данных в DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_volume'])

    # Преобразование столбцов в числовые значения
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    # Расчет +DM, -DM, TR
    df['H-pH'] = df['high'] - df['high'].shift(1)
    df['pL-L'] = df['low'].shift(1) - df['low']
    df['+DM'] = df[['H-pH', 'pL-L']].max(axis=1)
    df['-DM'] = df[['pL-L', 'H-pH']].min(axis=1)
    df['+DM'] = df['+DM'].apply(lambda x: x if x > 0 else 0)
    df['-DM'] = df['-DM'].apply(lambda x: abs(x) if x < 0 else 0)

    df['TR'] = df[['high', 'close']].max(axis=1) - df[['low', 'close']].min(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()

    df['+DI'] = (df['+DM'].rolling(window=period).mean() / df['ATR']) * 100
    df['-DI'] = (df['-DM'].rolling(window=period).mean() / df['ATR']) * 100

    df['DX'] = (abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])) * 100
    df['ADX'] = df['DX'].rolling(window=period).mean()

    # Удаление NaN значений
    df = df.dropna(subset=['ADX'])

    # Преобразование результата в список значений
    adx_values = df['ADX'].apply(lambda x: round(x, 8)).tolist()

    # Форматирование результата
    adx_result = {
        "adx_param": f"period = {period}",
        "adx": adx_values}

    return adx_result


def calculate_stochastic_oscillator(data, k_period=14, d_period=3, slowing=3):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_volume'])

    # Преобразуем столбцы в числовые значения
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    # Рассчитываем %K
    df['L14'] = df['low'].rolling(window=k_period).min()
    df['H14'] = df['high'].rolling(window=k_period).max()
    df['%K'] = ((df['close'] - df['L14']) / (df['H14'] - df['L14'])) * 100

    # Рассчитываем %D
    df['%D'] = df['%K'].rolling(window=d_period).mean()

    # Рассчитываем Slow %D
    df['Slow %D'] = df['%D'].rolling(window=slowing).mean()

    # Удаляем NaN значения
    df.dropna(inplace=True)

    # Создаем словарь с результатами
    stochastic_result = {
        "stochastic_oscillator": f"k_period={k_period}, d_period={d_period}, slowing={slowing}",
        "k_line": df['%K'].apply(lambda x: round(x, 8)).tolist(),
        "d_line": df['%D'].apply(lambda x: round(x, 8)).tolist(),
        "slow_d_line": df['Slow %D'].apply(lambda x: round(x, 8)).tolist()
    }

    return stochastic_result


def calculate_volume(data):
    # Инициализация списка для хранения объемов
    volumes = []

    # Перебор данных и извлечение объема
    for entry in data:
        volume = float(entry[5])  # Объем находится на шестом месте в каждом подсписке
        volumes.append(round(volume, 8))

    # Создание словаря с результатами
    volume_result = {"volumes": volumes}

    return volume_result


def promt(data):
    strategy_description = {
        "описание": "Стратегия основана на использовании комбинации индикаторов для определения точек входа и выхода на 15-минутном таймфрейме. Основные условия для входа в сделку включают анализ скользящих средних, RSI, ADX, стохастического осциллятора и объема.",
        "timeframe": "15-минутный",
        "indicators": ["скользящие средние", "RSI", "ADX", "стохастический осциллятор", "объем"],
        "long_entry": {
            "мас": "9-периодная пересекает 21-периодную снизу вверх",
            "RSI": "ниже 30 и растет",
            "ADX": "выше 25",
            "стохастик": "ниже 20 и растет",
            "объем": "рост на момент пересечения",
            "лимит": None  # Укажите точку входа, если таковая имеется
        },
        "short_entry": {
            "мас": "9-периодная пересекает 21-периодную сверху вниз",
            "RSI": "выше 70 и падает",
            "ADX": "выше 25",
            "стохастик": "выше 80 и падает",
            "объем": "рост на момент пересечения",
        },
        "ТВОЙ ОТВЕТ ДОЛЖЕН БЫТЬ ВОТ В ТАКОМ ВИДЕ": "exit_conditions: {trade: long/short/none",
            "tp": "2.5-5% от точки входа",
            "sl": "1-2% от уровня входа",
            "limit": "Укажите точку входа, если таковая имеется",


        "data_for_analyze": data
    }

    return strategy_description
