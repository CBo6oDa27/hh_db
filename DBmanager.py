import os
import psycopg2


class DBmanager():
    def __init__(self, database):
        self.conn = psycopg2.connect(
            database=database,
            user="postgres",
            password="123123"
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT employers.company_name, COUNT(vacancies.vacancy_id) FROM employers LEFT JOIN vacancies USING(employer_id) GROUP BY employers.company_name")
            return cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT title, salary_from, salary_to, vacancies.url, employers.company_name FROM vacancies LEFT JOIN employers USING(employer_id) ")
            return cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""

        with self.conn.cursor() as cursor:
            cursor.execute("SELECT salary_from, salary_to FROM vacancies")
            count = 0
            gross_salary = 0
            for row in cursor.fetchall():
                if row[0] != 0 and row[1] != 0:
                    gross_salary += (row[1] - row[0])/2 + row[0]
                    count += 1
                elif row[0] != 0 and row[1] == 0:
                    gross_salary += row[0]
                    count += 1
                elif row[0] == 0 and row[1] != 0:
                    gross_salary += row[1]
                    count += 1
            return gross_salary / count

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        average_salary = int(self.get_avg_salary())
        higher_salary_list=[]
        for row in self.get_all_vacancies():
            if row[1] > average_salary:
                higher_salary_list.append(row)
            elif row[2]  > average_salary:
                higher_salary_list.append(row)
            elif (row[2] - row[1])/2 + row[1] > average_salary:
                higher_salary_list.append(row)
        return higher_salary_list

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python."""
        query = f"SELECT title, salary_from, salary_to, url FROM vacancies WHERE title LIKE '%{keyword}%'"
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()