import pytest
import json
from unittest.mock import patch, Mock
from src.views import main_page


class TestViews:
    """Тесты для модуля views."""

    @patch('src.views.read_excel_file')
    def test_main_page_empty_data(self, mock_read):
        """Тест главной страницы с пустыми данными."""
        mock_read.return_value.empty = True
        result = main_page("2021-12-31 16:44:00")
        data = json.loads(result)
        assert "error" in data

    @patch('src.views.read_excel_file')
    @patch('src.views.filter_by_date_range')
    def test_main_page_no_data_for_period(self, mock_filter, mock_read):
        """Тест главной страницы с отсутствием данных за период."""
        mock_df = Mock()
        mock_df.empty = False
        mock_read.return_value = mock_df

        mock_filtered = Mock()
        mock_filtered.empty = True
        mock_filter.return_value = mock_filtered

        result = main_page("2021-12-31 16:44:00")
        data = json.loads(result)
        assert "error" in data

    @patch('src.views.read_excel_file')
    @patch('src.views.filter_by_date_range')
    @patch('src.views.get_greeting')
    @patch('src.views.calculate_card_stats')
    @patch('src.views.get_top_transactions')
    @patch('src.views.get_user_settings')
    @patch('src.views.get_exchange_rates')
    @patch('src.views.get_stock_prices')
    def test_main_page_success(
            self, mock_stocks, mock_rates, mock_settings,
            mock_top, mock_cards, mock_greeting, mock_filter, mock_read
    ):
        """Тест успешной работы главной страницы."""
        # Настраиваем моки
        mock_df = Mock()
        mock_df.empty = False
        mock_read.return_value = mock_df

        mock_filtered = Mock()
        mock_filtered.empty = False
        mock_filter.return_value = mock_filtered

        mock_greeting.return_value = "Добрый день"
        mock_cards.return_value = [{"last_digits": "1234", "total_spent": 1000}]
        mock_top.return_value = [{"date": "01.01.2021", "amount": 500}]
        mock_settings.return_value = {
            "user_currencies": ["USD"],
            "user_stocks": ["AAPL"]
        }
        mock_rates.return_value = [{"currency": "USD", "rate": 75.5}]
        mock_stocks.return_value = [{"stock": "AAPL", "price": 150.0}]

        result = main_page("2021-12-31 16:44:00")
        data = json.loads(result)

        assert "greeting" in data
        assert "cards" in data
        assert "top_transactions" in data
        assert "currency_rates" in data
        assert "stock_prices" in data
        assert data["greeting"] == "Добрый день"
