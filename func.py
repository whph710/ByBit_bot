import google.generativeai as genai
from config import API_KEY
from datetime import datetime
import json
from google.ai.generativelanguage_v1beta.types import content



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
    data1 = json.loads(response.text)
    # Вывод результата
    return data1





def generate_response(input_data):
    # Install an additional SDK for JSON schema support Google AI Python SDK
    # pip install google.ai.generativelanguage
    # Replace with your actual API key
    genai.configure(api_key=API_KEY)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            properties = {
                "response": content.Schema(
                    type = content.Type.ARRAY,
                    items = content.Schema(
                        type = content.Type.STRING,
                    ),
                ),
            },
        ),
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    response = model.generate_content([
        "Используй все свои знания технического анализа(в том числе Фигуры технического анализа, ценовые уровни, уровни объема) и на основе этого  входящие данные: 'response' - это предположение куда пойдет цена, 'trend' - отображает отношение EMA20\\EMA50\\EMA100, \"-1 \" это EMA20",
        "input: Если точки входа в позицию для получения прибыли ИМЕЮТСЯ",
        "output: {\"limit\": *, \"tp\": *, \"sl\": *}",
        "input: Если точек входа в позицию для получения прибыли НЕ ИМЕЮТСЯ",
        "output: {\"limit\": None, \"tp\": None, \"sl\": None}",
        "input: {'response': ['down'], 'trend': 0, 'ticket': '1INCHUSDT', 'time': '18:00', 'kline': [['1734786000000', '0.3949', '0.3965', '0.3944', '0.3961', '95126.6', '37600.77658'], ['1734785700000', '0.3977', '0.3979', '0.3948', '0.3949', '108545.9', '42988.69038'], ['1734785400000', '0.3969', '0.3992', '0.3954', '0.3977', '256054.7', '101700.07465'], ['1734785100000', '0.3964', '0.3988', '0.3961', '0.3969', '190002.7', '75491.44256'], ['1734784800000', '0.3973', '0.3992', '0.3961', '0.3964', '257402.5', '102341.85054'], ['1734784500000', '0.399', '0.399', '0.3957', '0.3973', '319704.6', '126968.42584'], ['1734784200000', '0.4016', '0.4016', '0.3979', '0.399', '393056.5', '156880.32561'], ['1734783900000', '0.4043', '0.4046', '0.401', '0.4016', '154317.8', '62008.38936'], ['1734783600000', '0.4058', '0.4058', '0.4039', '0.4043', '162229.7', '65731.49916'], ['1734783300000', '0.403', '0.4063', '0.4028', '0.4058', '308897.4', '125081.10871'], ['1734783000000', '0.4024', '0.404', '0.4011', '0.403', '406162.7', '163588.70671'], ['1734782700000', '0.4057', '0.4058', '0.4013', '0.4024', '523828.7', '210822.53926'], ['1734782400000', '0.4081', '0.4081', '0.4052', '0.4057', '60763.9', '24690.81886'], ['1734782100000', '0.4081', '0.4085', '0.4078', '0.4081', '14954.8', '6102.55914'], ['1734781800000', '0.407', '0.4081', '0.4069', '0.4081', '9977.2', '4066.71043'], ['1734781500000', '0.4079', '0.4089', '0.4069', '0.407', '27877.4', '11369.74433'], ['1734781200000', '0.4081', '0.4086', '0.4078', '0.4079', '16281.6', '6644.89961'], ['1734780900000', '0.4062', '0.4087', '0.4059', '0.4081', '48532.4', '19760.81635'], ['1734780600000', '0.4044', '0.4064', '0.4032', '0.4062', '141467.5', '57228.56168'], ['1734780300000', '0.4065', '0.4065', '0.4034', '0.4044', '112584.6', '45574.41983'], ['1734780000000', '0.4087', '0.4091', '0.4065', '0.4065', '65989.5', '26880.57142'], ['1734779700000', '0.4084', '0.4089', '0.4083', '0.4087', '17645.9', '7211.5934'], ['1734779400000', '0.4094', '0.4094', '0.4079', '0.4084', '11101.8', '4534.5024'], ['1734779100000', '0.4091', '0.4099', '0.4086', '0.4094', '22170.8', '9074.84032'], ['1734778800000', '0.4091', '0.41', '0.4088', '0.4091', '32355.6', '13251.4274'], ['1734778500000', '0.4085', '0.4092', '0.4077', '0.4091', '25203.4', '10292.05835'], ['1734778200000', '0.4087', '0.4093', '0.4085', '0.4085', '28300.3', '11574.39843'], ['1734777900000', '0.4075', '0.4092', '0.4073', '0.4087', '25335.1', '10343.73186'], ['1734777600000', '0.4079', '0.4084', '0.4071', '0.4075', '43840.7', '17869.85213'], ['1734777300000', '0.4107', '0.4107', '0.4075', '0.4079', '78129', '31936.64309'], ['1734777000000', '0.4126', '0.4127', '0.4104', '0.4107', '51325.6', '21116.69579'], ['1734776700000', '0.4109', '0.4127', '0.4109', '0.4126', '31735.7', '13067.29851'], ['1734776400000', '0.4097', '0.4112', '0.4096', '0.4109', '99067.5', '40695.36239'], ['1734776100000', '0.4096', '0.4098', '0.409', '0.4097', '13849.4', '5671.79523'], ['1734775800000', '0.4085', '0.4098', '0.4083', '0.4096', '45232', '18529.73263'], ['1734775500000', '0.4091', '0.4091', '0.4077', '0.4085', '60281.2', '24617.66751'], ['1734775200000', '0.4085', '0.4093', '0.4076', '0.4091', '46648.4', '19067.79212'], ['1734774900000', '0.409', '0.4091', '0.4082', '0.4085', '15771.1', '6444.60384'], ['1734774600000', '0.4085', '0.4095', '0.4085', '0.409', '29874.1', '12219.94425'], ['1734774300000', '0.4078', '0.4085', '0.4064', '0.4085', '51323.9', '20903.39785'], ['1734774000000', '0.4091', '0.4091', '0.4076', '0.4078', '30004.9', '12250.5296'], ['1734773700000', '0.4085', '0.4097', '0.4084', '0.4091', '58058.5', '23747.65337'], ['1734773400000', '0.4076', '0.4086', '0.4065', '0.4085', '50644.6', '20665.60873'], ['1734773100000', '0.4064', '0.4078', '0.4064', '0.4076', '20405.8', '8305.4776'], ['1734772800000', '0.4052', '0.407', '0.4049', '0.4064', '32407.3', '13154.96767'], ['1734772500000', '0.4062', '0.4075', '0.4052', '0.4052', '62026.6', '25211.90184'], ['1734772200000', '0.4055', '0.4075', '0.4052', '0.4062', '60900.9', '24757.04861'], ['1734771900000', '0.4085', '0.4085', '0.4053', '0.4055', '191567.4', '77821.8477'], ['1734771600000', '0.4089', '0.4101', '0.4068', '0.4085', '71884.2', '29342.99252'], ['1734771300000', '0.41', '0.4102', '0.4089', '0.4089', '119013.3', '48760.88105']]}"
        "output:  {\"limit\": \"0.3950\",\"tp\": \"0.3920\",\"sl\": \"0.3975\"} ",
        "input: " + str(input_data),
        "output: ",
    ])
    data1 = json.loads(response.text)
    # Вывод результата
    return data1['response']



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
