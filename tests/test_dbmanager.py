from src.database_utils import create_database, save_data_to_database
from src.HH_api import get_hh_data_short


def test_dbmanager_initialization(db_manager) -> None:
    """Проверяет инициализацию DBManager"""
    assert db_manager.dbname  # Имя базы данных должно быть установлено"
    assert db_manager.params  # Параметры подключения должны быть установлены"


def test_connect_disconnect(db_manager) -> None:
    """Проверяет подключение и отключение от базы данных"""
    conn = db_manager.connect()
    assert conn is not None  # "Подключение не должно быть None"
    assert not conn.closed  # "Подключение должно быть активным"

    db_manager.disconnect()
    assert conn.closed  # "Подключение должно быть закрыто"


def test_get_companies_and_vacancies_count(db_manager, test_dbname, sample_db_params, sample_employers_id) -> None:
    """Проверяет метод get_companies_and_vacancies_count"""

    # Подготавливаем тестовые данные
    create_database(test_dbname, sample_db_params)
    hh_data = get_hh_data_short(sample_employers_id)
    save_data_to_database(hh_data, test_dbname, sample_db_params)

    # Тестируем метод
    result = db_manager.get_companies_and_vacancies_count()
    assert isinstance(result, list)  # "Метод должен возвращать список"
    assert len(result) > 0  # "Список не должен быть пустым"
    for item in result:
        assert isinstance(item, tuple)  # "Каждый элемент должен быть кортежем"
        assert len(item) == 2  # "Каждый кортеж должен содержать 2 элемента"
        assert isinstance(item[0], str)  # "Первый элемент должен быть строкой (название компании)"
        assert isinstance(item[1], int)  # "Второй элемент должен быть целым числом (количество вакансий)"


def test_get_all_vacancies(db_manager, test_dbname, sample_db_params, sample_employers_id) -> None:
    """Проверяет метод get_all_vacancies"""

    # Подготавливаем тестовые данные
    create_database(test_dbname, sample_db_params)
    hh_data = get_hh_data_short(sample_employers_id)
    save_data_to_database(hh_data, test_dbname, sample_db_params)

    # Тестируем метод
    result = db_manager.get_all_vacancies()
    assert isinstance(result, list)  # "Метод должен возвращать список"
    if len(result) > 0:
        for item in result:
            assert isinstance(item, tuple)  # "Каждый элемент должен быть кортежем"
            assert len(item) == 6  # "Каждый кортеж должен содержать 6 элементов"


def test_get_avg_salary(db_manager, test_dbname, sample_db_params, sample_employers_id) -> None:
    """Проверяет метод get_avg_salary"""

    # Подготавливаем тестовые данные
    create_database(test_dbname, sample_db_params)
    hh_data = get_hh_data_short(sample_employers_id)
    save_data_to_database(hh_data, test_dbname, sample_db_params)


def test_get_vacancies_with_keyword(db_manager, test_dbname, sample_db_params, sample_employers_id) -> None:
    """Проверяет метод get_vacancies_with_keyword"""

    # Подготавливаем тестовые данные
    create_database(test_dbname, sample_db_params)
    hh_data = get_hh_data_short(sample_employers_id)
    save_data_to_database(hh_data, test_dbname, sample_db_params)

    # Тестируем метод
    keyword = "разработчик"
    result = db_manager.get_vacancies_with_keyword(keyword)
    assert isinstance(result, list)  # "Метод должен возвращать список"
    if len(result) > 0:
        for item in result:
            assert isinstance(item, tuple)  # "Каждый элемент должен быть кортежем"
            assert len(item) == 6  # "Каждый кортеж должен содержать 6 элементов"
            assert keyword.lower() in item[1].lower()  # "Название вакансии должно содержать ключевое слово"
