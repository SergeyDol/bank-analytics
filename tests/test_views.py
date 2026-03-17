from src.views import main_page

# Тестируем с разными датами
test_dates = [
    "2021-12-31 16:44:00",  # Вечер
    "2021-12-31 09:44:00",  # Утро
    "2021-12-31 03:44:00",  # Ночь
]

for date in test_dates:
    print(f"\nДата: {date}")
    result = main_page(date)
    print(result)