from abc import ABC, abstractmethod
from typing import Any, Tuple

import psycopg2


class DBase(ABC):
    """Абстрактный класс для работы с базой данных о вакансиях"""

    @abstractmethod
    def connect(self) -> psycopg2.extensions.connection:
        pass    # pragma: no cover

    @abstractmethod
    def disconnect(self) -> None:
        pass    # pragma: no cover

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[Tuple]:
        pass    # pragma: no cover

    @abstractmethod
    def get_all_vacancies(self) -> list[Tuple]:
        pass    # pragma: no cover

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass    # pragma: no cover

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[Tuple]:
        pass    # pragma: no cover

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list[Tuple]:
        pass    # pragma: no cover


class DBManager(DBase):
    """Класс для работы с базой данных вакансий. Наследуется от DBase."""

    def __init__(self, dbname: str, params: dict) -> None:
        """Инициализация параметров подключения"""
        self.dbname = dbname
        self.params = params
        self.conn: psycopg2.extensions.connection | Any = None

    def connect(self) -> psycopg2.extensions.connection:
        """Соединение с базой данных"""
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
            self.conn.autocommit = True
        return self.conn

    def disconnect(self) -> None:
        """Закрытие соединения с базой данных"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None

    def __enter__(self) -> "DBManager":
        """Поддержка контекстного менеджера"""
        self.connect()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Поддержка контекстного менеджера"""
        self.disconnect()

    def get_companies_and_vacancies_count(self) -> list[Tuple]:
        """Получение списка всех компаний и количества вакансий у каждой компании."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name AS company_name, COUNT (vacancy_id) AS vacancies_count
                FROM companies
                LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
                GROUP BY companies.company_id, companies.name
                ORDER BY vacancies_count DESC;
                """
            )
            result = cur.fetchall()
            self.disconnect()
        return result

    def get_all_vacancies(self) -> list[Tuple]:
        """Получение списка всех вакансий с указанием компании, названия, зарплаты и ссылки."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                companies.name AS company_name,
                vacancies.name AS vacancy_name,
                vacancies.salary_from,
                vacancies.salary_to,
                vacancies.currency,
                vacancies.url AS vacancy_url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                ORDER BY company_name, vacancy_name;
                """
            )
            result = cur.fetchall()
            self.disconnect()
        return result

    def get_avg_salary(self) -> float | Any:
        """Получение средней зарплаты по вакансиям."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies;
                """
            )
            result = cur.fetchone()
            self.disconnect()
        return round(result[0], 2) if result is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> list[Tuple]:
        """Получение списка вакансий с зарплатой выше средней."""
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                    SELECT AVG((salary_from + salary_to) / 2)
                    FROM vacancies;
                    """
            )
            avg_salary = cur.fetchone()[0]  # type: ignore

            cur.execute(
                """
                    SELECT
                        companies.name AS company_name,
                        vacancies.name AS vacancy_name,
                        vacancies.salary_from,
                        vacancies.salary_to,
                        vacancies.currency,
                        vacancies.url AS vacancy_url
                    FROM vacancies
                    JOIN companies ON vacancies.company_id = companies.company_id
                    WHERE ((vacancies.salary_from + vacancies.salary_to) / 2 > %s)
                    ORDER BY ((vacancies.salary_from + vacancies.salary_to) / 2) DESC;
                    """,
                (avg_salary,),
            )
            result = cur.fetchall()
            self.disconnect()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[Tuple]:
        """Получение списка вакансий, содержащих ключевое слово в названии."""
        self.connect()
        with self.conn.cursor() as cur:
            search_pattern = f"%{keyword}%"
            cur.execute(
                """
                    SELECT
                        companies.name AS company_name,
                        vacancies.name AS vacancy_name,
                        vacancies.salary_from,
                        vacancies.salary_to,
                        vacancies.currency,
                        vacancies.url AS vacancy_url
                    FROM vacancies
                    JOIN companies ON vacancies.company_id = companies.company_id
                    WHERE vacancies.name ILIKE %s
                    ORDER BY company_name, vacancy_name;
                    """,
                (search_pattern,),
            )
            result = cur.fetchall()
            self.disconnect()
        return result
