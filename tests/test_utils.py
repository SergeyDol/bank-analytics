import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch, Mock
from src.utils import (
    get_greeting,
    calculate_card_stats,
    get_top_transactions,
    get_user_settings,
    get_exchange_rates,
    get_stock_prices
)


class TestUtils:
    """Тесты для вспомогательных функций."""

    @pytest.mark.parametrize("hour,expected", [
        (6, "Доброе утро"),
        (9, "Доброе утро"),
        (12, "Добрый день"),
        (15, "Добрый день"),
        (18, "Добрый вечер"),
        (21, "Добрый вечер"),
        (0, "Доброй ночи"),
        (3, "Доброй ночи"),
    ])
    def test_get_greeting(self, hour, expected):
        """Тест приветствия в разное время суток."""
        assert get_greeting(hour) == expected

    def test_calculate_card_stats_empty(self):
        """Тест расчета статистики по картам с пустым DataFrame."""
        df = pd.DataFrame()
        result = calculate_card_stats(df)
        assert result == []

    def test_get_top_transactions_empty(self):
        """Тест получения топ-транзакций с пустым DataFrame."""
        df = pd.DataFrame()
        result = get_top_transactions(df)
        assert result == []

    @patch('src.utils.json.load')
    def test_get_user_settings_file_not_found(self, mock_json_load):
        """Тест получения настроек при отсутствии файла."""
        mock_json_load.side_effect = FileNotFoundError()
        result = get_user_settings()
        assert 'user_currencies' in result
        assert 'user_stocks' in result
        assert len(result['user_currencies']) > 0
        assert len(result['user_stocks']) > 0

    @patch('src.utils.requests.get')
    def test_get_exchange_rates_no_api_key(self, mock_get):
        """Тест получения курсов валют без API ключа."""
        with patch('src.utils.os.getenv', return_value='your_api_key_here'):
            result = get_exchange_rates(['USD', 'EUR'])
            assert len(result) == 2
            assert result[0]['rate'] == 0.0

    @patch('src.utils.requests.get')
    def test_get_exchange_rates_success(self, mock_get):
        """Тест успешного получения курсов валют."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'rates': {'USD': 100, 'EUR': 90}}
        mock_get.return_value = mock_response

        with patch('src.utils.os.getenv', return_value='real_key'):
            result = get_exchange_rates(['USD', 'EUR'])
            assert len(result) == 2
            assert result[0]['currency'] == 'USD'
            assert result[0]['rate'] > 0

    @patch('src.utils.requests.get')
    def test_get_stock_prices_no_api_key(self, mock_get):
        """Тест получения цен акций без API ключа."""
        with patch('src.utils.os.getenv', return_value='your_api_key_here'):
            result = get_stock_prices(['AAPL', 'GOOGL'])
            assert len(result) == 2
            assert result[0]['price'] == 0.0

    @patch('src.utils.requests.get')
    def test_get_stock_prices_success(self, mock_get):
        """Тест успешного получения цен акций."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'Global Quote': {'05. price': '150.50'}
        }
        mock_get.return_value = mock_response

        with patch('src.utils.os.getenv', return_value='real_key'):
            result = get_stock_prices(['AAPL'])
            assert len(result) == 1
            assert result[0]['stock'] == 'AAPL'
            assert result[0]['price'] == 150.50
