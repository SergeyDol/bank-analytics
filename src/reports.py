import json
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

from src.logger_config import setup_logger

logger = setup_logger("reports", "reports.log")


def report_decorator(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для записи результатов отчетов в файл.

    Args:
        filename: Имя файла для записи (по умолчанию report_YYYY-MM-DD_HH-MM-SS.json)
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)

            # Определяем имя файла
            if filename is None:
                file_name = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
            else:
                file_name = filename

            # Записываем результат в файл
            try:
                if isinstance(result, pd.DataFrame):
                    result.to_json(file_name, orient='records', force_ascii=False, indent=2)
                else:
                    with open(file_name, 'w', encoding='utf-8') as f:
                        json.dump(result, f, ensure_ascii=False, indent=2)

                logger.info(f"Результат отчета сохранен в файл: {file_name}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")

            return result

        return wrapper

    return decorator


@report_decorator()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        category: Название категории
        date: Дата отсчета (по умолчанию текущая)

    Returns:
        DataFrame с тратами по категории
    """
    try:
        # Если дата не передана, используем текущую
        if date is None:
            target_date = datetime.now()
        else:
            target_date = datetime.strptime(date, "%Y-%m-%d")

        # Вычисляем дату три месяца назад
        three_months_ago = target_date - timedelta(days=90)

        # Преобразуем даты операций
        transactions['date_dt'] = pd.to_datetime(
            transactions['Дата операции'],
            format='%d.%m.%Y %H:%M:%S'
        )

        # Фильтруем по дате и категории
        mask = (
                (transactions['date_dt'] >= three_months_ago) &
                (transactions['date_dt'] <= target_date) &
                (transactions['Категория'] == category) &
                (transactions['Сумма операции'] < 0)  # Только расходы
        )

        result = transactions[mask].copy()
        logger.info(f"Найдено {len(result)} транзакций по категории '{category}' за последние 3 месяца")

        return result[['Дата операции', 'Сумма операции', 'Категория', 'Описание']]

    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {e}")
        return pd.DataFrame()
