from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services import MessageMaker
from ai_client import make_day_plan, make_shoping_list
from database import save_user_profile, register_user_if_not_exists, get_user_id_by_tgid
# Создаем роутер
router = Router()


# Определяем состояния FSM
class UserSurvey(StatesGroup):
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_goal = State()
    waiting_for_sex = State()
    waiting_for_activity_level = State()
    waiting_for_birthdate = State()

# Хэндлер для старта опроса
@router.message(Command("start"))
async def start_survey(message: types.Message, state: FSMContext):
    register_user_if_not_exists(message.from_user.id) # сохраняем пользователя в таблицу users
    await message.answer("Привет! Давайте начнем опрос. Укажите ваш рост (в см):")
    await state.set_state(UserSurvey.waiting_for_height)

# Хэндлер для получения роста
@router.message(UserSurvey.waiting_for_height)
async def get_height(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        height = int(message.text)
        await state.update_data(height=height)

        await message.answer("Отлично! Теперь укажите ваш вес (в кг):")
        await state.set_state(UserSurvey.waiting_for_weight)
    except ValueError:
        await message.answer("Пожалуйста, введите число. Укажите ваш рост (в см):")

# Хэндлер для получения веса
@router.message(UserSurvey.waiting_for_weight)
async def get_weight(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        weight = float(message.text)
        await state.update_data(weight=weight)

        await message.answer("Какая у вас цель? Например: похудение, набор массы, поддержание формы.")
        await state.set_state(UserSurvey.waiting_for_goal)
    except ValueError:
        await message.answer("Пожалуйста, введите число. Укажите ваш вес (в кг):")

# Хэндлер для получения цели
@router.message(UserSurvey.waiting_for_goal)
async def get_goal(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=types.ReplyKeyboardRemove())
        return

    goal = message.text
    await state.update_data(goal=goal)
    
    await message.answer("Какой у вас пол?")
    await state.set_state(UserSurvey.waiting_for_sex)



    # Хэндлер для получения пола
@router.message(UserSurvey.waiting_for_sex)
async def get_weight(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        sex = message.text
        await state.update_data(sex=sex)

        await message.answer("Какой у вас уровень активности?")
        await state.set_state(UserSurvey.waiting_for_activity_level)
    except ValueError:
        await message.answer("Пожалуйста, введите ваш пол")

# Хэндлер для получения уровня активности
@router.message(UserSurvey.waiting_for_activity_level)
async def get_activity_level(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=types.ReplyKeyboardRemove())
        return

    activity_level = message.text
    await state.update_data(activity_level=activity_level)


    await message.answer("Укажите вашу дату рождения в формате ГГГГ-ММ-ДД:")
    await state.set_state(UserSurvey.waiting_for_birthdate)

# Хэндлер для получения даты рождения
@router.message(UserSurvey.waiting_for_birthdate)
async def get_birthdate(message: types.Message, state: FSMContext):
    if message.text.lower() == "отмена":
        await state.clear()
        await message.answer("Опрос отменен.", reply_markup=types.ReplyKeyboardRemove())
        return

    try:
        birthdate = message.text
        # Здесь можно добавить проверку формата даты, если необходимо
        await state.update_data(birthdate=birthdate)

        user_data = await state.get_data()
        user_id = get_user_id_by_tgid(message.from_user.id)
        save_user_profile(
            user_id=user_id,
            height_cm=user_data.get("height"),
            weight_kg=user_data.get("weight"),
            goal=user_data.get("goal"),
            sex=user_data.get("sex"),
            birthdate=user_data.get("birthdate"),
            activity_level=user_data.get("activity_level")
        )

        await message.answer("Формирую план питания, это займёт ~1 минуту")

        description = MessageMaker.get_user_description(message.from_user.id)
        model = 'google/gemini-2.0-flash-lite-001'
        temperature = None

        # вывод всех блюд на неделю
        week_plan_list = []
        for day in range(7):
            day_plan_json = await make_day_plan(description,model, temperature)

            week_plan_list.append(day_plan_json)

            plan_messages = MessageMaker.get_day_plan(day_plan_json)

            for msg_text in plan_messages:
                await message.answer(msg_text, parse_mode="HTML")
        # формирование описания все неделе для отдачи в нейросеть
        description_shoping_list = MessageMaker.create_week_plan_message(week_plan_list)
        # получение списка покупок
        shoping_list_dict = await make_shoping_list(description_shoping_list,model, temperature)
        # список покупок в виде текста
        shoping_list_text = MessageMaker.get_shopping_list_text(shoping_list_dict)
        # вывод списка покупок
        await message.answer(shoping_list_text,parse_mode="HTML")


        await state.clear()
    except ValueError: # проверки формата нет!
        await message.answer("Пожалуйста, введите дату рождения в формате ГГГГ-ММ-ДД:")
    
    except Exception as e:
        await state.clear()
        await message.answer(f"Просим прощение! Неизвестная ошибка при создании ответа. Текст ошибки: {e}. Это сообщение нужно потом убрать. Вы можете начнать диалог снова с команды /start")
