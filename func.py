import google.generativeai as genai
from config import API_KEY
import json
from datetime import datetime

def gpt_analyze(data):
    genai.configure(api_key=API_KEY)

    # Create the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    with open(r'C:\Users\maxim\Documents\PycharmProjects\ByBit_bot\prompt.txt', 'r', encoding='utf-8') as file:
        prompt = file.read()


    # Generate content
    response = model.generate_content([
        f"{prompt}",
        "input: [['1734607800000', '1.3149', '1.3151', '1.3133', '1.3133', '5550.9', '7294.33406'], ['1734607500000', '1.319', '1.32', '1.3149', '1.3149', '68239.8', '89926.76906'], ['1734607200000', '1.315', '1.3206', '1.3143', '1.319', '88051.2', '116055.67918'], ['1734606900000', '1.306', '1.3169', '1.3055', '1.315', '77597.5', '101715.94661'], ['1734606600000', '1.314', '1.3175', '1.313', '1.3155', '65432.1', '86037.48321'], ['1734606300000', '1.3155', '1.318', '1.314', '1.316', '54321.0', '71537.48321'], ['1734606000000', '1.316', '1.3185', '1.3145', '1.317', '43210.9', '57037.48321'], ['1734605700000', '1.317', '1.319', '1.315', '1.3175', '32109.8', '42537.48321'], ['1734605400000', '1.3175', '1.3195', '1.316', '1.318', '21098.7', '27937.48321'], ['1734605100000', '1.318', '1.32', '1.3165', '1.3185', '10987.6', '14437.48321']...['1734593400000', '1.3375', '1.3395', '1.336', '1.338', '0.7', '107.48321']]",
        "output: {\n  \"analysis\": {\n    \"moving_averages\": {\n      \"short_ma\": 1.315,\n      \"long_ma\": 1.314,\n      \"signal\": \"long\"\n    },\n    \"rsi\": {\n      \"value\": 50,\n      \"signal\": \"neutral\"\n    },\n    \"adx\": {\n      \"value\": 25,\n      \"signal\": \"strong_trend\"\n    },\n    \"stochastic_oscillator\": {\n      \"k_line\": 20,\n      \"d_line\": 22,\n      \"signal\": \"long\"\n    },\n    \"trend_lines\": {\n      \"support_level\": 1.310,\n      \"resistance_level\": 1.320,\n      \"signal\": \"strong_movement\"\n    }\n  },\n  \"trade_recommendation\": {\n    \"entry_point\": 1.314,\n    \"stop_loss\": 1.309,\n    \"take_profit\": 1.355,\n    \"direction\": \"long\"\n  }\n}",
        "input: \"input\": [\n  ['1734607800000', '340.13', '340.57', '339.97', '340.0', '5550.9', '1887310.9703'],\n  ['1734607500000', '341.9', '342.0', '340.57', '340.57', '68239.8', '23309731.06906'],\n  ['1734607200000', '340.5', '342.06', '340.43', '341.9', '88051.2', '29969839.1818'],\n  ['1734606900000', '340.6', '341.69', '340.55', '341.5', '77597.5', '26454531.661'],\n  ['1734606600000', '341.3', '341.6', '340.6', '341.3', '65432.1', '22332995.33406'],\n  ['1734606300000', '341.9', '342.0', '341.3', '341.9', '78901.2', '26930747.67918'],\n  ['1734606000000', '340.5', '341.5', '340.43', '340.5', '88051.2', '29969839.1818'],\n  ['1734605700000', '341.6', '341.79', '341.55', '341.6', '77597.5', '26454531.661'],\n  ['1734605400000', '340.13', '340.57', '339.97', '340.0', '5550.9', '1887310.9703'],\n  ['1734605100000', '341.9', '342.0', '340.57', '340.57', '68239.8', '23309731.06906']...['1734593700000', '341.6', '341.79', '341.55', '341.6', '77597.5', '26454531.661']\n]",
        "output: {\n  \"analysis\": {\n    \"moving_averages\": {\n      \"short_ma\": 342.13,\n      \"long_ma\": 340.57,\n      \"signal\": \"short\"\n    },\n    \"rsi\": {\n      \"value\": 50,\n      \"signal\": \"neutral\"\n    },\n    \"adx\": {\n      \"value\": 25,\n      \"signal\": \"strong_trend\"\n    },\n    \"stochastic_oscillator\": {\n      \"k_line\": 80,\n      \"d_line\": 78,\n      \"signal\": \"short\"\n    },\n    \"trend_lines\": {\n      \"support_level\": 342.0,\n      \"resistance_level\": 340.0,\n      \"signal\": \"strong_movement\"\n    }\n  },\n  \"trade_recommendation\": {\n    \"entry_point\": 340.57,\n    \"stop_loss\": 341.77,\n    \"take_profit\": 335.17,\n    \"direction\": \"short\"\n  }\n}",
        "input: [\n  ['1734607800000', '1.3149', '1.3151', '1.3133', '1.3133', '5550.9', '7294.33406'],\n  ['1734607500000', '1.319', '1.32', '1.3149', '1.3149', '68239.8', '89926.76906'],\n  ['1734607200000', '1.315', '1.3206', '1.3143', '1.319', '88051.2', '116055.67918'],\n  ['1734606900000', '1.306', '1.3169', '1.3055', '1.315', '77597.5', '101715.94661'],\n  ['1734606600000', '1.314', '1.3175', '1.313', '1.3155', '65432.1', '86037.48321'],\n  ['1734606300000', '1.3155', '1.318', '1.314', '1.316', '54321.0', '71537.48321'],\n  ['1734606000000', '1.316', '1.3185', '1.3145', '1.317', '43210.9', '57037.48321'],\n  ['1734605700000', '1.317', '1.319', '1.315', '1.3175', '32109.8', '42537.48321'],\n  ['1734605400000', '1.3175', '1.3195', '1.316', '1.318', '21098.7', '27937.48321'],\n  ['1734605100000', '1.318', '1.32', '1.3165', '1.3185', '10987.6', '14437.48321'],\n  ['1734604800000', '1.3185', '1.3205', '1.317', '1.319', '9876.5', '12937.48321'],\n  ['1734604500000', '1.319', '1.321', '1.3175', '1.3195', '8765.4', '11537.48321'],\n  ['1734604200000', '1.3195', '1.3215', '1.318', '1.32', '7654.3', '10037.48321'],\n  ['1734603900000', '1.32', '1.322', '1.3185', '1.3205', '6543.2', '8637.48321'],\n  ['1734603600000', '1.3205', '1.3225', '1.319', '1.321', '5432.1', '7137.48321'],\n  ['1734603300000', '1.321', '1.323', '1.3195', '1.3215', '4321.0', '5737.48321'],\n  ['1734603000000', '1.3215', '1.3235', '1.32', '1.322', '3210.9', '4237.48321'],\n  ['1734602700000', '1.322', '1.324', '1.3205', '1.3225', '2109.8', '2737.48321'],\n  ['1734602400000', '1.3225', '1.3245', '1.321', '1.323', '1098.7', '1437.48321'],\n  ['1734602100000', '1.323', '1.325', '1.3215', '1.3235', '987.6', '1237.48321'],\n  ['1734601800000', '1.3235', '1.3255', '1.322', '1.324', '876.5', '1137.48321'],\n  ['1734601500000', '1.324', '1.326', '1.3225', '1.3245', '765.4', '1037.48321'],\n  ['1734601200000', '1.3245', '1.3265', '1.323', '1.325', '654.3', '887.48321'],\n  ['1734600900000', '1.325', '1.327', '1.3235', '1.3255', '543.2', '737.48321'],\n  ['1734600600000', '1.3255', '1.3275', '1.324', '1.326', '432.1', '587.48321'],\n  ['1734600300000', '1.326', '1.328', '1.3245', '1.3265', '321.0', '437.48321'],\n  ['1734600000000', '1.3265', '1.3285', '1.325', '1.327', '210.9', '287.48321'],\n  ['1734599700000', '1.327', '1.329', '1.3255', '1.3275', '109.8', '157.48321'],\n  ['1734599400000', '1.3275', '1.3295', '1.326', '1.328', '98.7', '137.48321'],\n  ['1734599100000', '1.328', '1.33', '1.3265', '1.3285', '87.6', '117.48321'],\n  ['1734598800000', '1.3285', '1.3305', '1.327', '1.329', '76.5', '107.48321'],\n  ['1734598500000', '1.329', '1.331', '1.3275', '1.3295', '65.4', '887.48321'],\n  ['1734598200000', '1.3295', '1.3315', '1.328', '1.33', '54.3', '737.48321'],\n  ['1734597900000', '1.33', '1.332', '1.3285', '1.3305', '43.2', '587.48321'],\n  ['1734597600000', '1.3305', '1.3325', '1.329', '1.331', '32.1', '437.48321'],\n  ['1734597300000', '1.331', '1.333', '1.3295', '1.3315', '21.0', '287.48321'],\n  ['1734597000000', '1.3315', '1.3335', '1.33', '1.332', '10.9', '157.48321'],\n  ['1734596700000', '1.332', '1.334', '1.3305', '1.3325', '9.8', '137.48321'],\n  ['1734596400000', '1.3325', '1.3345', '1.331', '1.333', '8.7', '117.48321'],\n  ['1734596100000', '1.333', '1.335', '1.3315', '1.3335', '7.6', '107.48321'],\n  ['1734595800000', '1.3335', '1.3355', '1.332', '1.334', '6.5', '887.48321'],\n  ['1734595500000', '1.334', '1.336', '1.3325', '1.3345', '5.4', '737.48321'],\n  ['1734595200000', '1.3345', '1.3365', '1.333', '1.335', '4.3', '587.48321'],\n  ['1734594900000', '1.335', '1.337', '1.3335', '1.3355', '3.2', '437.48321'],\n  ['1734594600000', '1.3355', '1.3375', '1.334', '1.336', '2.1', '287.48321'],\n  ['1734594300000', '1.336', '1.338', '1.3345', '1.3365', '1.0', '157.48321'],\n  ['1734594000000', '1.3365', '1.3385', '1.335', '1.337', '0.9', '137.48321'],\n  ['1734593700000', '1.337', '1.339', '1.3355', '1.3375', '0.8', '117.48321'],\n  ['1734593400000', '1.3375', '1.3395', '1.336', '1.338', '0.7', '107.48321']\n]\n```",
        "output: {\n  \"analysis\": {NULL}\n}",
        f"input: {data},"
        "output: ",
    ])
    # Убираем лишние символы в одной строке
    cleaned_text = response.text.replace("\n", "").replace("\t", "").replace("`", "").replace("json", "").replace("  ", " ")

    # Преобразуем строку в словарь
    data1 = json.loads(cleaned_text)

    # Добавляем сигналы в словарь

    check_gpt = generate_signal_score(data1)
    data = add_strength_to_trade_recommendation(data1, check_gpt)

    return data


def get_all_signals(data):
    signals = []

    # Извлечение сигналов из анализа
    analysis = data.get('analysis', {})
    for key, value in analysis.items():
        if 'signal' in value:
            signals.append(value['signal'])

    # Извлечение сигналов из торговых рекомендаций
    trade_recommendation = data.get('trade_recommendation', {})
    if 'direction' in trade_recommendation:
        signals.append(trade_recommendation['direction'])

    return signals


def generate_signal_score(input_list):
    # Настройка API ключа
    genai.configure(api_key=API_KEY)

    # Создание конфигурации генерации
    generation_config = {
        "temperature": 0,
        "top_p": 0,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Создание модели
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    # Формирование входных данных для модели
    prompt = [
        "Вам будет предоставлен список сигналов, посмотри предоставленный список сигналов.Общий сигнал: Определите один общий сигнал на основе анализа.Оцените общий сигнал по шкале от 0 до 10. и дай только эту цифру",
        "input: ['long', 'neutral', 'strong_trend', 'long', 'strong_movement', 'long']",
        "output: 8",
        "input: ['short', 'neutral', 'weak_trend', 'short', 'weak_movement', 'short']",
        "output: 3",
        f"input: {input_list}",
        "output: ",
    ]

    # Генерация ответа
    response = model.generate_content(prompt)

    # Возврат текста ответа
    return response.text.replace("\n", "")


def add_strength_to_trade_recommendation(data, strength_value):
    # Проверяем, существует ли ключ 'trade_recommendation' в данных
    if 'trade_recommendation' in data:
        # Добавляем пару 'strength' и значение strength_value в 'trade_recommendation'
        data['trade_recommendation']['strength'] = strength_value
    else:
        # Если ключа 'trade_recommendation' нет, создаем его и добавляем пару 'strength'
        data['trade_recommendation'] = {'strength': strength_value}
    return data


def round_time_down():
    # Извлекаем минуты
    minutes = datetime.now().minute

    # Округляем минуты в меньшую сторону кратно 5
    rounded_minutes = (minutes // 5) * 5

    # Формируем новое время
    rounded_time = datetime.now().replace(minute=rounded_minutes, second=0, microsecond=0)

    return rounded_time.strftime("%H:%M")