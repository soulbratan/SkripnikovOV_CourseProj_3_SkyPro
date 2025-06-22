from unittest.mock import MagicMock, patch

from src.HH_api import get_hh_data_full, get_hh_data_short


def test_get_hh_data_short() -> None:
    """Тестирование получения кратких данных с HH API"""
    mock_company_response = MagicMock()
    mock_company_response.json.return_value = {
        "name": "Test Company",
        "area": {"name": "Moscow"},
        "open_vacancies": 10,
        "industries": [{"name": "IT"}],
        "alternate_url": "test.com",
        "vacancies_url": "test.com/vac",
    }

    mock_vacancies_response = MagicMock()
    mock_vacancies_response.json.return_value = {
        "items": [
            {
                "name": "Developer",
                "area": {"name": "Moscow"},
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "published_at": "2023-01-01",
                "snippet": {"responsibility": "Code"},
                "alternate_url": "test.com/vac/1",
            }
        ]
    }

    with patch("requests.get", side_effect=[mock_company_response, mock_vacancies_response]):
        result = get_hh_data_short(["123"])

        assert len(result) == 1
        assert result[0]["company"]["name"] == "Test Company"
        assert result[0]["vacancies"][0]["name"] == "Developer"


def test_get_hh_data_full() -> None:
    """Тестирование получения полных данных с HH API"""
    mock_company_response = MagicMock()
    mock_company_response.json.return_value = {
        "name": "Test Company",
        "area": {"name": "Moscow"},
        "open_vacancies": 10,
        "industries": [{"name": "IT"}],
        "alternate_url": "test.com",
        "vacancies_url": "test.com/vac",
    }

    mock_vacancies_page1 = MagicMock()
    mock_vacancies_page1.json.return_value = {
        "items": [
            {
                "name": "Developer 1",
                "area": {"name": "Moscow"},
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "published_at": "2023-01-01",
                "snippet": {"responsibility": "Code"},
                "alternate_url": "test.com/vac/1",
            }
        ]
    }

    mock_vacancies_page2 = MagicMock()
    mock_vacancies_page2.json.return_value = {"items": []}

    with patch("requests.get", side_effect=[mock_company_response, mock_vacancies_page1, mock_vacancies_page2]):
        result = get_hh_data_full(["123"])

        assert len(result) == 1
        assert len(result[0]["vacancies"]) == 1
        assert result[0]["vacancies"][0]["name"] == "Developer 1"
