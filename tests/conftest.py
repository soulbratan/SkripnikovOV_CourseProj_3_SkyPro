from configparser import ConfigParser
from typing import Any, Generator
from unittest.mock import patch

import psycopg2
import pytest


@pytest.fixture
def sample_employers_id() -> list[str]:
    return ["15478", "1740"]


@pytest.fixture
def sample_db_params() -> dict[str, str]:
    config = ConfigParser()
    config.read("database.ini", encoding="utf-8")
    params = dict(config["postgresql"])
    # Убедимся, что параметры используют UTF-8
    params["client_encoding"] = "utf-8"
    return params


@pytest.fixture
def test_dbname() -> str:
    return "test_vacancies_db"


@pytest.fixture
def db_manager(test_dbname: str, sample_db_params: dict[str, str]) -> Generator[Any, None, None]:
    """DBManager fixture with explicit encoding handling"""
    from src.DBManager import DBManager

    conn = psycopg2.connect(dbname="postgres", **sample_db_params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {test_dbname}")
        cur.execute(f"CREATE DATABASE {test_dbname} ENCODING 'UTF8'")
    conn.close()

    manager = DBManager(test_dbname, sample_db_params)
    yield manager

    manager.disconnect()
    conn = psycopg2.connect(dbname="postgres", **sample_db_params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {test_dbname}")
    conn.close()


@pytest.fixture(autouse=True)
def setup_teardown(test_dbname: str, sample_db_params: dict[str, str]) -> None:
    """Фикстура для создания и удаления тестовой БД"""
    # Удаляем базу, если она существует
    conn = psycopg2.connect(dbname="postgres", **sample_db_params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {test_dbname}")
    conn.close()
    yield
    # Удаляем базу после тестов
    conn = psycopg2.connect(dbname="postgres", **sample_db_params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {test_dbname}")
    conn.close()


# Мокируем внешние зависимости
@pytest.fixture
def mock_dependencies():
    with (
        patch("main.config") as mock_config,
        patch("main.create_database") as mock_create_db,
        patch("main.save_data_to_database") as mock_save_data,
        patch("main.DBManager") as mock_dbmanager,
        patch("main.get_hh_data_full") as mock_get_full,
        patch("main.get_hh_data_short") as mock_get_short,
        patch("builtins.input") as mock_input,
        patch("builtins.print") as mock_print,
    ):
        yield {
            "mock_config": mock_config,
            "mock_create_db": mock_create_db,
            "mock_save_data": mock_save_data,
            "mock_dbmanager": mock_dbmanager,
            "mock_get_full": mock_get_full,
            "mock_get_short": mock_get_short,
            "mock_input": mock_input,
            "mock_print": mock_print,
        }
