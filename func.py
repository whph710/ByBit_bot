import google.generativeai as genai


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


# Пример использования функции
text = "2"
result = gemini_1_5_flash(text)
print(result)
