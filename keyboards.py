from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

sex_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской")],
        [KeyboardButton(text="Женский")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True  # клавиатура свернётся после нажатия
)

accept_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Принять")],
        [KeyboardButton(text="Изменить")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True  
)