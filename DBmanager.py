import os
import psycopg2


class DBmanager():
    def __init__(self, database):

        self.conn = psycopg2.connect(
            database=database,
            user=os.environ.get('pg_user'),
            password=os.environ.get('pg_pass')
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT employers.company_name, COUNT(vacancies.vacancy_id) FROM employers LEFT JOIN vacancies USING(employer_id) GROUP BY employers.company_name")
            result = cursor.fetchall()
            self.close_connection()  # Закрыть подключение к базе данных
            return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT title, salary_from, salary_to, vacancies.url, employers.company_name FROM vacancies LEFT JOIN employers USING(employer_id) ")
            result = cursor.fetchall()
            self.close_connection()  # Закрыть подключение к базе данных
            return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

        with self.conn.cursor() as cursor:
            cursor.execute("SELECT AVG((salary_from + salary_to) / NULLIF((CASE WHEN salary_from = 0 OR salary_to = 0 THEN 1 ELSE 2 END), 0)) FROM vacancies")
            average_salary = cursor.fetchone()[0]
            self.close_connection()  # Закрыть подключение к базе данных
            return average_salary

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT AVG((salary_from + salary_to) / NULLIF((CASE WHEN salary_from = 0 OR salary_to = 0 THEN 1 ELSE 2 END), 0)) FROM vacancies")
            average_salary = cursor.fetchone()[0]
            cursor.execute(
                "SELECT title, salary_from, salary_to, vacancies.url, employers.company_name FROM vacancies LEFT JOIN employers USING(employer_id) WHERE salary_from > %s OR salary_to > %s",
                (average_salary, average_salary))
            higher_salary_list = cursor.fetchall()
            self.close_connection()  # Закрыть подключение к базе данных
            return higher_salary_list

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python."""
        query = f"SELECT title, salary_from, salary_to, url FROM vacancies WHERE title LIKE '%{keyword}%'"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            self.close_connection()  # Закрыть подключение к базе данных
            return result

    def close_connection(self):
        """Закрывает подключение к базе данных"""
        self.conn.close()