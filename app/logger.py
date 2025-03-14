import logging
from logging.handlers import RotatingFileHandler
import os

# Создаем директорию для логов, если её нет
os.makedirs("logs", exist_ok=True)

# Настройка логгера
logger = logging.getLogger("library_api")
logger.setLevel(logging.INFO)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Обработчик для записи в файл
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10485760,  # 10 MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)

# Формат логов
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Добавляем обработчики к логгеру
logger.addHandler(console_handler)
logger.addHandler(file_handler)