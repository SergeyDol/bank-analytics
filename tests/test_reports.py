import pytest
import pandas as pd
from datetime import datetime
from unittest.mock import patch
from src.reports import spending_by_category, report_decorator


class TestReports:
    """Тесты для модуля reports."""

    @pytest.fixture
    def sample_transactions_df(self):
        """Фикстура с тестовыми транзакциями в DataFrame."""
        data = {
            'Дата операции': [
                '01.12.2021 10:00:00',
                '15.11.2021 15:30:00',
                '10.10.2021 09:20:00',
                '01.09.2021 14:00:00'
            ],
            'Сумма операции': [-500, -300, -200, -100],
            'Категория': ['Супермаркеты', 'Супермаркеты', 'Кафе', 'Супермаркеты'],
            'Описание': ['Магнит', 'Пятёрочка', 'Кофе', 'Перекрёсток']
        }
        return pd.DataFrame(data)

    def test_spending_by_category(self, sample_transactions_df):
        """Тест отчета по категории."""
        result = spending_by_category(
            sample_transactions_df,
            'Супермаркеты',
            '2021-12-31'
        )
        assert len(result) == 2  # Должны попасть только транзакции за последние 3 месяца

    def test_spending_by_category_no_date(self, sample_transactions_df):
        """Тест отчета по категории без указания даты."""
        with patch('src.reports.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2021, 12, 31)
            result = spending_by_category(sample_transactions_df, 'Супермаркеты')
            assert len(result) == 2

    def test_spending_by_category_no_transactions(self):
        """Тест отчета по категории без транзакций."""
        df = pd.DataFrame(columns=['Дата операции', 'Сумма операции', 'Категория'])
        result = spending_by_category(df, 'Супермаркеты', '2021-12-31')
        assert len(result) == 0

    @patch('src.reports.json.dump')
    @patch('builtins.open')
    def test_report_decorator(self, mock_open, mock_json_dump):
        """Тест декоратора для отчетов."""

        @report_decorator()
        def test_func():
            return {"test": "data"}

        result = test_func()
        assert result == {"test": "data"}
        mock_open.assert_called_once()
