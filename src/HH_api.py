import requests
from typing import Any

def get_hh_data_short(employers_id: list[str]) -> list[dict[str, Any]]:
    """
    Функция получения данных от API HH.ru. Функция возвращает вакансии первой страницы.
    :param employers_id: Список ID выбираемых компаний.
    :return: Возвращает список словарей с информацией о компании и её вакансиями.
    """
    data = []
    for employer_id in employers_id:
        # Получаем данные о компании и формируем словарь с данными
        url_emp_inf = f"https://api.hh.ru/employers/{employer_id}"
        response_emp_inf = requests.get(url_emp_inf)
        company_data = response_emp_inf.json()

        company_inf = {
            "name": company_data["name"],
            "area": company_data["area"]["name"],
            "open_vacancies": company_data["open_vacancies"],
            "industries": company_data["industries"],
            "url": company_data["alternate_url"],
            "vacancies_url": company_data["vacancies_url"],
        }

        # Получаем вакансии от компании и формируем словарь с вакансиями
        url_vac = "https://api.hh.ru/vacancies"
        page_n = 0
        data_vacs = []
        params = {"employer_id": employer_id, "per_page": 100, "page": page_n}
        response_vac = requests.get(url_vac, params)
        data_vac = response_vac.json()
        vacancies = []
        for vac in data_vac["items"]:
            name = vac["name"]
            area = vac["area"].get("name") if vac["area"].get("name") is not None else "Нет данных"
            salary = vac.get("salary")
            if salary == None:
                salary = {"salary": 0,
                          "salary_range": 0,
                          "currency": "Не указана"}
            salary_from = salary.get("from") if salary.get("from") is not None else 0
            salary_to = salary.get("to") if salary.get("to") is not None else salary_from
            currency = salary.get("currency") if salary.get("currency") is not None else "Не указано"
            published_at = vac["published_at"]
            responsibility = vac["snippet"]["responsibility"]
            url = vac["alternate_url"]
            vacancy_inf = {
                "name": name,
                "area": area,
                "salary_from": salary_from,
                "salary_to": salary_to,
                "currency": currency,
                "published_at": published_at,
                "responsibility": responsibility,
                "url": url
            }
            vacancies.append(vacancy_inf)
        data_vacs.extend(vacancies)

        data.append({"company": company_inf, "vacancies": data_vacs})
    return data


def get_hh_data_full(employers_id: list[str]) -> list[dict[str, Any]]:
    """
    Функция получения данных от API HH.ru. Функция возвращает все вакансии работодателя.
    :param employers_id: Список ID выбираемых компаний.
    :return: Возвращает список словарей с информацией о компании и её вакансиями.
    """
    data = []
    for employer_id in employers_id:
        # Получаем данные о компании и формируем словарь с данными
        url_emp_inf = f"https://api.hh.ru/employers/{employer_id}"
        response_emp_inf = requests.get(url_emp_inf)
        company_data = response_emp_inf.json()

        company_inf = {
            "name": company_data["name"],
            "area": company_data["area"]["name"],
            "open_vacancies": company_data["open_vacancies"],
            "industries": company_data["industries"],
            "url": company_data["alternate_url"],
            "vacancies_url": company_data["vacancies_url"],
        }

        # Получаем вакансии от компании и формируем словарь с вакансиями
        url_vac = "https://api.hh.ru/vacancies"
        page_n = 0
        data_vacs = []
        while True:
            params = {"employer_id": employer_id, "per_page": 100, "page": page_n}
            response_vac = requests.get(url_vac, params)
            data_vac = response_vac.json()
            if len(data_vac.get("items", "")) == 0:
                break
            vacancies = []
            for vac in data_vac["items"]:
                name = vac["name"]
                area = vac["area"].get("name") if vac["area"].get("name") is not None else "Нет данных"
                salary = vac.get("salary")
                if salary == None:
                    salary = {"salary": 0,
                              "salary_range": 0,
                              "currency": "Не указана"}
                salary_from = salary.get("from") if salary.get("from") is not None else 0
                salary_to = salary.get("to") if salary.get("to") is not None else salary_from
                currency = salary.get("currency") if salary.get("currency") is not None else "Не указано"
                published_at = vac["published_at"]
                responsibility = vac["snippet"]["responsibility"]
                url = vac["alternate_url"]
                vacancy_inf = {
                    "name": name,
                    "area": area,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency,
                    "published_at": published_at,
                    "responsibility": responsibility,
                    "url": url
                }
                vacancies.append(vacancy_inf)
            data_vacs.extend(vacancies)
            page_n += 1

        data.append({"company": company_inf, "vacancies": data_vacs})
    return data
