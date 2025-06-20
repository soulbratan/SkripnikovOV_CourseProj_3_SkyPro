import psycopg2
from typing import Any

def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f"DROP DATABASE {database_name}")
    except Exception as e:
        print(f'Информация: {e}')
    finally:
        cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
                company_id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                area VARCHAR(255) NOT NULL,
                open_vacancies INT,
                industries VARCHAR(255),
                url VARCHAR(255),
                vacancies_url VARCHAR(255)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INT REFERENCES companies(company_id),
                name VARCHAR(255) NOT NULL,
                area VARCHAR(255) NOT NULL,
                salary_from INT,
                salary_to INT,
                currency VARCHAR(10),
                published_at DATE,
                responsibility VARCHAR(255),
                url VARCHAR(255)
            )
        """)

    conn.commit()
    conn.close()

def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE companies, vacancies RESTART IDENTITY CASCADE;")
        for company in data:
            company_data = company["company"]
            cur.execute(
            """
                INSERT INTO companies (name, area, open_vacancies, industries, url,vacancies_url)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING company_id
                """, (company_data["name"], company_data["area"], company_data["open_vacancies"], company_data["industries"][0]["name"], company_data["url"], company_data["vacancies_url"]))
            company_id = cur.fetchone()[0]

            vacancies_data = company["vacancies"]
            for vacancy in vacancies_data:
                cur.execute(
                """
                     INSERT INTO vacancies (company_id, name, area, salary_from, salary_to, currency, published_at, responsibility, url)
                     VALUES (%s, %s, %s, %s, %s, %s)
                    """, (company_id, vacancy["name"], vacancy["area"], vacancy["salary_from"], vacancy["salary_to"], vacancy["currency"], vacancy["published_at"], vacancy["responsibility"], vacancy["url"]))

    conn.commit()
    conn.close()