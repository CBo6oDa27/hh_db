import psycopg2
import requests


def check_and_create_db():
    #Создаем новую базу данных для работы с проектом
    try:
        # Установка соединения с базой данных
        conn = psycopg2.connect(user="postgres", password="123123")
        # Создание курсора
        cursor = conn.cursor()
        # Проверка существования таблицы "vacancies"
        cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'vacancydb')")
        # Получение результата
        exists = cursor.fetchone()[0]

        # Закрытие курсора и соединения
        if exists:
            cursor.close()
            conn.close()
            # Не нужно создавать и заполнять базу
            return
        else:
            with conn.cursor() as cursor:
                conn.autocommit = True
                cursor.execute("CREATE DATABASE vacancydb")
            conn.close()
    except:
        pass

    #Обращаемся по API HH и получаем список вакансий по заданным компаниям
    response = requests.get(
        "https://api.hh.ru/vacancies?",
        headers={"HH-User-Agent": 'VacancyMachine/1.0 (zakirov.alexey@gmail.com)'},
        params={"employer_id": (1740, 3529, 15478, 78638, 740, 3388, 23186, 3776, 6041, 4233, 2180), "per_page": 100}
    )
    # Cоздаем структуру БД и записываем в нее полученные от HH данные
    with psycopg2.connect(database="vacancydb", user="postgres", password="123123") as conn:


        with conn.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE employers(employer_id int PRIMARY KEY NOT NULL, company_name varchar(255), url varchar(255));")
            cursor.execute("CREATE TABLE vacancies(vacancy_id int PRIMARY KEY NOT NULL, salary_from int, salary_to int, title varchar(255), url varchar(255), employer_id int REFERENCES employers(employer_id))")
            for item in response.json()['items']:
                if item['salary'] is None:
                    salary_from = 0
                    salary_to = 0
                else:
                    salary_from = item['salary']['from']
                    salary_to = item['salary']['to']
                if salary_from == None:
                    salary_from = 0
                if salary_to == None:
                    salary_to = 0

                cursor.execute(
                    "INSERT INTO employers (employer_id, company_name, url) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                    (item['employer']['id'], item['employer']['name'], item['employer']['alternate_url']))

                cursor.execute("INSERT INTO vacancies (vacancy_id, salary_from, salary_to, title, url, employer_id) VALUES (%s, %s, %s, %s, %s, %s)",
                    (item['id'], salary_from, salary_to, item['name'], item['alternate_url'], item['employer']['id']))
