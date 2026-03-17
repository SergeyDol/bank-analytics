from src.services import simple_search
from src.reports import spending_by_category

print("=" * 50)
print("ТЕСТ СЕРВИСА ПРОСТОГО ПОИСКА")
print("=" * 50)

# Поиск по слову "Перевод"
result = simple_search("Перевод")
print(result)

print("\n" + "=" * 50)
print("ТЕСТ ОТЧЕТА ПО КАТЕГОРИИ")
print("=" * 50)

# Отчет по категории "Супермаркеты"
result = spending_by_category("Супермаркеты", "31.12.2021")
print(result)