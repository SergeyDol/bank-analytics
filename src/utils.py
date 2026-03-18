import json
import os
from datetime import datetime
from typing import List, Dict, Any

import pandas as pd
import requests
from dotenv import load_dotenv

from src.logger_config import setup_logger

logger = setup_logger("utils", "utils.log")
load_dotenv()


def get_greeting(hour: int) -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Args:
        hour: Час (0-23)

    Returns:
        Строка с приветствием
    """
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Читает Excel-файл с транзакциями и возвращает DataFrame.

    Args:
        file_path: Путь к файлу

    Returns:
        DataFrame с транзакциями
    """
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Успешно прочитан файл {file_path}. Найдено {len(df)} строк")
        return df
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return pd.DataFrame()


def filter_by_date_range(df: pd.DataFrame, date_str: str) -> pd.DataFrame:
    """
    Фильтрует транзакции по дате: с начала месяца по указанную дату.

    Args:
        df: DataFrame с транзакциями
        date_str: Строка с датой в формате 'YYYY-MM-DD HH:MM:SS'

    Returns:
        Отфильтрованный DataFrame
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        first_day = target_date.replace(day=1, hour=0, minute=0, second=0)

        df['Дата операции_dt'] = pd.to_datetime(
            df['Дата операции'],
            format='%d.%m.%Y %H:%M:%S'
        )

        mask = (df['Дата операции_dt'] >= first_day) & (df['Дата операции_dt'] <= target_date)
        filtered_df = df[mask].copy()

        logger.info(
            f"Отфильтровано {len(filtered_df)} транзакций за период "
            f"{first_day.date()} - {target_date.date()}"
        )
        return filtered_df

    except Exception as e:
        logger.error(f"Ошибка при фильтрации по дате: {e}")
        return pd.DataFrame()


def calculate_card_stats(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Рассчитывает статистику по каждой карте.

    Args:
        df: DataFrame с отфильтрованными транзакциями

    Returns:
        Список словарей с данными по картам
    """
    try:
        expenses_df = df[(df['Сумма операции'] < 0) & (df['Номер карты'].notna())].copy()

        if expenses_df.empty:
            return []

        expenses_df['last_digits'] = expenses_df['Номер карты'].str.extract(r'\*(\d{4})$')

        card_stats = []
        for card, group in expenses_df.groupby('last_digits'):
            total_spent = abs(group['Сумма операции'].sum())
            cashback = round(total_spent / 100, 2)

            card_stats.append({
                "last_digits": card,
                "total_spent": round(total_spent, 2),
                "cashback": cashback
            })

        card_stats.sort(key=lambda x: x['total_spent'], reverse=True)
        logger.info(f"Рассчитана статистика по {len(card_stats)} картам")
        return card_stats

    except Exception as e:
        logger.error(f"Ошибка при расчете статистики по картам: {e}")
        return []


def get_top_transactions(df: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
    """
    Возвращает топ-N транзакций по сумме платежа.

    Args:
        df: DataFrame с транзакциями
        n: Количество транзакций

    Returns:
        Список словарей с топ-транзакциями
    """
    try:
        expenses_df = df[df['Сумма операции'] < 0].copy()

        if expenses_df.empty:
            return []

        expenses_df['abs_amount'] = expenses_df['Сумма операции'].abs()
        top_df = expenses_df.nlargest(n, 'abs_amount')

        top_transactions = []
        for _, row in top_df.iterrows():
            date = pd.to_datetime(row['Дата операции'], format='%d.%m.%Y %H:%M:%S')

            top_transactions.append({
                "date": date.strftime('%d.%m.%Y'),
                "amount": round(abs(row['Сумма операции']), 2),
                "category": row['Категория'] if pd.notna(row['Категория']) else "Другое",
                "description": row['Описание'] if pd.notna(row['Описание']) else ""
            })

        logger.info(f"Получено топ-{len(top_transactions)} транзакций")
        return top_transactions

    except Exception as e:
        logger.error(f"Ошибка при получении топ-транзакций: {e}")
        return []


def get_user_settings() -> Dict[str, Any]:
    """
    Загружает пользовательские настройки из файла user_settings.json.

    Returns:
        Словарь с настройками пользователя
    """
    try:
        with open('user_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        logger.debug(f"Загружены пользовательские настройки: {settings}")
        return settings
    except Exception as e:
        logger.error(f"Ошибка при загрузке user_settings.json: {e}")
        return {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
        }


def get_exchange_rates(currencies: List[str]) -> List[Dict[str, float]]:
    """
    Получает текущие курсы валют через API.

    Args:
        currencies: Список кодов валют

    Returns:
        Список словарей с курсами валют
    """
    api_key = os.getenv("EXCHANGE_RATE_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        logger.warning("API ключ для курсов валют не настроен")
        return [{"currency": curr, "rate": 0.0} for curr in currencies]

    try:
        url = "https://api.exchangerate-api.com/v4/latest/RUB"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            rates = []
            for currency in currencies:
                rate = 1 / data['rates'].get(currency, 1)
                rates.append({
                    "currency": currency,
                    "rate": round(rate, 2)
                })
            logger.info(f"Получены курсы валют: {rates}")
            return rates
        else:
            logger.error(f"Ошибка API: {response.status_code}")
            return [{"currency": curr, "rate": 0.0} for curr in currencies]

    except Exception as e:
        logger.error(f"Ошибка при получении курсов валют: {e}")
        return [{"currency": curr, "rate": 0.0} for curr in currencies]


def get_stock_prices(stocks: List[str]) -> List[Dict[str, float]]:
    """
    Получает текущие цены акций через API Alpha Vantage.

    Args:
        stocks: Список тикеров акций

    Returns:
        Список словарей с ценами акций
    """
    api_key = os.getenv("STOCKS_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        logger.warning("API ключ для цен акций не настроен")
        return [{"stock": stock, "price": 0.0} for stock in stocks]

    try:
        prices = []
        for stock in stocks:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': stock,
                'apikey': api_key
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                global_quote = data.get('Global Quote', {})
                price = float(global_quote.get('05. price', 0))
                prices.append({
                    "stock": stock,
                    "price": round(price, 2)
                })
            else:
                logger.error(f"Ошибка API для {stock}: {response.status_code}")
                prices.append({"stock": stock, "price": 0.0})

        logger.info(f"Получены цены акций: {prices}")
        return prices

    except Exception as e:
        logger.error(f"Ошибка при получении цен акций: {e}")
        return [{"stock": stock, "price": 0.0} for stock in stocks]
