import logging
import sys
from pathlib import Path

# Создаём логгер
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Файл логов
log_file = Path("bot.log")
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# В консоль тоже
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)