# Dvmn-hhru
Programmers' salaries statistics on [hh.ru](www.hh.ru) and [superjob.ru](www.superjob.ru) vacancies

## Description
The code prints out programmers' salaries statistics for vacancies placed at hh.ru and superjob.ru:
* in Moscow
* vacancies not older than 30 days
* only vacancies with shown salaries and only in RUB are taken into account

## Installation
0. You need python interpreter installed on your PС. The project is tested on Python 3.10.
1. Clone the project to your PC, details [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).
2. Install, run and activate your virtual environment, details [here](https://docs.python-guide.org/dev/virtualenvs/).
3. To install the dependencies, simply run 
```python
pip install -r requirements.txt
```
4. Hh.ru requires no token or password. To see superjob.ru statistics please get your secret key [here](https://api.superjob.ru/register). 
5. In the root directory of the project create a new file named `.env` with an environment variable `SJ_SECRET_KEY={your_secret_key_here}`.

## Example of use
```python
python main.py
```
```
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| C                     | 520              | 491                 | 119836           |
+-----------------------+------------------+---------------------+------------------+

+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Go                    | 200              | 186                 | 218664           |
| C#                    | 300              | 279                 | 215807           |
| C                     | 609              | 571                 | 220361           |
| C++                   | 400              | 374                 | 221450           |
| PHP                   | 500              | 469                 | 220855           |
| Python                | 609              | 571                 | 220361           |
| Java                  | 400              | 374                 | 221450           |
| JavaScript            | 609              | 571                 | 220361           |
+-----------------------+------------------+---------------------+------------------+
```

## Project goals
The code is written for educational purposes on online-course for web-developers dvmn.org.

## License
This software is licensed under the MIT License - see the [LICENSE](https://github.com/vdesyatke/Dvmn-hhru/blob/master/LICENSE) file for details.