"""
Модуль: plot_manager

Этот модуль предоставляет собой функции для исследования БД и её содержания
"""

import timeit

import mysql.connector
from mysql.connector import Error


def measure_delete_time(delete_func, *args):
    """
    Измеряет время выполнения удаления данных заданной функцией.

    Parameters:
    delete_func : function
        Функция, время выполнения удаления которой нужно измерить.
    *args
        Дополнительные аргументы для функции удаления.

    Returns:
    float
        Время выполнения функции в секундах.
    """
    start_time = timeit.default_timer()
    delete_func(*args)
    return timeit.default_timer() - start_time


def measure_query_time(query):
    """
    Измеряет время выполнения SQL-запроса.

    Parameters:
    query : str
        SQL-запрос для выполнения.

    Returns:
    float
        Время выполнения запроса в секундах.
    """
    setup_code = f'''
from lib.db_controller import execute_query
query = "{query}"
    '''
    query_code = '''
execute_query(query)
    '''

    time_taken = timeit.timeit(stmt=query_code, setup=setup_code, number=1)
    return time_taken


def show_database_content(host='localhost', user='admin', password='root', database='garden'):
    """
    Выводит содержимое базы данных MySQL.

    Parameters:
    host : str, optional
        Хост базы данных. По умолчанию 'localhost'.
    user : str, optional
        Имя пользователя. По умолчанию 'admin'.
    password : str, optional
        Пароль пользователя. По умолчанию 'root'.
    database : str, optional
        Имя базы данных. По умолчанию 'garden'.

    Returns:
    None
    """
    try:
        # Установка соединения с базой данных с использованием контекстного менеджера
        with mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as connection:
            print("Successfully connected to MySQL server")

            # Получаем список таблиц в базе данных
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()

                # Выводим содержимое каждой таблицы
                for table in tables:
                    table_name = table[0]
                    print(f"\nContents of table '{table_name}':")

                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()

                    # Выводим заголовки столбцов
                    column_names = [description[0] for description in cursor.description]
                    print(" | ".join(column_names))
                    print("-" * (len(" | ".join(column_names)) + len(column_names) * 3 - 1))

                    # Выводим данные таблицы
                    for row in rows:
                        print(" | ".join(str(item) for item in row))

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")


if __name__ == "__main__":
    show_database_content()
