import json
from datetime import datetime
from typing import Dict, Any
import pandas as pd
import logging
import json
from datetime import datetime
from typing import Dict, Any
import pandas as pd
import logging

from src.utils import (
    read_excel_file,
    filter_by_date_range,
    get_greeting,
    calculate_card_stats,
    get_top_transactions,
    get_user_settings,      # Добавлено
    get_exchange_rates,     # Добавлено
    get_stock_prices        # Добавлено
)
from src.logger_config import setup_logger

logger = setup_logger("views", "views.log")

from src.utils import (
    read_excel_file,
    filter_by_date_range,
    get_greeting,
    calculate_card_stats,
    get_top_transactions
)
from src.logger_config import setup_logger

logger = setup_logger("views", "views.log")


def main_page(date_str: str) -> str:
    """
    Главная функция для страницы 'Главная'.

    Args:
        date_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        JSON-строка с данными для отображения
    """
    try:
        # 1. Читаем данные
        df = read_excel_file('data/operations.xlsx')
        if df.empty:
            return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False)

        # 2. Фильтруем по дате
        filtered_df = filter_by_date_range(df, date_str)
        if filtered_df.empty:
            return json.dumps({"error": "Нет данных за указанный период"}, ensure_ascii=False)

        # 3. Получаем час из входной даты для приветствия
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        greeting = get_greeting(target_date.hour)

        # 4. Рассчитываем статистику по картам
        card_stats = calculate_card_stats(filtered_df)

        # 5. Получаем топ-5 транзакций
        top_transactions = get_top_transactions(filtered_df)

        # 6. Формируем результат
        result = {
            "greeting": greeting,
            "cards": card_stats,
            "top_transactions": top_transactions,
            "currency_rates": [],  # Пока пусто, добавим позже
            "stock_prices": []  # Пока пусто, добавим позже
        }

        logger.info(f"Успешно сформирован ответ для даты {date_str}")
        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в main_page: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def main_page(date_str: str) -> str:
        """
        Главная функция для страницы 'Главная'.

        Args:
            date_str: Строка с датой и временем в формате 'YYYY-MM-DD HH:MM:SS'

        Returns:
            JSON-строка с данными для отображения
        """
        try:
            # 1. Читаем данные
            df = read_excel_file('data/operations.xlsx')
            if df.empty:
                return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False)

            # 2. Фильтруем по дате
            filtered_df = filter_by_date_range(df, date_str)
            if filtered_df.empty:
                return json.dumps({"error": "Нет данных за указанный период"}, ensure_ascii=False)

            # 3. Получаем час из входной даты для приветствия
            target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            greeting = get_greeting(target_date.hour)

            # 4. Рассчитываем статистику по картам
            card_stats = calculate_card_stats(filtered_df)

            # 5. Получаем топ-5 транзакций
            top_transactions = get_top_transactions(filtered_df)

            # 6. Получаем пользовательские настройки
            settings = get_user_settings()

            # 7. Получаем курсы валют
            currency_rates = get_exchange_rates(settings['user_currencies'])

            # 8. Получаем цены акций
            stock_prices = get_stock_prices(settings['user_stocks'])

            # 9. Формируем результат
            result = {
                "greeting": greeting,
                "cards": card_stats,
                "top_transactions": top_transactions,
                "currency_rates": currency_rates,
                "stock_prices": stock_prices
            }

            logger.info(f"Успешно сформирован ответ для даты {date_str}")
            return json.dumps(result, ensure_ascii=False, indent=2, default=str)

        except Exception as e:
            logger.error(f"Ошибка в main_page: {e}")
            return json.dumps({"error": str(e)}, ensure_ascii=False)