import timeit
import matplotlib.pyplot as plt

from randomik import *
from db_controller import *


def execute_query(db_file, query):
    '''Выполняет запрос к определённой БД, возвращает количество секунд, за которое запрос был выполнен'''
    conn = sqlite3.connect(db_file, isolation_level=None)

    with conn:
        cursor = conn.cursor()

        start_time = timeit.default_timer()
        cursor.execute(query)
        end_time = timeit.default_timer()
        print("Время выполнения запроса:", end_time - start_time, "секунд")


if __name__ == '__main__':
    pass