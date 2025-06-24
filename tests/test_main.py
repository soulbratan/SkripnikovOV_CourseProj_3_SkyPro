from unittest.mock import MagicMock

import main


def test_main_full_data_flow(mock_dependencies) -> None:
    emps_id = ["15478", "1740", "3529", "78638", "4181", "80", "1057", "3776", "2381", "84585"]
    # Настраиваем моки
    mock_dependencies["mock_input"].side_effect = ["1", "1", "0"]  # Выбор полных данных и выход
    mock_dependencies["mock_get_full"].return_value = [{"test": "data"}]

    # Создаем мок для DBManager
    db_manager_instance = MagicMock()
    db_manager_instance.get_companies_and_vacancies_count.return_value = [("Company", 5)]
    db_manager_instance.get_all_vacancies.return_value = []
    db_manager_instance.get_avg_salary.return_value = 50000
    db_manager_instance.get_vacancies_with_higher_salary.return_value = []
    db_manager_instance.get_vacancies_with_keyword.return_value = []
    mock_dependencies["mock_dbmanager"].return_value = db_manager_instance

    # Запускаем main
    main.main()

    # Проверяем вызовы
    mock_dependencies["mock_get_full"].assert_called_once_with(emps_id)
    mock_dependencies["mock_create_db"].assert_called_once()
    mock_dependencies["mock_save_data"].assert_called_once()
    db_manager_instance.get_companies_and_vacancies_count.assert_called_once()


def test_main_short_data_flow(mock_dependencies: MagicMock) -> None:
    emps_id = ["15478", "1740", "3529", "78638", "4181", "80", "1057", "3776", "2381", "84585"]
    # Настраиваем моки
    mock_dependencies["mock_input"].side_effect = ["2", "2", "0"]  # Выбор коротких данных и выход
    mock_dependencies["mock_get_short"].return_value = [{"test": "data"}]

    # Создаем мок для DBManager
    db_manager_instance = MagicMock()
    mock_dependencies["mock_dbmanager"].return_value = db_manager_instance

    # Запускаем main
    main.main()

    # Проверяем вызовы
    mock_dependencies["mock_get_short"].assert_called_once_with(emps_id)
    mock_dependencies["mock_create_db"].assert_called_once()
    mock_dependencies["mock_save_data"].assert_called_once()
    db_manager_instance.get_all_vacancies.assert_called_once()


def test_main_invalid_input_then_valid(mock_dependencies: MagicMock) -> None:
    # Настраиваем моки (сначала неверный ввод, потом верный)
    mock_dependencies["mock_input"].side_effect = ["3", "1", "0"]  # Неверный ввод, затем правильный
    mock_dependencies["mock_get_full"].return_value = [{"test": "data"}]

    # Создаем мок для DBManager
    db_manager_instance = MagicMock()
    mock_dependencies["mock_dbmanager"].return_value = db_manager_instance

    # Запускаем main
    main.main()

    # Проверяем, что было сообщение об ошибке
    assert "Неправильный ввод" in str(mock_dependencies["mock_print"].call_args_list)


def test_main_all_db_functions(mock_dependencies: MagicMock) -> None:
    # Настраиваем моки для проверки всех функций DBManager
    mock_dependencies["mock_input"].side_effect = ["1", "1", "2", "3", "4", "5", "python", "0"]
    mock_dependencies["mock_get_full"].return_value = [{"test": "data"}]

    # Создаем мок для DBManager с возвращаемыми значениями
    db_manager_instance = MagicMock()
    db_manager_instance.get_companies_and_vacancies_count.return_value = [("Company", 5)]
    db_manager_instance.get_all_vacancies.return_value = [("Company", "Vacancy", 100, 200, "RUB", "url")]
    db_manager_instance.get_avg_salary.return_value = 50000
    db_manager_instance.get_vacancies_with_higher_salary.return_value = [
        ("Company", "Vacancy", 60000, 80000, "RUB", "url")
    ]
    db_manager_instance.get_vacancies_with_keyword.return_value = [("Company", "Python Dev", 100, 200, "RUB", "url")]
    mock_dependencies["mock_dbmanager"].return_value = db_manager_instance

    # Запускаем main
    main.main()

    # Проверяем вызовы всех методов DBManager
    db_manager_instance.get_companies_and_vacancies_count.assert_called_once()
    db_manager_instance.get_all_vacancies.assert_called_once()
    db_manager_instance.get_avg_salary.assert_called_once()
    db_manager_instance.get_vacancies_with_higher_salary.assert_called_once()
    db_manager_instance.get_vacancies_with_keyword.assert_called_once_with("python")


def test_main_keyword_search(mock_dependencies: MagicMock) -> None:
    # Настраиваем моки для проверки поиска по ключевому слову
    mock_dependencies["mock_input"].side_effect = ["1", "5", "developer", "0"]
    mock_dependencies["mock_get_full"].return_value = [{"test": "data"}]

    # Создаем мок для DBManager
    db_manager_instance = MagicMock()
    db_manager_instance.get_vacancies_with_keyword.return_value = [
        ("Company", "Python Developer", 100, 200, "RUB", "url")
    ]
    mock_dependencies["mock_dbmanager"].return_value = db_manager_instance

    # Запускаем main
    main.main()

    # Проверяем вызов поиска с правильным ключевым словом
    db_manager_instance.get_vacancies_with_keyword.assert_called_once_with("developer")
    # Проверяем вывод результатов
    assert "Python Developer" in str(mock_dependencies["mock_print"].call_args_list)
