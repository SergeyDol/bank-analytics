import json
import re
import pandas as pd  # Добавьте эту строку
from typing import List, Dict, Any
import logging
from src.utils import read_excel_file
from src.logger_config import setup_logger

logger = setup_logger("services", "services.log")


def simple_search(search_query: str) -> str:
    """
    Сервис простого поиска по транзакциям.

    Args:
        search_query: Строка для поиска

    Returns:
        JSON-строка с найденными транзакциями
    """
    try:
        # Читаем данные
        df = read_excel_file('data/operations.xlsx')
        if df.empty:
            return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False)

        # Ищем в описании и категории (без учета регистра)
        mask = (
                df['Описание'].str.contains(search_query, case=False, na=False) |
                df['Категория'].str.contains(search_query, case=False, na=False)
        )

        results = df[mask]

        # Форматируем результат
        transactions = []
        for _, row in results.iterrows():
            transactions.append({
                "date": row['Дата операции'],
                "amount": abs(row['Сумма операции']),
                "category": row['Категория'] if pd.notna(row['Категория']) else "Другое",
                "description": row['Описание'] if pd.notna(row['Описание']) else "",
                "type": "расход" if row['Сумма операции'] < 0 else "доход"
            })

        result = {
            "query": search_query,
            "found": len(transactions),
            "transactions": transactions
        }

        logger.info(f"Поиск '{search_query}' - найдено {len(transactions)} транзакций")
        return json.dumps(result, ensure_ascii=False, indent=2, default=str)

    except Exception as e:
        logger.error(f"Ошибка в simple_search: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)