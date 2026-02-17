from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from database import save_user_profile
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

        user_data = await state.get_data()
        save_user_profile(
            user_id=message.from_user.id,
            height_cm=user_data.get("height"),
            weight_kg=user_data.get("weight"),
            goal=user_data.get("goal"),
            sex=user_data.get("sex"),
            birthdate=user_data.get("birthdate"),
            activity_level=user_data.get("activity_level")
        )


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

        user_data = await state.get_data()
        save_user_profile(
            user_id=message.from_user.id,
            height_cm=user_data.get("height"),
            weight_kg=user_data.get("weight"),
            goal=user_data.get("goal"),
            sex=user_data.get("sex"),
            birthdate=user_data.get("birthdate"),
            activity_level=user_data.get("activity_level")
        )


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

    user_data = await state.get_data()
    save_user_profile(
        user_id=message.from_user.id,
        height_cm=user_data.get("height"),
        weight_kg=user_data.get("weight"),
        goal=user_data.get("goal"),
        sex=user_data.get("sex"),
        birthdate=user_data.get("birthdate"),
        activity_level=user_data.get("activity_level")
    )

    
    await message.answer("Какой у вас пол?")
    await state.set_state(UserSurvey.waiting_for_sex)


    # # Отправляем подтверждение
    # await message.answer(
    #     f"Спасибо за ответы!\n"
    #     f"Ваш рост: {user_data['height']} см\n"
    #     f"Ваш вес: {user_data['weight']} кг\n"
    #     f"Ваша цель: {user_data['goal']}",
    #     reply_markup=types.ReplyKeyboardRemove()
    # )


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

        user_data = await state.get_data()
        save_user_profile(
            user_id=message.from_user.id,
            height_cm=user_data.get("height"),
            weight_kg=user_data.get("weight"),
            goal=user_data.get("goal"),
            sex=user_data.get("sex"),
            birthdate=user_data.get("birthdate"),
            activity_level=user_data.get("activity_level")
        )


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

    user_data = await state.get_data()
    save_user_profile(
        user_id=message.from_user.id,
        height_cm=user_data.get("height"),
        weight_kg=user_data.get("weight"),
        goal=user_data.get("goal"),
        sex=user_data.get("sex"),
        birthdate=user_data.get("birthdate"),
        activity_level=user_data.get("activity_level")
    )

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
        save_user_profile(
            user_id=message.from_user.id,
            height_cm=user_data.get("height"),
            weight_kg=user_data.get("weight"),
            goal=user_data.get("goal"),
            sex=user_data.get("sex"),
            birthdate=user_data.get("birthdate"),
            activity_level=user_data.get("activity_level")
        )

        await message.answer(
            f"Спасибо за ответы!\n"
            f"Ваш рост: {user_data['height']} см\n"
            f"Ваш вес: {user_data['weight']} кг\n"
            f"Ваша цель: {user_data['goal']}\n"
            f"Ваш пол: {user_data['sex']}\n"
            f"Ваш уровень активности: {user_data['activity_level']}\n"
            f"Ваша дата рождения: {user_data['birthdate']}",
            reply_markup=types.ReplyKeyboardRemove()
        )

        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите дату рождения в формате ГГГГ-ММ-ДД:")
