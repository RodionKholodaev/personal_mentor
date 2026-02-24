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
                max_tokens=20000,
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

async def make_day_plan(description: str, model:str, temperature: float) -> dict: 

    print("попал в make_day_plan")
    system_msg = """
    Ты — профессиональный диетолог и шеф-повар. Твоя задача: составить план питания на 1 днень (3 приема пищи: завтрак, обед, ужин).

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

    Структура JSON:
    {
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
    }
    Приемы пищи должны быть разнообразны и соответствовать описанию пользователя!
    Давай правильн на калории, белки, жиры и углеводы
    """
    data = await ask_llm(description, system_msg, model = model, temp = temperature)
    return data
    

async def make_shoping_list(description: str, model:str, temperature: float) -> dict:
    system_msg="""
    Ты — логист по закупкам.
    Твоя задача — проанализировать предоставленный план питания на 7 дней (21 прием пищи) и составить консолидированный список покупок.
    Инструкции:

    Суммирование:
    Найди одинаковые продукты во всех рецептах и суммируй их количество или вес.

    Конвертация:
    Приводи единицы измерения к единому стандарту (например, если в одном рецепте 200 г моркови, а в другом 1 кг — в списке должно быть 1.2 кг).

    Категоризация:
    Распредели продукты по логическим категориям (Овощи, Фрукты, Мясо и птица, Бакалея, Молочные продукты и т.д.).

    Точность:
    Учитывай мелкие ингредиенты (специи, масла, соусы), если они указаны в рецептах.

    Формат:
    Выдавай ответ строго в формате JSON. Не добавляй никаких вступительных или заключительных фраз.

    Формат вывода:
    {
    "shopping_list": [
        {
        "item": "Название продукта",
        "amount": число,
        "unit": "единица измерения (г, шт, мл, кг)",
        "category": "Категория"
        },
        {
        "item": "Название продукта",
        "amount": число,
        "unit": "единица измерения (г, шт, мл, кг)",
        "category": "Категория"
        },
        и так далее все продукты что нужны для всех рецептов
    ]
    }
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


