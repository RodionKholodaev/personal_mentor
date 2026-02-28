import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.commands import router  
from config import BOT_TOKEN

from database import init_db

from logger import logger

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Подключаем роутеры
dp.include_router(router)

async def main():
    logger.info("Бот запущен")
    # Запуск polling
    init_db()
    try:
        await dp.start_polling(
            bot,
            skip_updates=True,
            handle_signals=False
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Остановка по Ctrl+C")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
    finally:
        logger.info("Закрытие соединений")
        await bot.session.close()
        await dp.storage.close()


if __name__ == "__main__":
    asyncio.run(main())