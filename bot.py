from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from handlers.commands import router  # Импортируем роутер из commands.py

API_TOKEN = "В

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаем роутеры
dp.include_router(router)

if __name__ == "__main__":
    start_polling(dp, skip_updates=True)