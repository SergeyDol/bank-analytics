import json
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
import logging
from src.utils import read_excel_file
from src.logger_config import setup_logger

logger = setup_logger("reports", "reports.log")


def spending_by_category(category: str, date: Optional[str] = None) -> str:
    """
    Отчет о тратах по категории за последние 3 месяца.

    Args:
        category: Название категории
        date: Дата отсчета (если None, используется текущая)

    Returns:
        JSON-строка с отчетом
    """
    try:
        # Определяем дату отсчета
        if date:
            end_date = pd.to_datetime(date, format='%d.%m.%Y')
        else:
            end_date = datetime.now()

        # Начало периода (3 месяца назад)
        start_date = end_date - timedelta(days=90)

        # Читаем данные
        df = read_excel_file('data/operations.xlsx')
        if df.empty:
            return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False)

        # Преобразуем даты
        df['date_dt'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')

        # Фильтруем по дате и категории, берем только расходы
        mask = (
                (df['date_dt'] >= start_date) &
                (df['date_dt'] <= end_date) &
                (df['Категория'] == category) &
                (df['Сумма операции'] < 0)
        )

        filtered_df = df[mask]

        # Рассчитываем статистику
        if len(filtered_df) > 0:
            total_spent = abs(filtered_df['Сумма операции'].sum())
            transactions_count = len(filtered_df)
            avg_spent = total_spent / transactions_count

            # Формируем результат
            result = {
                "category": category,
                "period": {
                    "from": start_date.strftime('%d.%m.%Y'),
                    "to": end_date.strftime('%d.%m.%Y')
                },
                "total_spent": round(total_spent, 2),
                "transactions_count": transactions_count,
                "average_spent": round(avg_spent, 2),
                "transactions": []
            }

            # Добавляем топ-10 транзакций
            top_transactions = filtered_df.nlargest(10, 'Сумма операции')
            for _, row in top_transactions.iterrows():
                result["transactions"].append({
                    "date": row['Дата операции'],
                    "amount": abs(row['Сумма операции']),
                    "description": row['Описание'] if pd.notna(row['Описание']) else ""
                })
        else:
            result = {
                "category": category,
                "period": {
                    "from": start_date.strftime('%d.%m.%Y'),
                    "to": end_date.strftime('%d.%m.%Y')
                },
                "total_spent": 0,
                "transactions_count": 0,
                "average_spent": 0,
                "transactions": []
            }

        logger.info(
            f"Отчет по категории '{category}' - всего {result['transactions_count']} транзакций на сумму {result['total_spent']:.2f}")
        return json.dumps(result, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        logger.error(f"Ошибка в spending_by_category: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)