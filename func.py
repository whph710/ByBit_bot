import pandas as pd
import numpy as np

def calculate_ifish_and_trends(close_prices, length, lengthwma, prd, PPnum):
    """
    Расчет iFish, пивотных точек и трендовых линий.
    """
    # Расчет RSI
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    # Преобразование для iFish
    v1 = 0.1 * (rsi - 50)
    v2 = v1.rolling(window=lengthwma).mean()
    ifish_values = 2 * v2

    # Нахождение пивотных точек
    pivot_highs = (ifish_values > ifish_values.shift(1)) & (ifish_values > ifish_values.shift(-1))
    pivot_lows = (ifish_values < ifish_values.shift(1)) & (ifish_values < ifish_values.shift(-1))

    # Выбор первых PPnum точек
    high_indices = ifish_values[pivot_highs].nlargest(PPnum).index
    low_indices = ifish_values[pivot_lows].nsmallest(PPnum).index

    # Генерация трендовых линий
    trend_lines_high = []
    for i in range(len(high_indices) - 1):
        trend_lines_high.append((high_indices[i], ifish_values[high_indices[i]],
                                 high_indices[i + 1], ifish_values[high_indices[i + 1]]))

    trend_lines_low = []
    for i in range(len(low_indices) - 1):
        trend_lines_low.append((low_indices[i], ifish_values[low_indices[i]],
                                low_indices[i + 1], ifish_values[low_indices[i + 1]]))

    # Проверка пересечения трендовой линии для последних трех значений
    last_three_ifish = ifish_values.iloc[-200:]
    trend_crossing = False

    for ifish_value in last_three_ifish:
        for line in trend_lines_high + trend_lines_low:
            x1, y1, x2, y2 = line
            if (x1 <= len(ifish_values) - 1 <= x2) or (x2 <= len(ifish_values) - 1 <= x1):
                y_interp = y1 + (y2 - y1) * (len(ifish_values) - 1 - x1) / (x2 - x1)
                if (ifish_value > y_interp and ifish_value <= y1) or (ifish_value < y_interp and ifish_value >= y1):
                    trend_crossing = True
                    break
        if trend_crossing:
            break

    return ifish_values, pivot_highs, pivot_lows, trend_lines_high, trend_lines_low, trend_crossing

def process_ifish_data(data, length=14, lengthwma=7, prd=14, PPnum=2):
    """
    Обрабатывает данные для расчета индикатора iFish и трендовых линий.

    :param data: Список строк данных [[timestamp, open, high, low, close, volume, quote_volume], ...]
    :param length: Период для RSI.
    :param lengthwma: Период сглаживания для iFish.
    :param prd: Период для пивотных точек.
    :param PPnum: Количество пивотных точек для проверки.
    :return: ifish_values, pivot_highs, pivot_lows, trend_lines_high, trend_lines_low, trend_crossing
    """
    # Создаем DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'quote_volume'])

    # Преобразуем данные
    df['timestamp'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    df[['open', 'high', 'low', 'close', 'volume', 'quote_volume']] = df[['open', 'high', 'low', 'close', 'volume', 'quote_volume']].astype(float)

    # Извлекаем цены закрытия
    close_prices = df['close']

    # Вызываем функцию расчета
    ifish_values, pivot_highs, pivot_lows, trend_lines_high, trend_lines_low, trend_crossing = calculate_ifish_and_trends(
        close_prices, length, lengthwma, prd, PPnum
    )
    print("iFish Values:", ifish_values)
    print("Pivot Highs:", pivot_highs)
    print("Pivot Lows:", pivot_lows)
    print("Trend Lines High:", trend_lines_high)
    print("Trend Lines Low:", trend_lines_low)
    print("Trend Crossing:", trend_crossing)

    #return ifish_values, pivot_highs, pivot_lows, trend_lines_high, trend_lines_low, trend_crossing
