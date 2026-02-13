from aiogram import Router, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

# Создаем роутер
router = Router()

# Определяем состояния FSM
class UserSurvey(StatesGroup):
    waiting_for_height = State()
    waiting_for_weight = State()
    waiting_for_goal = State()

# Клавиатура для отмены
cancel_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Отмена"))

# Хэндлер для старта опроса
@router.message(Command("start"))
async def start_survey(message: types.Message):
    await message.answer("Привет! Давайте начнем опрос. Укажите ваш рост (в см):", reply_markup=cancel_button)
    await UserSurvey.waiting_for_height.set()

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
        await UserSurvey.waiting_for_weight.set()
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
        await UserSurvey.waiting_for_goal.set()
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

    # Получаем все данные из состояния
    user_data = await state.get_data()

    # Отправляем подтверждение
    await message.answer(
        f"Спасибо за ответы!\n"
        f"Ваш рост: {user_data['height']} см\n"
        f"Ваш вес: {user_data['weight']} кг\n"
        f"Ваша цель: {user_data['goal']}",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Завершаем состояние
    await state.clear()