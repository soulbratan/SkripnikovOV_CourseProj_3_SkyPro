import os
from configparser import ConfigParser


def test_config_file_exists() -> None:
    """Проверяет, что файл конфигурации существует"""
    assert os.path.exists("database.ini"), "Файл database.ini не найден"


def test_config_section_exists() -> None:
    """Проверяет, что секция postgresql существует в файле"""
    config = ConfigParser()
    config.read("database.ini")
    assert "postgresql" in config, "Секция postgresql не найдена в файле конфигурации"


def test_config_returns_dict(sample_db_params: dict[str, str]) -> None:
    """Проверяет, что функция config возвращает словарь"""
    from src.config import config

    result = config("database.ini")
    assert isinstance(result, dict), "Функция config должна возвращать словарь"
    assert "host" in result, "В словаре конфигурации должен быть ключ 'host'"
