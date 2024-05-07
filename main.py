import requests
from environs import Env
import time
from datetime import date, timedelta
from terminaltables import AsciiTable


POPULAR_LANGUAGES = (
    'Go', 'C#', 'C', 'C++', 'PHP', 'Python', 'Java', 'JavaScript',
)


def get_vacancies(area=1, only_with_salary=False, period=3650,
                  language=None, per_page=100, page=0):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': area,
        'only_with_salary': only_with_salary,
        'period': period,
        'per_page': per_page,
        'page': page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['items']


def get_all_vacancies_hh(area=1, only_with_salary=False, per_page=100,
                         period=3650, language=None):
    language = language or ''
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': area,
        'only_with_salary': only_with_salary,
        'period': period,
        'per_page': per_page,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_json = response.json()
    pages = response_json['pages']
    vacancies = response_json['items']
    for page in range(1, pages):
        vacancies.extend(
            get_vacancies(period=30, language=language, page=page, only_with_salary=only_with_salary)
        )
    return vacancies


def get_salaries_stats_hh(popular_languages=POPULAR_LANGUAGES):
    table_data = []
    for language in popular_languages:
        vacancies = get_all_vacancies_hh(language=language, period=30, only_with_salary=True)
        countable_salaries = tuple(
            salary for vacancy in vacancies if (salary := predict_rub_salary(vacancy))
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
    return table_data


def print_salaries(table_data, title):
    table_data.insert(0, ('Язык программирования',
                          'Вакансий найдено',
                          'Вакансий обработано',
                          'Средняя зарплата',
                          )
                      )
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)
    print()


def predict_rub_salary(vacancy):
    if 'currency' in vacancy:
        currency = vacancy['currency']
        payment_from = vacancy.get('payment_from')
        payment_to = vacancy.get('payment_to')
    elif 'salary' in vacancy:
        currency = vacancy['salary']['currency']
        payment_from = vacancy['salary'].get('from')
        payment_to = vacancy['salary'].get('to')
    else:
        return None

    if currency not in ('rub', 'RUR'):
        return None
    if not payment_to and not payment_from:
        return None
    if not payment_from:
        return payment_to * 0.8
    if not payment_to:
        return payment_from * 1.2
    return (payment_to + payment_from) * 0.5


def get_unixdate_month_ago():
    date_published_from = date.today() - timedelta(days=30)
    date_published_from = int(time.mktime(date_published_from.timetuple()))
    return date_published_from


def get_all_vacancies_sj(secret_key, town=4, count=40, language=None):
    language = language or ''
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}
    date_published_from = get_unixdate_month_ago()
    params = {
        'town': town,
        'keyword': language,
        'count': count,
        'date_published_from': date_published_from
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    response_json = response.json()

    pages = (response_json['total'] + count - 1) // count
    vacancies = response_json['objects']
    for page in range(1, pages):
        params['page'] = page
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies.extend(response.json()['objects'])
    return vacancies


def get_salaries_stats_sj(secret_key, popular_languages=POPULAR_LANGUAGES):
    table_data = []
    for language in popular_languages:
        vacancies = get_all_vacancies_sj(secret_key=secret_key, language=language)
        countable_salaries = tuple(
            salary for vacancy in vacancies if (salary := predict_rub_salary(vacancy))
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
    return table_data


def main():
    env = Env()
    env.read_env()
    table_data_sj = get_salaries_stats_sj(secret_key=env('SJ_SECRET_KEY'))
    print_salaries(table_data=table_data_sj, title='SuperJob Moscow')
    table_data_hh = get_salaries_stats_hh()
    print_salaries(table_data=table_data_hh, title='HeadHunter Moscow')


if __name__ == '__main__':
    main()
