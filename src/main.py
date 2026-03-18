import json

from src.logger_config import setup_logger
from src.reports import spending_by_category
from src.services import simple_search
from src.utils import read_excel_file
from src.views import main_page

logger = setup_logger("main", "main.log")


def demonstrate_views():
    """Демонстрация работы веб-страницы 'Главная'."""
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ВЕБ-СТРАНИЦЫ 'ГЛАВНАЯ'")
    print("=" * 50)

    # Тестируем с разными датами
    test_dates = [
        "2021-12-31 16:44:00",  # Вечер
        "2021-12-31 09:44:00",  # Утро
        "2021-12-31 03:44:00",  # Ночь
    ]

    for date in test_dates:
        print(f"\nДата: {date}")
        result = main_page(date)
        data = json.loads(result)

        print(f"Приветствие: {data.get('greeting')}")
        print(f"Карт: {len(data.get('cards', []))}")
        print(f"Топ-транзакций: {len(data.get('top_transactions', []))}")
        print(f"Курсов валют: {len(data.get('currency_rates', []))}")
        print(f"Цен акций: {len(data.get('stock_prices', []))}")


def demonstrate_services():
    """Демонстрация работы сервиса 'Простой поиск'."""
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СЕРВИСА 'ПРОСТОЙ ПОИСК'")
    print("=" * 50)

    # Загружаем транзакции
    df = read_excel_file('data/operations.xlsx')
    if df.empty:
        print("Не удалось загрузить данные")
        return

    transactions = df.to_dict('records')

    # Тестируем поиск
    search_queries = ["Перевод", "МТС", "Яндекс"]

    for query in search_queries:
        print(f"\nПоиск по запросу: '{query}'")
        result = simple_search(transactions, query)
        data = json.loads(result)
        print(f"Найдено транзакций: {len(data)}")


def demonstrate_reports():
    """Демонстрация работы отчета 'Траты по категории'."""
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ОТЧЕТА 'ТРАТЫ ПО КАТЕГОРИИ'")
    print("=" * 50)

    # Загружаем транзакции
    df = read_excel_file('data/operations.xlsx')
    if df.empty:
        print("Не удалось загрузить данные")
        return

    # Тестируем отчет
    categories = ["Супермаркеты", "Переводы", "Каршеринг"]

    for category in categories:
        print(f"\nКатегория: '{category}'")
        result = spending_by_category(df, category, "2021-12-31")
        print(f"Найдено транзакций: {len(result)}")
        print("Результат сохранен в файл с отчетом")


def main():
    """Главная функция приложения."""
    print("=" * 50)
    print("ПРИЛОЖЕНИЕ ДЛЯ АНАЛИЗА БАНКОВСКИХ ТРАНЗАКЦИЙ")
    print("=" * 50)

    try:
        demonstrate_views()
        demonstrate_services()
        demonstrate_reports()

        print("\n" + "=" * 50)
        print("ВСЕ ДЕМОНСТРАЦИИ УСПЕШНО ВЫПОЛНЕНЫ!")
        print("=" * 50)

    except Exception as e:
        logger.error(f"Ошибка в main: {e}")
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()
