from createDB import check_and_create_db
from DBmanager import DBmanager

def main():
    # Создадим базу если она еще не существует и не заполнена
    check_and_create_db()

    print("Выберите запрос, котороый необходимо выполнить?\n"
          "1 - Получить спсиок всех компаний и узнать количество вакансий у каждой компании? \n"
          "2 - Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n"
          "3 - Получить среднюю зарплату по вакансиям\n"
          "4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
          "Получить список всех вакансий по ключевому слову - введите ключевое слово\n")

    choice = input("Введите значение или клюечвое слово:")


    if choice == '1':
        for row in DBmanager('vacancydb').get_companies_and_vacancies_count():
            print(f"{row[0]} - {row[1]} вакансий")
    elif choice == '2':
        for row in DBmanager('vacancydb').get_all_vacancies():
            if row[1] == 0 and row[2] == 0:
                    salary = "Зарплата не указана."
            elif row[1] == 0 and row[2] != 0:
                salary = "Зарплата до " + str(row[2]) + " руб."
            elif row[1] != 0 and row[2] == 0:
                salary = "Зарплата от " + str(row[1]) + " руб."
            else:
                salary = "Зарплата от " + str(row[1])+ " до " + str(row[2]) + "  руб."

            print(f"{row[0]}. {salary} Ссылка: {row[3]} Компания: {row[4]}")
    elif choice == '3':
        print(f"Средняя зарплата по вакансиям составляет {int(DBmanager('vacancydb').get_avg_salary())} руб.")
    elif choice == '4':
            for row in DBmanager('vacancydb').get_vacancies_with_higher_salary():
                if row[1] == 0 and row[2] == 0:
                    salary = "Зарплата не указана."
                elif row[1] == 0 and row[2] != 0:
                    salary = "Зарплата до " + str(row[2]) + " руб."
                elif row[1] != 0 and row[2] == 0:
                    salary = "Зарплата от " + str(row[1]) + " руб."
                else:
                    salary = "Зарплата от " + str(row[1]) + " до " + str(row[2]) + "  руб."

                print(f"{row[0]}. {salary} Ссылка: {row[3]} Компания: {row[4]}")
    else:
        for row in DBmanager('vacancydb').get_vacancies_with_keyword(choice):
            if row[1] == 0 and row[2] == 0:
                    salary = "Зарплата не указана."
            elif row[1] == 0 and row[2] != 0:
                salary = "Зарплата до " + str(row[2]) + " руб."
            elif row[1] != 0 and row[2] == 0:
                salary = "Зарплата от " + str(row[1]) + " руб."
            else:
                salary = "Зарплата от " + str(row[1])+ " до " + str(row[2]) + "  руб."

            print(f"{row[0]}. {salary} Ссылка: {row[3]} ")

if __name__ == '__main__':
    main()