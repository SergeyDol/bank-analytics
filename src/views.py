import json
from datetime import datetime

from src.logger_config import setup_logger
from src.utils import (calculate_card_stats, filter_by_date_range,
                       get_exchange_rates, get_greeting, get_stock_prices,
                       get_top_transactions, get_user_settings,
                       read_excel_file)

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
        df = read_excel_file('data/operations.xlsx')
        if df.empty:
            return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False)

        filtered_df = filter_by_date_range(df, date_str)
        if filtered_df.empty:
            return json.dumps({"error": "Нет данных за указанный период"}, ensure_ascii=False)

        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        greeting = get_greeting(target_date.hour)

        card_stats = calculate_card_stats(filtered_df)
        top_transactions = get_top_transactions(filtered_df)
        settings = get_user_settings()
        currency_rates = get_exchange_rates(settings['user_currencies'])
        stock_prices = get_stock_prices(settings['user_stocks'])

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
