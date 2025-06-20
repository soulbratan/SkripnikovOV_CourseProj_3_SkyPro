from src.config import config
from src.database_utils import create_database, save_data_to_database
from src.DBManager import DBManager
from src.HH_api import get_hh_data_full, get_hh_data_short


def main() -> None:
    """Функция взаимодействия с пользователем. Объединяет логику проекта"""
    # Записываем ID выбранных компаний переменную
    employers_id = ["15478", "1740", "3529", "78638", "4181", "80", "1057", "3776", "2381", "84585"]
    running = True

    # Запускаем цикл
    while running:
        print(
            "Выберите действие:\n1. Получить данные о компаниях и всех вакансиях компании.\n"
            "2. Получить данные о компаниях и до 100 вакансий компании."
        )
        choose_one = int(input("Введите -> "))
        if choose_one == 1:
            print("Ожидайте получения данных!\n")

            # Если <1> то получаем полный список вакансий, которые есть у работодателя
            hh_data = get_hh_data_full(employers_id)

            # Выходим из цикла
            running = False
        elif choose_one == 2:
            print("Ожидайте получения данных!\n")

            # Если <2> то получаем список до 100 вакансий, которые есть у работодателя
            hh_data = get_hh_data_short(employers_id)

            # Выходим из цикла
            running = False
        else:
            print("Неправильный ввод. Введите '1' или '2'")

    # Записываем название БД в переменную
    dbname = "vacancies_db"
    print(f"Создаём базу данных <{dbname}>")

    # Получаем конфигурацию для postgreSQL
    params = config("database.ini")

    # Создаём БД
    create_database(dbname, params)
    print(f"Заполняем базу данных <{dbname}> полученными с API HH данными.")

    # Заполняем БД полученными данными от HH API.ru
    save_data_to_database(hh_data, dbname, params)

    # Создаём экземпляр класса DBManager
    dbmanager = DBManager(dbname, params)

    running = True
    while running:
        print("\nВыберите действие для работы с БД:")
        print("1. Получить список всех компаний и количество вакансий у каждой компании.")
        print("2. Получить список всех вакансий.")
        print("3. Получить среднюю зарплату по вакансиям.")
        print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
        print("5. Получить список всех вакансий по ключевому слову.")
        print("0. Завершить работу.")
        try:
            choose_two = int(input("Введите -> "))
        except ValueError:
            choose_two = 6
        if choose_two == 1:
            result = dbmanager.get_companies_and_vacancies_count()
            for i in range(len(result)):
                if len(result[i]) > 0:
                    company_name = result[i][0]
                    vacancies_count = result[i][1]
                    print(f"\n{i + 1}) Компания: {company_name}. Количество вакансий: {vacancies_count}")
        elif choose_two == 2:
            result = dbmanager.get_all_vacancies()
            for i in range(len(result)):
                if len(result[i]) > 0:
                    company_name = result[i][0]
                    vacancies_name = result[i][1]
                    salary_from = result[i][2]
                    salary_to = result[i][3]
                    currency = result[i][4]
                    url = result[i][5]
                    print(
                        f"\n{i + 1})\nКомпания: {company_name}.\nВакансия: {vacancies_name}\n"
                        f"ЗП от: {salary_from}\nЗП до: {salary_to}\nВалюта: {currency}\nСсылка: {url}"
                    )
        elif choose_two == 3:
            result = dbmanager.get_avg_salary()  # type: ignore
            print(f"Средняя зарплата: {result}")
        elif choose_two == 4:
            result = dbmanager.get_vacancies_with_higher_salary()
            for i in range(len(result)):
                if len(result[i]) > 0:
                    company_name = result[i][0]
                    vacancies_name = result[i][1]
                    salary_from = result[i][2]
                    salary_to = result[i][3]
                    currency = result[i][4]
                    url = result[i][5]
                    print(
                        f"\n{i + 1})\nКомпания: {company_name}.\nВакансия: {vacancies_name}\n"
                        f"ЗП от: {salary_from}\nЗП до: {salary_to}\nВалюта: {currency}\nСсылка: {url}"
                    )
        elif choose_two == 5:
            keyword = input("Введите ключевое слово -> ")
            result = dbmanager.get_vacancies_with_keyword(keyword)
            for i in range(len(result)):
                if len(result[i]) > 0:
                    company_name = result[i][0]
                    vacancies_name = result[i][1]
                    salary_from = result[i][2]
                    salary_to = result[i][3]
                    currency = result[i][4]
                    url = result[i][5]
                    print(
                        f"\n{i + 1})\nКомпания: {company_name}.\nВакансия: {vacancies_name}\n"
                        f"ЗП от: {salary_from}\nЗП до: {salary_to}\nВалюта: {currency}\nСсылка: {url}"
                    )
        elif choose_two == 0:
            running = False
        else:
            print("\nВы ничего не выбрали. Попробуйте ещё раз!")


if __name__ == "__main__":
    main()
