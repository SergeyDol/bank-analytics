# Bank Analytics Application

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/imports-isort-1674b1.svg)](https://pycqa.github.io/isort/)
[![Linting: flake8](https://img.shields.io/badge/linting-flake8-yellow.svg)](https://flake8.pycqa.org/)
[![Type checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue.svg)](http://mypy-lang.org/)

Приложение для анализа банковских транзакций. Позволяет получать статистику по расходам, кешбэку, курсам валют и ценам акций.

## 📝 Описание

Проект реализует три основных направления:
- **Веб-страницы** - генерация JSON-ответов для отображения на фронтенде
- **Сервисы** - вспомогательные функции для анализа транзакций
- **Отчеты** - формирование отчетов с возможностью сохранения в файл

## 🚀 Функциональность

### Веб-страницы (`views.py`)
- **Главная страница** - принимает дату и возвращает JSON с:
  - Приветствием в зависимости от времени суток
  - Статистикой по картам (расходы, кешбэк)
  - Топ-5 транзакций по сумме
  - Курсами валют (из пользовательских настроек)
  - Ценами акций S&P 500

### Сервисы (`services.py`)
- **Простой поиск** - поиск транзакций по строке в описании

### Отчеты (`reports.py`)
- **Траты по категории** - анализ расходов по категории за последние 3 месяца
- **Декоратор для отчетов** - автоматическое сохранение результатов в JSON-файл

## 💻 Установка

### Предварительные требования
- Python 3.10 или выше
- Poetry (менеджер зависимостей)

### Шаги по установке

1. **Клонировать репозиторий**
```bash
git clone https://github.com/ваш-username/bank-analytics.git
cd bank-analytics
Установить зависимости через poetry

bash
poetry install
Активировать виртуальное окружение

bash
poetry shell
# или
.venv\Scripts\activate  # для Windows
source .venv/bin/activate  # для Mac/Linux
Создать файл .env

bash
cp .env_template .env
Добавить API ключи в файл .env

Поместить файл с данными

Скачайте файл operations.xlsx из личного кабинета Т-Банка

Положите его в папку data/

🎮 Использование
Запуск демонстрации всех функций
bash
python src/main.py
Пример работы с отдельными модулями
python
from src.views import main_page
from src.services import simple_search
from src.reports import spending_by_category
from src.utils import read_excel_file

# Главная страница
result = main_page("2021-12-31 16:44:00")
print(result)

# Простой поиск
transactions = read_excel_file('data/operations.xlsx').to_dict('records')
search_result = simple_search(transactions, "Перевод")
print(search_result)

# Отчет по категории
df = read_excel_file('data/operations.xlsx')
report = spending_by_category(df, "Супермаркеты", "2021-12-31")
print(report)
🧪 Тестирование
Запуск всех тестов
bash
pytest tests/ -v
Проверка покрытия кода тестами
bash
pytest --cov=src tests/
Просмотр отчета о покрытии
bash
pytest --cov=src --cov-report=html tests/
# Открыть htmlcov/index.html в браузере
🔧 Линтеры
Сортировка импортов
bash
isort .
Проверка стиля кода
bash
flake8 .
Форматирование кода
bash
black .
Проверка типов
bash
mypy src/
📁 Структура проекта
text
bank_analytics/
├── src/
│   ├── __init__.py
│   ├── main.py          # Точка входа
│   ├── views.py         # Функции для веб-страниц
│   ├── services.py      # Сервисные функции
│   ├── reports.py       # Функции для отчетов
│   ├── utils.py         # Вспомогательные функции
│   └── logger_config.py # Настройка логирования
├── tests/
│   ├── __init__.py
│   ├── test_utils.py
│   ├── test_views.py
│   ├── test_services.py
│   └── test_reports.py
├── data/
│   └── operations.xlsx  # Файл с транзакциями
├── logs/                 # Логи приложения
├── .env                  # Переменные окружения (не в git)
├── .env_template         # Шаблон .env
├── .flake8               # Конфигурация flake8
├── .gitignore
├── pyproject.toml        # Конфигурация poetry и линтеров
├── README.md
└── user_settings.json    # Пользовательские настройки
🔑 API ключи
Для работы с курсами валют и ценами акций необходимо получить API ключи:

Курсы валют
Бесплатный API: exchangerate-api.com

Получите ключ и добавьте в .env: EXCHANGE_RATE_API_KEY=ваш_ключ

Цены акций
Бесплатный API: alphavantage.co

Получите ключ и добавьте в .env: STOCKS_API_KEY=ваш_ключ

⚙️ Конфигурация
Пользовательские настройки (user_settings.json)
json
{
  "user_currencies": ["USD", "EUR"],
  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
}
Переменные окружения (.env_template)
env
# API Keys
EXCHANGE_RATE_API_KEY=your_api_key_here
STOCKS_API_KEY=your_api_key_here

# File paths
DATA_FILE_PATH=data/operations.xlsx
