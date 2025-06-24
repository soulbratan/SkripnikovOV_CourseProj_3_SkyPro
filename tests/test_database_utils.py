def test_create_database(test_dbname: str, sample_db_params: dict[str, str]) -> None:
    """Проверяет создание базы данных и таблиц"""
    from src.database_utils import create_database

    create_database(test_dbname, sample_db_params)

    # Проверяем, что база данных создана и таблицы существуют
    import psycopg2

    conn = psycopg2.connect(dbname=test_dbname, **sample_db_params)
    with conn.cursor() as cur:
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = [table[0] for table in cur.fetchall()]
        assert "companies" in tables  # Таблица companies должна существовать
        assert "vacancies" in tables  # Таблица vacancies должна существовать
    conn.close()


def test_save_data_to_database(test_dbname: str, sample_db_params: dict[str, str], sample_employers_id) -> None:
    """Проверяет сохранение данных в базу"""
    from src.database_utils import create_database, save_data_to_database
    from src.HH_api import get_hh_data_short

    # Создаем базу и таблицы
    create_database(test_dbname, sample_db_params)

    # Получаем тестовые данные
    hh_data = get_hh_data_short(sample_employers_id)

    # Сохраняем данные
    save_data_to_database(hh_data, test_dbname, sample_db_params)

    # Проверяем, что данные сохранены
    import psycopg2

    conn = psycopg2.connect(dbname=test_dbname, **sample_db_params)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM companies")
        companies_count = cur.fetchone()[0]
        assert companies_count > 0  # Должны быть добавлены компании

        cur.execute("SELECT COUNT(*) FROM vacancies")
        vacancies_count = cur.fetchone()[0]
        assert vacancies_count > 0  # Должны быть добавлены вакансии
    conn.close()
