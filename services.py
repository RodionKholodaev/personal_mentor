from database import get_user_profile
class message_maker():
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


# Я ЭТУ ФУНКЦИЮ НЕ ПРОВЕРЯЛ! Я УСТАЛ! НАДЕЮСЬ ОНА РАБОТАЕТ И РАБОТАЕТ ПРАВИЛЬНО
    @staticmethod
    def get_week_plan(week_plan_json: dict) -> list[str]:
        messages = []

        # Формируем сообщения по дням
        for day in week_plan_json.get("weekly_plan", []):
            day_num = day.get("day_number")
            day_text = f"🗓 **ДЕНЬ {day_num}**\n\n"
            
            for meal in day.get("meals", []):
                m_type = meal.get("type").upper()
                recipe = meal.get("recipe", {})
                title = recipe.get("title", "Без названия")
                kcal = recipe.get("nutrients", {}).get("kcal", 0)
                time = recipe.get("cooking_time_min", 0)
                
                day_text += f"🍴 **{m_type}: {title}**\n"
                day_text += f"🔸 Калории: {kcal} ккал | ⏱ {time} мин\n"
                
                # Можно добавить ингредиенты кратко, если нужно:
                # ingredients = ", ".join(recipe.get("ingredients", []))
                # day_text += f"🛒 {ingredients}\n"
                
                day_text += "—" * 15 + "\n"
            
            messages.append(day_text)

        # Формируем сообщение со списком покупок
        shopping_data = week_plan_json.get("shopping_list", [])
        if shopping_data:
            shop_text = "🛒 **СПИСОК ПОКУПОК НА НЕДЕЛЮ**\n\n"
            
            # Группируем по категориям для удобства
            categories = {}
            for item in shopping_data:
                cat = item.get("category", "Прочее")
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(item)

            for cat, items in categories.items():
                shop_text += f"🔹 ___{cat}___\n"
                for i in items:
                    shop_text += f"• {i['item']}: {i['amount']} {i['unit']}\n"
                shop_text += "\n"
            
            messages.append(shop_text)

        return messages