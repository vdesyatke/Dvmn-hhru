import requests
from environs import Env
import time
from datetime import date, timedelta
from terminaltables import AsciiTable


POPULAR_LANGUAGES = (
    'Go', 'C#', 'C', 'C++', 'PHP', 'Python', 'Java', 'JavaScript',
)


def get_vacancies(area=1, only_with_salary=True, period=None,
                  language=None, per_page=100, page=0):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': area,
        'only_with_salary': only_with_salary,
        'period': period or 3650,
        'per_page': per_page,
        'page': page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items']


def get_all_vacancies_hh(area=1, only_with_salary=True, per_page=100,
                         period=None, language=None):
    language = language or ''
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': area,
        'only_with_salary': only_with_salary,
        'period': period or 3650,
        'per_page': per_page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    pages = response.json()['pages']
    vacancies = list()
    for page in range(pages):
        vacancies.extend(
            get_vacancies(period=30, language='Python', page=page)
        )
    return vacancies


def predict_rub_salary_hh(vacancy):
    if vacancy['salary']['currency'] != 'RUR':
        return
    if not vacancy['salary']['from']:
        return vacancy['salary']['to'] * 0.8
    if not vacancy['salary']['to']:
        return vacancy['salary']['from'] * 1.2
    return (vacancy['salary']['to'] + vacancy['salary']['from']) * 0.5


def print_salaries_hh(popular_languages=POPULAR_LANGUAGES):
    table_data = [
        ('Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'),
    ]
    for language in popular_languages:
        vacancies = get_all_vacancies_hh(language=language, period=30)
        countable_salaries = tuple(
            predict_rub_salary_hh(vacancy)
            for vacancy in vacancies
            if predict_rub_salary_hh(vacancy)
        )
        vacancies_processed = len(countable_salaries)
        average_salary = int(
            sum(countable_salaries) / vacancies_processed
        )
        table_data.append(
            (language, len(vacancies), vacancies_processed, average_salary),
        )
    title = 'HeadHunter Moscow'
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)
    print()


def predict_rub_salary_sj(vacancy):
    if vacancy['currency'] != 'rub':
        return None
    if not vacancy['payment_to'] and not vacancy['payment_from']:
        return None
    if not vacancy['payment_from']:
        return vacancy['payment_to'] * 0.8
    if not vacancy['payment_to']:
        return vacancy['payment_from'] * 1.2
    return (vacancy['payment_to'] + vacancy['payment_from']) * 0.5


def get_unixdate_month_ago():
    date_published_from = date.today() - timedelta(days=30)
    date_published_from = int(time.mktime(date_published_from.timetuple()))
    return date_published_from


def get_all_vacancies_sj(town=4, count=40, language=None):
    language = language or ''
    env = Env()
    env.read_env()
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': env('SECRET_KEY')}
    date_published_from = get_unixdate_month_ago()
    params = {
        'town': town,
        'keyword': language,
        'count': count,
        'date_published_from': date_published_from
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    pages = (response.json()['total'] + count - 1) // count
    vacancies = response.json()['objects']
    for page in range(1, pages):
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        vacancies.extend(response.json()['objects'])
    return vacancies


def print_salaries_sj(popular_languages=POPULAR_LANGUAGES):
    table_data = [
        ('Язык программирования', 'Вакансий найдено',
         'Вакансий обработано', 'Средняя зарплата'),
    ]
    for language in popular_languages:
        vacancies = get_all_vacancies_sj(language=language)
        countable_salaries = tuple(
            predict_rub_salary_sj(vacancy)
            for vacancy in vacancies
            if predict_rub_salary_sj(vacancy)
        )
        vacancies_processed = len(countable_salaries)
        try:
            average_salary = int(
                sum(countable_salaries) / vacancies_processed
            )
        except ZeroDivisionError:
            average_salary = 'No salary info for this programming language'
        table_data.append(
            (language, len(vacancies), vacancies_processed, average_salary),
        )
    title = 'SuperJob Moscow'
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)
    print()


def main():
    print_salaries_sj()
    print_salaries_hh()


if __name__ == '__main__':
    main()
