import google.generativeai as genai
from config import token_gemini



def gemini_analyze(data):
    genai.configure(api_key=token_gemini)

    # Create the model
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.1,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    response = model.generate_content([data])

    return response




import asyncio
from openai import AsyncOpenAI
from config import OpenAI

# Создание клиента для взаимодействия с OpenAI
client = AsyncOpenAI(
    api_key=OpenAI,  # API ключ OpenAI
    )



# Функция для получения ответа от GPT
async def gpt_text(reg, model='gpt-4o'):

    # Создание запроса для получения ответа от GPT
    completion = await client.chat.completions.create(
        model=model,  # Модель GPT
        messages=[  # Сообщения для отправки GPT
            {"role": "user", "content": str(reg)}  # Сообщение от пользователя
        ]
    )
    # Возвращение ответа от GPT
    return {'response': completion.choices[0].message.content,
            'usage': completion.usage.total_tokens}

