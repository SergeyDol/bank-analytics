import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str, log_file: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Настраивает и возвращает логгер для модуля.

    Args:
        name: Имя логгера
        log_file: Имя файла для логов
        level: Уровень логирования

    Returns:
        Настроенный логгер
    """
    # Создаем логгер
    logger = logging.getLogger(name)

    # Устанавливаем уровень логирования
    logger.setLevel(level)

    # Проверяем, что у логгера еще нет handlers
    if logger.handlers:
        return logger

    # Создаем папку logs если ее нет
    os.makedirs("logs", exist_ok=True)

    # Создаем file handler
    file_handler = RotatingFileHandler(
        f"logs/{log_file}",
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(level)

    # Создаем formatter
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Устанавливаем formatter
    file_handler.setFormatter(file_formatter)

    # Добавляем handler
    logger.addHandler(file_handler)

    return logger