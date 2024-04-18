'''Модуль содержит функции, изменяющие структуру или наполнение БД'''

import sqlite3

from randomik import *


def create_some_db():
    '''Конструктор баз данных. Для использования нужно менять тело функции'''
    conn = sqlite3.connect('some_db.db', isolation_level=None)

    with conn:
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        email TEXT,
                        password TEXT,
                        type TEXT
                        )''')


def create_fertilizers_table():
    '''Конструктор таблицы удобрений для garden.db'''
    conn = sqlite3.connect('garden.db', isolation_level=None)

    with conn:
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS fertilizers (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        amount INTEGER
                        )''')


def create_crops_table():
    '''Конструктор таблицы культур для garden.db'''
    conn = sqlite3.connect('garden.db', isolation_level=None)

    with conn:
        cur = conn.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS crops (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        season TEXT,
                        watering_frequency INTEGER,
                        ripening_period INTEGER
                        )''')


def create_garden_db():
    '''Создаёт базу данных garden.db с таблицами: удобрения, культуры'''
    create_fertilizers_table()
    create_crops_table()

def copy_db(old_db_file, new_db_file):
    '''Создаём «песочницу» — копию базы данных с незаполненными таблицами'''
    con = sqlite3.connect(old_db_file, isolation_level=None)
    bck = sqlite3.connect(new_db_file, isolation_level=None)

    with bck:
        con.backup(bck)


def insert_to_db(db_file, table, data_list):
    '''Вставляем данные в таблицу базы данных'''
    conn = sqlite3.connect(db_file, isolation_level=None)

    with conn:
        cursor = conn.cursor()

        if isinstance(data_list[0], int): # Если подали одну строку
            cursor.execute("""INSERT INTO {table} VALUES {data};""".format(table=table, data=tuple(data_list)))
        else: # Если подали несколько строк
            for data in data_list:
                cursor.execute("""INSERT INTO {table} VALUES {data};""".format(table=table, data=tuple(data)))


def clear_table(db_file, table):
    '''Удаляем данные из таблицы базы данных'''
    conn = sqlite3.connect(db_file, isolation_level=None)

    with conn:
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM {table};'''.format(table=table))

def clear_tables():
    '''Очищает таблицы «fertilizer» и «crops» в базе данных «garden.db».
    Также обнуляет статические переменные ID в функциях «new_random_fertilizer» и «new_random_crop»'''
    clear_table('garden.db', 'fertilizers')
    clear_table('garden.db', 'crops')

    new_random_fertilizer.id_count = 0
    new_random_crop.id_count = 0


def raplase_table_data(db_file, table, data_list):
    '''Заменяет все данные таблицы на data_list'''
    clear_table(db_file, table)
    insert_to_db(db_file, table, data_list)


if __name__ == '__main__':
    create_garden_db()
    data = new_random_crops(20)
    insert_to_db('garden.db', 'crops', data)
    clear_tables()
    data = new_random_crops(30)
    insert_to_db('garden.db', 'crops', data)
    pass