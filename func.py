import google.generativeai as genai
from config import API_KEY
from datetime import datetime


def round_time_down():
    # Извлекаем минуты
    minutes = datetime.now().minute

    # Округляем минуты в меньшую сторону кратно 5
    rounded_minutes = (minutes // 5) * 5

    # Формируем новое время
    rounded_time = datetime.now().replace(minute=rounded_minutes, second=0, microsecond=0)

    return rounded_time.strftime("%H:%M")


def trend_ai(data):
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
        "Проведи данные через индикатор и используй все свои знания технического анализа(в том числе Фигуры технического анализа и Свечные паттерны) и скажи в каком направлени(up, down, 0) будет резкий скачок цены на следующих 5 свечах. Если не предвидится скачка то 0(если не предвидится движения от 2.5% тоже ставь 0).Ты можешь выбрать только один ответ из трех:\n//@version=4\nstudy(title=\"RSI iFish with Trend Lines\", shorttitle=\"RSI iFish\", overlay=false)\n\n// Входные параметры\nlength = input(14, title=\"RSI length\")\nlengthwma = input(7, title=\"Smoothing length\")\nprd = input(defval = 14, title=\"Pivot Point Period\", minval = 5, maxval = 50)\nPPnum = input(defval = 3, title=\"Number of Pivot Point to check\", minval = 2, maxval = 3)\n\n// Функция для расчета iFish\ncalc_ifish(series, lengthwma) =>\n    v1 = 0.1 * (series - 50)\n    v2 = wma(v1, lengthwma)\n    ifish = v2 * 2  // Линейная трансформация\n    ifish\n\n// Расчет RSI\nrsi_value = rsi(close, length)\n\n// Применение функции calc_ifish к RSI\nifish_value = calc_ifish(rsi_value, lengthwma)\n\n// Отображение значения iFish\nplot(ifish_value, color=color.white, title=\"RSI iFish\")\nhline(0, \"Zero Line\", color=#5e52ff, linestyle=hline.style_dotted)\n\n// Логика для трендовых линий\nfloat ph = na, float pl = na\nph := pivothigh(ifish_value, prd, prd)\npl := pivotlow(ifish_value, prd, prd)\n\ngetloc(bar_i)=>\n    _ret = bar_index + prd - bar_i\n\nt1pos = valuewhen(ph, bar_index, 0)\nt1val = nz(ifish_value[getloc(t1pos)])\nt2pos = valuewhen(ph, bar_index, 1)\nt2val = nz(ifish_value[getloc(t2pos)])\nt3pos = valuewhen(ph, bar_index, 2)\nt3val = nz(ifish_value[getloc(t3pos)])\n\nb1pos = valuewhen(pl, bar_index, 0)\nb1val = nz(ifish_value[getloc(b1pos)])\nb2pos = valuewhen(pl, bar_index, 1)\nb2val = nz(ifish_value[getloc(b2pos)])\nb3pos = valuewhen(pl, bar_index, 2)\nb3val = nz(ifish_value[getloc(b3pos)])\n\ngetloval(l1, l2)=>\n    _ret1 = l1 == 1 ? b1val : l1 == 2 ? b2val : l1 ==3 ? b3val : 0\n    _ret2 = l2 == 1 ? b1val : l2 == 2 ? b2val : l2 ==3 ? b3val : 0\n    [_ret1, _ret2]\n\ngetlopos(l1, l2)=>\n    _ret1 = l1 == 1 ? b1pos : l1 == 2 ? b2pos : l1 ==3 ? b3pos : 0\n    _ret2 = l2 == 1 ? b1pos : l2 == 2 ? b2pos : l2 ==3 ? b3pos : 0\n    [_ret1, _ret2]\n\ngethival(l1, l2)=>\n    _ret1 = l1 == 1 ? t1val : l1 == 2 ? t2val : l1 ==3 ? t3val : 0\n    _ret2 = l2 == 1 ? t1val : l2 == 2 ? t2val : l2 ==3 ? t3val : 0\n    [_ret1, _ret2]\n\ngethipos(l1, l2)=>\n    _ret1 = l1 == 1 ? t1pos : l1 == 2 ? t2pos : l1 ==3 ? t3pos :  0\n    _ret2 = l2 == 1 ? t1pos : l2 == 2 ? t2pos : l2 ==3 ? t3pos :  0\n    [_ret1, _ret2]\n\n// line definitions\nvar line l1 = na, var line l2 = na, var line l3 = na\nvar line t1 = na, var line t2 = na, var line t3 = na\n\ncountlinelo = 0\ncountlinehi = 0\nfor p1 = 1 to PPnum - 1\n    uv1 = 0.0\n    uv2 = 0.0\n    up1 = 0\n    up2 = 0\n    for p2 = PPnum to p1 + 1\n        [val1, val2] = getloval(p1, p2)\n        [pos1, pos2] = getlopos(p1, p2)\n        if val1 > val2\n            diff = (val1 - val2) / (pos1 - pos2)\n            hline = val2 + diff\n            lloc = bar_index\n            lval = ifish_value\n            valid = true\n            for x = pos2 + 1 - prd to bar_index\n                if nz(ifish_value[getloc(x + prd)]) < hline\n                    valid := false\n                lloc := x\n                lval := hline\n                hline := hline + diff\n\n            if valid\n                uv1 := hline\n                uv2 := val2\n                up1 := lloc\n                up2 := pos2\n                break\n    dv1 = 0.0\n    dv2 = 0.0\n    dp1 = 0\n    dp2 = 0\n    for p2 = PPnum to p1 + 1\n        [val1, val2] = gethival(p1, p2)\n        [pos1, pos2] = gethipos(p1, p2)\n        if val1 < val2\n            diff = (val2 - val1) / (pos1 - pos2)\n            hline = val2 - diff\n            lloc = bar_index\n            lval = ifish_value\n            valid = true\n            for x = pos2 + 1 - prd to bar_index\n                if nz(ifish_value[getloc(x + prd)]) > hline\n                    valid := false\n                    break\n                lloc := x\n                lval := hline\n                hline := hline - diff\n\n            if valid\n                dv1 := hline\n                dv2 := val2\n                dp1 := lloc\n                dp2 := pos2\n                break\n\n    if up1 != 0 and up2 != 0\n        countlinelo := countlinelo + 1\n        l1 := countlinelo == 1 ? line.new(up2 - prd, uv2, up1, uv1) : l1\n        l2 := countlinelo == 2 ? line.new(up2 - prd, uv2, up1, uv1) : l2\n        l3 := countlinelo == 3 ? line.new(up2 - prd, uv2, up1, uv1) : l3\n\n    if dp1 != 0 and dp2 != 0\n        countlinehi := countlinehi + 1\n        t1 := countlinehi == 1 ? line.new(dp2 - prd, dv2, dp1, dv1) : t1\n        t2 := countlinehi == 2 ? line.new(dp2 - prd, dv2, dp1, dv1) : t2\n        t3 := countlinehi == 3 ? line.new(dp2 - prd, dv2, dp1, dv1) : t3",
        "input: ",
        "output: 'up'",
        "input: ",
        "output: 'down'",
        f"input: ",
        "output: 0",
        f"input: {data}",
        "output: ",
    ])
    #print(data)

    # Вывод результата
    return response.text


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
    ema200 = calculate_ema(closes, 200)

    # Функция для определения результата
    def determine_result(ema20, ema50, ema200):
        if ema20 > ema50 > ema200:
            return 1
        elif ema20 < ema50 < ema200:
            return -1
        else:
            return 0
    # Определение результата для последнего значения
    result = determine_result(ema20[0], ema50[0], ema200[0])

    return result
