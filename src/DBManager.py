import psycopg2
from typing import Any
from abc import ABC, abstractmethod


class DBase(ABC):
    """Абстрактный класс для работы с базой данных о вакансиях"""

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_avg_salary(self) -> float:
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list[dict[str, Any]]:
        pass



class DBManager(DBase):
    """Класс для работы с базой данных вакансий. Наследуется от DBase."""
    def __init__(self, dbname:str, params: dict) -> None:
        """Инициализация параметров подключения"""
        self.dbname = dbname
        self.params = params
        self.conn = None

    def connect(self):
        """Соединение с базой данных"""
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(dbname=self.dbname, **self.params)
            self.conn.autocommit = True
        return self.conn

    def disconnect(self):
        """Закрытие соединения с базой данных"""
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Поддержка контекстного менеджера"""
        self.disconnect()

    def get_companies_and_vacancies_count(self) -> list[dict[str, Any]]:
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.name AS company_name, COUNT (vacancy_id) AS vacancies_count
                FROM companies
                LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
                GROUP BY companies.company_id, companies.name
                ORDER BY vacancies_count DESC;
                """)
            result = cur.fetchall()
            self.disconnect()
        return result

    def get_all_vacancies(self) -> list[dict[str, Any]]:
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
                """)
            result = cur.fetchall()
            self.disconnect()
        return result

    def get_avg_salary(self) -> float:
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies;
                """)
            result = cur.fetchone()
            self.disconnect()
        return round(result[0], 2)

    def get_vacancies_with_higher_salary(self) -> list[dict[str, Any]]:
        self.connect()
        with self.conn.cursor() as cur:
            cur.execute(
                    """
                    SELECT AVG((salary_from + salary_to) / 2) 
                    FROM vacancies;
                    """)
            avg_salary = cur.fetchone()[0]

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
                    """, (avg_salary,))
            result = cur.fetchall()
            self.disconnect()
        return result


    def get_vacancies_with_keyword(self, keyword: str) -> list[dict[str, Any]]:
        self.connect()
        with self.conn.cursor() as cur:
            search_pattern = f'%{keyword}%'
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
                    """, (search_pattern,))
            result = cur.fetchall()
            self.disconnect()
        return result
