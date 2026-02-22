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
async def ask_llm(description: str, system_msg:str, model: str, temp: float) -> dict:
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
    сюда вставить системный промт
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