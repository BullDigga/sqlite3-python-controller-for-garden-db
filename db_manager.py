'''Данный модуль содержит функции, анализирующие работу с БД'''

import timeit
import matplotlib.pyplot as plt

from randomik import *
from db_controller import *


def execute_query(db_file, query, print_time=False):
    '''Выполняет запрос к определённой БД, возвращает количество секунд, за которое запрос был выполнен'''
    conn = sqlite3.connect(db_file, isolation_level=None)

    with conn:
        cursor = conn.cursor()

        start_time = timeit.default_timer()
        cursor.execute(query)
        end_time = timeit.default_timer()
        if print_time:
            print("Время выполнения запроса:", end_time - start_time, "секунд")


def generate_data_dependency(table, row_count):
    '''Функция для построения графика зависимости времени генерации данных в зависимости от их количества'''
    data = []
    time_list = []
    num_rows_list = []
    for i in range(row_count):
        start_time = timeit.default_timer()
        for _ in range(i):
            if table == 'fertilizers':
                data.append(new_random_fertilizer())
            elif table == 'crops':
                data.append(new_random_crop())
        end_time = timeit.default_timer()
        num_rows_list.append(i)
        time_list.append(end_time - start_time)

    plt.plot(num_rows_list, time_list, marker='o')
    plt.title('Время генерации данных в зависимости от их количества')
    plt.xlabel('Количество сгенерированных данных')
    plt.ylabel('Время генерации (сек)')
    plt.grid(True)
    plt.show()


def execute_dependency(db_name, query, row_count):
    '''Функция для построения графика зависимости времени выполнения запросов в зависимости от количества строк в таблице'''
    query_times = []
    num_rows_list = []
    for i in range(1, row_count, 500):
        clear_table(db_name, 'fertilizers')
        clear_table(db_name, 'crops')
        fertilizers = [(j, ) + new_random_fertilizer() for j in range(i)]
        insert_to_db(db_name, 'fertilizers', fertilizers)
        crops = [(j, ) + new_random_crop() for j in range(i)]
        insert_to_db(db_name, 'crops', crops)

        start_time = timeit.default_timer()
        execute_query(db_name, query)
        end_time = timeit.default_timer()

        num_rows_list.append(i)
        query_times.append(end_time - start_time)

    plt.plot(num_rows_list, query_times, marker='o')
    plt.title('Время выполнения запросов в зависимости от количества строк в таблице')
    plt.xlabel('Количество строк в таблице')
    plt.ylabel('Время выполнения запроса (сек)')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    db_name = 'garden.db'
    table = 'fertilizers'
    clear_table(db_name, table)

    # generate_data_dependency(table, 5000)

    query = 'SELECT * FROM fertilizers'
    execute_dependency(db_name, query, 10000)