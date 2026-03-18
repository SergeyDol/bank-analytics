import pytest
import json
from src.services import simple_search


class TestServices:
    """Тесты для модуля services."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с тестовыми транзакциями."""
        return [
            {
                "Описание": "Перевод организации",
                "Категория": "Переводы"
            },
            {
                "Описание": "Я МТС +7 921 11-22-33",
                "Категория": "Мобильная связь"
            },
            {
                "Описание": "Яндекс Такси",
                "Категория": "Транспорт"
            }
        ]

    def test_simple_search_found(self, sample_transactions):
        """Тест поиска с найденными результатами."""
        result = simple_search(sample_transactions, "МТС")
        data = json.loads(result)
        assert len(data) == 1
        assert "МТС" in data[0]["Описание"]

    def test_simple_search_not_found(self, sample_transactions):
        """Тест поиска без результатов."""
        result = simple_search(sample_transactions, "несуществующий запрос")
        data = json.loads(result)
        assert len(data) == 0

    def test_simple_search_case_insensitive(self, sample_transactions):
        """Тест поиска без учета регистра."""
        result = simple_search(sample_transactions, "перевод")
        data = json.loads(result)
        assert len(data) == 1
        assert "Перевод" in data[0]["Категория"]

    def test_simple_search_empty_transactions(self):
        """Тест поиска с пустым списком транзакций."""
        result = simple_search([], "МТС")
        data = json.loads(result)
        assert len(data) == 0
