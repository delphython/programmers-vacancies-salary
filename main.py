import datetime
import os

import requests
from dotenv import load_dotenv
from terminaltables import SingleTable


def fetch_hh_vacancies(text, area, date_from, *_):
    vacancies = []
    page = 0
    pages_number = 1

    hh_api_url = "https://api.hh.ru/vacancies"
    params = {
      "text": text,
      "area": area,
      "date_from": date_from,
    }

    while page < pages_number:
        params.update({"page": page})
        page_response = requests.get(hh_api_url, params)
        page_response.raise_for_status()

        vacancies_on_page = page_response.json()

        pages_number = vacancies_on_page["pages"]
        page += 1

        vacancies += vacancies_on_page["items"]

    found = vacancies_on_page["found"]

    return vacancies, found


def fetch_sj_vacancies(keyword, town, date_published_from, token):
    vacancies_on_page_count = 20
    vacancies_catalogue_section = 48
    vacancies = []
    page = 0
    is_next_page = True

    sj_api_url = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": token,
    }
    params = {
        "town": town,
        "keyword": keyword,
        "catalogues": vacancies_catalogue_section,
        "date_published_from": date_published_from,
        "count": vacancies_on_page_count,
    }

    while is_next_page:
        params.update({"page": page})
        page_response = requests.get(
            sj_api_url, params=params, headers=headers)
        page_response.raise_for_status()

        vacancies_on_page = page_response.json()
        is_next_page = vacancies_on_page["more"]
        page += 1

        vacancies += vacancies_on_page["objects"]

    found = vacancies_on_page["total"]

    return vacancies, found


def get_vacancies_statistic(
    fetch_vacancies_function,
    predict_rub_salary_function,
    prog_languages,
    job_area,
    vacancies_period,
    token=None
):
    job_statistics = {}

    for prog_language in prog_languages:
        salary_sum = 0
        vacancies_processed = 0
        job_specialization = f"Программист {prog_language}"

        vacancies, found = fetch_vacancies_function(
            job_specialization, job_area, vacancies_period, token)

        for vacancy in vacancies:
            rub_salary = predict_rub_salary_function(vacancy)
            if rub_salary:
                salary_sum += rub_salary
                vacancies_processed += 1

        average_salary = int(
            salary_sum / vacancies_processed) if vacancies_processed else 0

        job_statistics[prog_language] = {
            "vacancies_found": found,
            "average_salary": average_salary,
            "vacancies_processed": vacancies_processed,
        }

    return job_statistics


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        return salary_from * 1.2
    elif not salary_from and salary_to:
        return salary_to * 0.8


def predict_rub_salary_hh(vacancy):
    salary = vacancy["salary"]
    if salary and salary["currency"] == "RUR":
        return predict_rub_salary(salary["from"], salary["to"])


def predict_rub_salary_sj(vacancy):
    if vacancy["currency"] == "rub":
        return predict_rub_salary(
            vacancy["payment_from"],
            vacancy["payment_to"]
        )


def get_vacancies_statistics_table(title, job_statistics):
    vacancies_statistics_table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]

    for prog_lang, statistics in job_statistics.items():
        vacancies_statistics_table.append(
           [
               prog_lang,
               statistics["vacancies_found"],
               statistics["vacancies_processed"],
               statistics["average_salary"],
           ]
        )

    table_instance = SingleTable(vacancies_statistics_table, title)

    return table_instance.table


def main():
    load_dotenv()

    sj_api_key = os.environ["SUPERJOB_API_KEY"]
    sj_job_area = 4
    hh_job_area = 1
    vacancies_search_days = 30
    hh_title = "HeadHunter Moscow"
    sj_title = "SuperJob Moscow"

    prog_languages = [
        "Java",
        "Python",
        "Ruby",
        "PHP",
        "C++",
        "C#",
        "Go",
        "Scala",
        "Swift",
    ]

    date_search_from = (
        datetime.datetime.now() - datetime.timedelta
        (days=vacancies_search_days)).date()

    hh_statistic = get_vacancies_statistic(
        fetch_hh_vacancies,
        predict_rub_salary_hh,
        prog_languages, hh_job_area,
        date_search_from
    )
    sj_statistic = get_vacancies_statistic(
        fetch_sj_vacancies,
        predict_rub_salary_sj,
        prog_languages,
        sj_job_area,
        date_search_from,
        sj_api_key
    )

    print(get_vacancies_statistics_table(hh_title, hh_statistic))
    print(get_vacancies_statistics_table(sj_title, sj_statistic))


if __name__ == "__main__":
    main()
