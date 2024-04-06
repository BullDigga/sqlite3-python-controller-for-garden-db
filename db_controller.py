import sqlite3


def create_some_db():
    '''Конструктор баз данных. Для использования нужно менять тело функции'''
    conn = sqlite3.connect('some_db2.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    email TEXT,
                    password TEXT,
                    type TEXT
                    )''')

    conn.close()


def copy_db(old_db_file, new_db_file):
    '''Создаём «песочницу» — копию базы данных с незаполненными таблицами'''
    con = sqlite3.connect(old_db_file)
    bck = sqlite3.connect(new_db_file)
    with bck:
        con.backup(bck)
    bck.close()
    con.close()


def insert_to_db(db_file, table, data_array):
    '''Вставляем данные в таблицу базы данных'''
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    if isinstance(data_array[0], int): # Если подали одну строку
        cursor.execute("""INSERT INTO {table} VALUES {data};""".format(table=table, data=tuple(data_array)))
    else: # Если подали несколько строк
        for data in data_array:
            cursor.execute("""INSERT INTO {table} VALUES {data};""".format(table=table, data=tuple(data)))

    conn.commit()
    cursor.close()


def clear_table(db_file, table):
    '''Удаляем данные из таблицы базы данных'''
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM {table};'''.format(table=table))

    conn.commit()
    cursor.close()


def raplase_table_data(db_file, table, data_array):
    '''Заменяет все данные таблицы на data_array'''
    clear_table(db_file, table)
    insert_to_db(db_file, table, data_array)


if __name__ == '__main__':
    # create_some_db()
    # copy_db('some_db.db', 'new_db.db')
    # data = [2, 'mam', 40, 'mama@gmail.com', 'lalal21', 'admin']
    # insert_to_db('some_db.db', 'users', data)
    clear_table('some_db.db', 'users')
    # raplase_table_data('some_db.db', 'users', data)
    pass