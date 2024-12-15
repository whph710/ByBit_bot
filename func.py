import google.generativeai as genai
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def gemini_1_5_flash(text):
    # Конфигурация API
    genai.configure(api_key="AIzaSyD9IYhnHAWWK2fAhHrMSf8jRYxvfc9HzDA")

    # Чтение содержимого файла
    try:
        with open(r'C:\Users\maxim\Documents\PycharmProjects\ByBit_bot\prompt.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError:
        return "Файл не найден."
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"

    # Объединение текста с содержимым файла
    combined_text = text + "\n" + file_content

    # Создание модели и генерация контента
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(combined_text)
        return response.text
    except Exception as e:
        return f"Ошибка при генерации контента: {e}"

import pandas as pd
import numpy as np


def calculate_ifish(rsi_values, lengthwma):
    v1 = 0.1 * (rsi_values - 50)
    v2 = v1.rolling(window=lengthwma).mean()  # Используем скользящее среднее для сглаживания
    ifish = v2 * 2  # Линейная трансформация
    return ifish

def pivot_points(series, prd):
    ph = series.rolling(window=prd, center=True).apply(lambda x: x.argmax() if x.argmax() == prd // 2 else np.nan, raw=False)
    pl = series.rolling(window=prd, center=True).apply(lambda x: x.argmin() if x.argmin() == prd // 2 else np.nan, raw=False)
    return ph, pl

def get_loc(series, index):
    return series.index[index]

def get_values(series, index1, index2):
    return series.iloc[index1], series.iloc[index2]

def draw_trend_lines(df, ifish_values, prd, PPnum):
    ph, pl = pivot_points(ifish_values, prd)

    t1pos = df.index[ph.dropna().index[0]]
    t1val = ifish_values[t1pos]
    t2pos = df.index[ph.dropna().index[1]]
    t2val = ifish_values[t2pos]
    t3pos = df.index[ph.dropna().index[2]]
    t3val = ifish_values[t3pos]

    b1pos = df.index[pl.dropna().index[0]]
    b1val = ifish_values[b1pos]
    b2pos = df.index[pl.dropna().index[1]]
    b2val = ifish_values[b2pos]
    b3pos = df.index[pl.dropna().index[2]]
    b3val = ifish_values[b3pos]

    trend_lines = []
    countlinelo = 0
    countlinehi = 0

    for p1 in range(1, PPnum):
        uv1 = 0.0
        uv2 = 0.0
        up1 = 0
        up2 = 0
        for p2 in range(PPnum, p1 + 1):
            val1, val2 = get_values(ifish_values, t1pos, t2pos)
            pos1, pos2 = get_loc(df.index, t1pos), get_loc(df.index, t2pos)
            if val1 > val2:
                diff = (val1 - val2) / (pos1 - pos2)
                hline = val2 + diff
                lloc = df.index[-1]
                lval = ifish_values.iloc[-1]
                valid = True
                for x in range(pos2 + 1 - prd, len(df)):
                    if ifish_values.iloc[x] < hline:
                        valid = False
                        break
                    lloc = df.index[x]
                    lval = hline
                    hline += diff

                if valid:
                    uv1 = hline
                    uv2 = val2
                    up1 = lloc
                    up2 = pos2
                    break

        dv1 = 0.0
        dv2 = 0.0
        dp1 = 0
        dp2 = 0
        for p2 in range(PPnum, p1 + 1):
            val1, val2 = get_values(ifish_values, b1pos, b2pos)
            pos1, pos2 = get_loc(df.index, b1pos), get_loc(df.index, b2pos)
            if val1 < val2:
                diff = (val2 - val1) / (pos1 - pos2)
                hline = val2 - diff
                lloc = df.index[-1]
                lval = ifish_values.iloc[-1]
                valid = True
                for x in range(pos2 + 1 - prd, len(df)):
                    if ifish_values.iloc[x] > hline:
                        valid = False
                        break
                    lloc = df.index[x]
                    lval = hline
                    hline -= diff

                if valid:
                    dv1 = hline
                    dv2 = val2
                    dp1 = lloc
                    dp2 = pos2
                    break

        if up1 != 0 and up2 != 0:
            countlinelo += 1
            trend_lines.append((up2, uv2, up1, uv1))

        if dp1 != 0 and dp2 != 0:
            countlinehi += 1
            trend_lines.append((dp2, dv2, dp1, dv1))

    return trend_lines

def analyze_trends(data, rsi_length=14, lengthwma=7, prd=14, PPnum=3):

    # Расчет RSI
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=rsi_length).mean()
    avg_loss = loss.rolling(window=rsi_length).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Расчет iFish
    ifish_values = calculate_ifish(rsi, lengthwma)

    # Построение трендовых линий
    trend_lines = draw_trend_lines(data, ifish_values, prd, PPnum)

    # Определение пересечений
    last_ifish = ifish_values.iloc[-1]
    cross_signal = None
    for line in trend_lines:
        x1, y1, x2, y2 = line
        if (last_ifish > y1 and last_ifish > y2) or (last_ifish < y1 and last_ifish < y2):
            cross_signal = 'upcross' if last_ifish > y1 and last_ifish > y2 else 'downcross'
            break

    return trend_lines, cross_signal

