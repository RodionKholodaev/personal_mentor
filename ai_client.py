# ai_client.py
import os
import json
import asyncio

from openai import AsyncOpenAI

from config import OPENROUTER_API_KEY



# Инициализация клиента OpenRouter (OpenAI-совместимый) [web:45][web:49][web:83]
# возможно будет не работать с openrouter
client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# нужно указывать системный промт, промт пользователя, модель и температуру
async def ask_llm(description: str, system_msg:str, model: str, temp: float = None) -> dict:
    print("попал в ask_llm")
    user_msg = description

    error = ""
    max_retries=3
    for i in range(max_retries):
        try:
            print("перед получением ответа")
            # Вызов chat completion через OpenRouter [web:45][web:49][web:76]
            response = await client.chat.completions.create(
                model=model, # google/gemini-2.0-flash-lite-001 - было так
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                # JSON-режим: просим модель возвращать JSON-объект [web:81][web:85]
                response_format={"type": "json_object"},
                max_tokens=200,
                temperature=temp,
            )
            print("после получения ответа")

            content: str = response.choices[0].message.content
            data = json.loads(content)

            print(data)

            return data  

        except Exception as e:
            print("попал в exception")
            # На проде лучше логировать ошибку
            error=e
            await asyncio.sleep(0.5)

    return error

async def make_week_plan(description: str, model:str, temperature: float) -> dict: 

    print("попал в make_week_plan")
    system_msg = """
    Ты — профессиональный диетолог и шеф-повар. Твоя задача: составить план питания на 7 дней (21 прием пищи: завтрак, обед, ужин).

    Данные пользователя:
    - Пол, возраст, рост, вес (для расчета КБЖУ).
    - Цель (похудение, набор массы, поддержание).
    - Предпочтения и аллергии (учитывай их строго).

    Требования к ответу:
    1. Ответ должен быть СТРОГО в формате JSON.
    2. Не пиши никакой лишний текст до или после JSON.
    3. Каждый рецепт должен быть уникальным и соответствовать целям пользователя.
    4. Используй русский язык для описаний.
    5. расписывай шаги подробно
    6. В конце JSON добавь объект "shopping_list".
    7. "shopping_list" должен содержать агрегированный список всех продуктов, необходимых для приготовления всех 21 блюда.
    8. Одинаковые продукты должны быть суммированы. Например, если лук встречается в 5 рецептах по 50г, в списке покупок должно быть: "item": "Лук", "amount": 250, "unit": "г".

    Структура JSON:
    {
    "weekly_plan": [
        {
        "day_number": 1,
        "meals": [
            {
            "type": "breakfast",
            "recipe": {
                "title": "Название блюда",
                "ingredients": ["ингредиент 1", "ингредиент 2"],
                "instructions": ["шаг 1", "шаг 2"],
                "nutrients": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
                "cooking_time_min": 20
            }
            },
            { "type": "lunch", "recipe": { ... } },
            { "type": "dinner", "recipe": { ... } }
        ]
        },
        "day_number": 2,
        "meals": [
            {
            "type": "breakfast",
            "recipe": {
                "title": "Название блюда",
                "ingredients": ["ингредиент 1", "ингредиент 2"],
                "instructions": ["шаг 1", "шаг 2"],
                "nutrients": {"kcal": 0, "protein": 0, "fat": 0, "carbs": 0},
                "cooking_time_min": 20
            }
            },
            { "type": "lunch", "recipe": { ... } },
            { "type": "dinner", "recipe": { ... } }
        ]
        },
        и так далее все 7 дней
    ]
    "shopping_list": [
    {
        "item": "Название продукта(например картошка)",
        "amount": 500,
        "unit": "г",
        "category": "Овощи"
    },
    {
        "item": "Название продукта(например помело)",
        "amount": 1,
        "unit": "шт",
        "category": "Фрукт"
    },
    и так далее все продукты что нужны для всех рецептов
    ]
    }
    Приемы пищи должны быть разнообразны и соответствовать пожеланиям пользователя!
    Давай правильн на калории, белки, жиры и углеводы
    """
    data = await ask_llm(description, system_msg, model = model, temp = temperature)
    return data
    

async def edit_week_plan(message:str, model:str, temperature:float) -> dict:
    """
    описание функции
    """
    system_msg = f'''
    
    '''
    description = message
    data = await ask_llm(description, system_msg, model, temperature)
    return data