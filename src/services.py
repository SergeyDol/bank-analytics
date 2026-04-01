import json
from typing import Any, Dict, List

from src.logger_config import setup_logger

logger = setup_logger("services", "services.log")


def simple_search(transactions: List[Dict[str, Any]], search_string: str) -> str:
    try:
        result = []
        search_lower = search_string.lower()

        for transaction in transactions:
            description = transaction.get('Описание', '')
            category = transaction.get('Категория', '')

            # Проверяем, что значение является строкой
            description_str = description if isinstance(description, str) else ''
            category_str = category if isinstance(category, str) else ''

            if search_lower in description_str.lower() or search_lower in category_str.lower():
                result.append(transaction)

        logger.info(f"Найдено {len(result)} транзакций по запросу '{search_string}'")
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Ошибка в simple_search: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)
