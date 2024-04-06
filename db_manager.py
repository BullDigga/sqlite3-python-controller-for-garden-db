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
    if table == 'fertilizers':
        for i in range(row_count):
            start_time = timeit.default_timer()
            for _ in range(i):
                data.append(new_random_fertilizer())
            end_time = timeit.default_timer()
            num_rows_list.append(i)
            time_list.append(end_time - start_time)
    elif table == 'crops':
        for i in range(row_count):
            start_time = timeit.default_timer()
            for _ in range(i):
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
    if table == 'fertilizers':
        for i in range(row_count):
            start_time = timeit.default_timer()
            execute_query(db_name, query)
            end_time = timeit.default_timer()

            num_rows_list.append(i)
            query_times.append(end_time - start_time)
    elif table == 'crops':
        for i in range(row_count):
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

    # data_list = [
    #     [(i,) + tuple(new_random_fertilizer()) for i in range(1, 101)],
    #     [(i,) + tuple(new_random_fertilizer()) for i in range(101, 301)],
    #     [(i,) + tuple(new_random_fertilizer()) for i in range(301, 1001)],
    #     [(i,) + tuple(new_random_fertilizer()) for i in range(1001, 5001)],
    #     [(i,) + tuple(new_random_fertilizer()) for i in range(5001, 10001)],
    #     [(i,) + tuple(new_random_fertilizer()) for i in range(10001, 20001)],
    # ]
    #
    # insert_and_plot_data(db_name, table, data_list)

    # generate_data_dependency(table, 100)

    query = 'SELECT * FROM fertilizers'
    execute_dependency(db_name, query, 20000)