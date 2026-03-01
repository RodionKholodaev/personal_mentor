from database import get_user_profile
import json


class MessageMaker:
    @staticmethod
    def get_user_description(user_id: int) -> str:

        user_profile = get_user_profile(user_id)

        # недописал нужно чтобы эта функция создавала полное описание пользователя для нейросети.
        description = f"""
        вот информация обо мне:
        пол: {user_profile.get('sex')}
        дата рождения: {user_profile.get('birthdate')}
        рост: {user_profile.get('height_cm')}
        вес: {user_profile.get('weight_kg')}
        уровень активности: {user_profile.get('activity_level')}
        цель: {user_profile.get('goal')}
        составь мне план питания на неделю
        """
        return description


    @staticmethod
    def get_previous_days(week_plan_list : list[dict]) -> str:
        dishes = ""
        for day in range(len(week_plan_list)):
            dishes += f"День {day+1}: \n"
            for dish in week_plan_list[day]["meals"]:
                dishes += f"{dish["type"]}: {dish["recipe"]["title"]} \n"

        return dishes

# функции ниже скороее всего нужно будет править!
    @staticmethod
    def get_day_plan(day_plan_json: dict) -> list[str]:
        """
        Преобразует JSON плана на день в список из 3-х красиво оформленных сообщений.
        """
        meal_messages = []
        
        # Словарь для красивых заголовков
        type_titles = {
            "breakfast": "🌅 ЗАВТРАК",
            "lunch": "☀️ ОБЕД",
            "dinner": "🌙 УЖИН"
        }

        for meal in day_plan_json.get("meals"):
            m_type = meal.get("type", "unknown")
            recipe = meal.get("recipe")
            
            title = recipe.get("title").upper()
            ingredients = recipe.get("ingredients")
            instructions = recipe.get("instructions")
            nutrients = recipe.get("nutrients")
            cooking_time = recipe.get("cooking_time_min")

            # Формируем текст одного приема пищи
            text = f"<b>{type_titles.get(m_type, m_type)}: {title}</b>\n"
            text += f"⏱ <i>Время приготовления: {cooking_time} мин.</i>\n\n"
            
            # Ингредиенты
            text += "<b>🛒 Ингредиенты:</b>\n"
            for ing in ingredients:
                text += f"• {ing}\n"
            
            # Инструкции
            text += "\n<b>👨‍🍳 Приготовление:</b>\n"
            for i, step in enumerate(instructions, 1):
                text += f"{i}. {step}\n"
            
            # КБЖУ
            text += "\n<b>📊 Пищевая ценность (на порцию):</b>\n"
            text += f"<code>Ккал: {nutrients.get('kcal', 0)} | Б: {nutrients.get('protein', 0)}г | Ж: {nutrients.get('fat', 0)}г | У: {nutrients.get('carbs', 0)}г</code>\n"
            # text += " —" * 10 # Визуальный разделитель

            meal_messages.append(text)

        return meal_messages
    

    @staticmethod
    def create_week_plan_message(day_plans: list[dict]) -> str:
        """
        Принимает список из 7 словарей (планов на день) 
        и упаковывает их в структуру "week_plan" с нумерацией дней.
        """
        week_plan_data = []
        
        for index, day_data in enumerate(day_plans, start=1):
            # Создаем структуру для конкретного дня
            day_entry = {
                "day": index,
                "meals": day_data.get("meals", [])
            }
            week_plan_data.append(day_entry)
        
        # Оборачиваем в финальный словарь
        final_structure = {
            "week_plan": week_plan_data
        }
        
        # Превращаем в строку. ensure_ascii=False нужен, чтобы кириллица не превратилась в \u044d
        return json.dumps(final_structure, ensure_ascii=False, indent=2)
    

    @staticmethod
    def get_shopping_list_text(shopping_list_json: dict) -> str:
        """
        Преобразует JSON списка покупок в структурированный текст по категориям.
        """
        items = shopping_list_json.get("shopping_list", [])
        if not items:
            return "🛒 Список покупок пуст."

        # Группируем продукты по категориям
        categories = {}
        for entry in items:
            cat = entry.get("category", "Прочее")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(entry)

        # Формируем сообщение
        msg_parts = ["<b>🛒 СПИСОК ПОКУПОК НА НЕДЕЛЮ</b>\n"]
        
        for category, products in categories.items():
            msg_parts.append(f"\n🔹 <b>{category.upper()}</b>")
            for p in products:
                name = p.get("item", "Неизвестно")
                amount = p.get("amount", "")
                unit = p.get("unit", "")
                # Добавляем пустой квадрат для чек-листа в Telegram
                msg_parts.append(f"☐ {name} — {amount} {unit}")
        
        msg_parts.append("\n<i>Проверьте наличие специй и масла дома!</i>")
        
        return "\n".join(msg_parts)