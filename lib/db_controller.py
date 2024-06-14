'''Модуль содержит функции, изменяющие структуру или наполнение БД'''

import mysql.connector
from mysql.connector import Error
from randomik import *


def create_connection(database=None):
    '''Создаёт и возвращает соединение с сервером MySQL или указанной базой данных'''
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='root',
            database=database
        )
        if conn.is_connected():
            print(f"Successfully connected to the MySQL server{' and database ' + database if database else ''}")
            return conn
    except Error as e:
        print(f"Error: '{e}'")
        return None


def create_database(db_name):
    '''Создаёт базу данных с указанным именем'''
    conn = create_connection('garden')

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                print(f"Database '{db_name}' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")
    else:
        print("Failed to create the database connection")


def create_fertilizers_table():
    '''Конструктор таблицы удобрений для garden'''
    conn = create_connection('garden')

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS fertilizers (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                amount INT
                                )''')
                conn.commit()
                print("Table 'fertilizers' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def create_crops_table():
    '''Конструктор таблицы культур для garden'''
    conn = create_connection('garden')

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS crops (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                season VARCHAR(255),
                                watering_frequency INT,
                                ripening_period INT
                                )''')
                conn.commit()
                print("Table 'crops' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def create_employees_table():
    '''Конструктор таблицы сотрудников для garden'''
    conn = create_connection('garden')

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS employees (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                fullname VARCHAR(255),
                                post VARCHAR(255)
                                )''')
                conn.commit()
                print("Table 'employees' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def create_gardens_table():
    '''Конструктор таблицы садов для garden'''
    conn = create_connection('garden')

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS gardens (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255)
                                )''')
                conn.commit()
                print("Table 'gardens' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def create_actions_table():
    '''Конструктор таблицы действий для garden'''
    conn = create_connection('garden')

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute('''CREATE TABLE IF NOT EXISTS actions (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255)
                                )''')
                conn.commit()
                print("Table 'actions' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def create_garden_db():
    '''Создаёт базу данных garden с таблицами: удобрения, культуры, сотрудники, сады, действия'''
    conn = create_connection()

    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("CREATE DATABASE IF NOT EXISTS garden")
                print("Database 'garden' created successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")

    create_fertilizers_table()
    create_crops_table()
    create_employees_table()
    create_gardens_table()
    create_actions_table()


def clear_tables():
    host = 'localhost'
    user = 'admin'
    password = 'root'
    database = 'garden'

    tables = ['fertilizers', 'crops', 'employees', 'gardens', 'actions']  # список всех таблиц в вашей базе данных

    conn = create_connection('garden')
    if conn:
        cursor = conn.cursor()
        for table in tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"Table {table} cleared successfully.")
            except mysql.connector.Error as e:
                print(f"Error clearing table {table}: {e}")

        conn.commit()
        cursor.close()
        conn.close()
        print("Tables cleared.")
    else:
        print("Failed to connect to MySQL server.")


def copy_tables(source_db, target_db):
    '''Копирует схемы таблиц из source_db в target_db'''
    source_conn = create_connection(source_db)
    target_conn = create_connection(target_db)

    if source_conn and target_conn:
        try:
            with source_conn.cursor() as source_cur, target_conn.cursor() as target_cur:
                source_cur.execute("SHOW TABLES")
                tables = source_cur.fetchall()

                for table in tables:
                    table_name = table[0]
                    source_cur.execute(f"SHOW CREATE TABLE {table_name}")
                    create_table_query = source_cur.fetchone()[1]

                    target_cur.execute(create_table_query)

                target_conn.commit()
                print(f"Tables copied from '{source_db}' to '{target_db}' successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            source_conn.close()
            target_conn.close()
            print("Connections closed\n")


def copy_data(source_db, target_db):
    '''Копирует данные из таблиц source_db в соответствующие таблицы target_db'''
    source_conn = create_connection(source_db)
    target_conn = create_connection(target_db)

    if source_conn and target_conn:
        try:
            with source_conn.cursor() as source_cur, target_conn.cursor() as target_cur:
                source_cur.execute("SHOW TABLES")
                tables = source_cur.fetchall()

                for table in tables:
                    table_name = table[0]
                    source_cur.execute(f"SELECT * FROM {table_name}")
                    rows = source_cur.fetchall()
                    columns = [col[0] for col in source_cur.description]
                    columns_str = ", ".join(columns)
                    placeholders = ", ".join(['%s'] * len(columns))

                    for row in rows:
                        target_cur.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})", row)

                target_conn.commit()
                print(f"Data copied from '{source_db}' to '{target_db}' successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            source_conn.close()
            target_conn.close()
            print("Connections closed\n")


def create_sandbox(source_db, sandbox_db):
    '''Создаёт песочницу для указанной базы данных'''
    create_database(sandbox_db)
    copy_tables(source_db, sandbox_db)


def insert_into_fertilizers(database, fertilizers):
    '''Вставляет данные в таблицу fertilizers'''
    conn = create_connection(database)

    if conn:
        try:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO fertilizers (name, amount) VALUES (%s, %s)"
                cursor.executemany(insert_query, fertilizers)
                conn.commit()
                print(f"{cursor.rowcount} rows inserted into fertilizers")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def insert_into_crops(database, crops):
    '''Вставляет данные в таблицу crops'''
    conn = create_connection(database)

    if conn:
        try:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO crops (name, season, watering_frequency, ripening_period) VALUES (%s, %s, %s, %s)"
                cursor.executemany(insert_query, crops)
                conn.commit()
                print(f"{cursor.rowcount} rows inserted into crops")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def insert_into_employees(database, employees):
    '''Вставляет данные в таблицу employees'''
    conn = create_connection(database)

    if conn:
        try:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO employees (fullname, post) VALUES (%s, %s)"
                cursor.executemany(insert_query, employees)
                conn.commit()
                print(f"{cursor.rowcount} rows inserted into employees")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def insert_into_gardens(database, gardens):
    '''Вставляет данные в таблицу gardens'''
    conn = create_connection(database)

    if conn:
        try:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO gardens (name) VALUES (%s)"
                cursor.executemany(insert_query, [(garden,) for garden in gardens])
                conn.commit()
                print(f"{cursor.rowcount} rows inserted into gardens")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def insert_into_actions(database, actions):
    '''Вставляет данные в таблицу actions'''
    conn = create_connection(database)

    if conn:
        try:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO actions (name) VALUES (%s)"
                cursor.executemany(insert_query, [(action,) for action in actions])
                conn.commit()
                print(f"{cursor.rowcount} rows inserted into actions")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            conn.close()
            print("Connection closed\n")


def show_database_info(database = None):
    host = 'localhost'
    user = 'admin'
    password = 'root'
    if database == None:
        database = 'garden'

    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            cursor = conn.cursor()

            # Получение списка таблиц в базе данных
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                print(f"Table: {table_name}")

                # Получение структуры таблицы
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print("Columns:")
                for column in columns:
                    print(column)

                # Получение данных из таблицы
                cursor.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                print("Data:")
                for row in rows:
                    print(row)
                print("\n")

            cursor.close()
            conn.close()

    except mysql.connector.Error as e:
        print(f"Error: '{e}'")


def clear_table(table):
    '''Очищает таблицу от всех данных'''
    database = 'garden'
    conn = create_connection(database)
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"DELETE FROM {table}")
                conn.commit()
                print(f"Table '{table}' cleared successfully.")
        except Error as e:
            print(f"Error clearing table '{table}': {e}")
        finally:
            conn.close()
    else:
        print(f"Failed to connect to MySQL server.")



def replace_table_data(table, data):
    '''Заменяет все данные в указанной таблице новыми данными'''
    database = 'garden'
    conn = create_connection(database)
    if conn:
        try:
            clear_table(table)
            with conn.cursor() as cursor:
                if table == 'fertilizers':
                    insert_query = "INSERT INTO fertilizers (name, amount) VALUES (%s, %s)"
                elif table == 'crops':
                    insert_query = "INSERT INTO crops (name, season, watering_frequency, ripening_period) VALUES (%s, %s, %s, %s)"
                elif table == 'employees':
                    insert_query = "INSERT INTO employees (fullname, post) VALUES (%s, %s)"
                elif table == 'gardens':
                    insert_query = "INSERT INTO gardens (name) VALUES (%s)"
                elif table == 'actions':
                    insert_query = "INSERT INTO actions (name) VALUES (%s)"

                cursor.executemany(insert_query, data)
                conn.commit()
                print(f"Data replaced in table '{table}' successfully.")
        except Error as e:
            print(f"Error replacing data in table '{table}': {e}")
        finally:
            conn.close()
    else:
        print(f"Failed to connect to MySQL server.")


def backup_table(database, table, backup_filename):
    '''Создаёт бэкап данных из указанной таблицы в файл'''

    conn = mysql.connector.connect(
        host='localhost',
        user='admin',
        password='root',
        database=database
    )

    if conn.is_connected():
        try:
            with open(backup_filename, 'w') as backup_file:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                for row in rows:
                    row_str = ','.join(map(str, row)) + '\n'
                    backup_file.write(row_str)
                print(f"Backup of table '{table}' saved to '{backup_filename}' successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed\n")


def restore_table(database, table, backup_filename):
    '''Восстанавливает данные из указанного файла бэкапа в указанную таблицу'''

    conn = mysql.connector.connect(
        host='localhost',
        user='admin',
        password='root',
        database=database
    )

    if conn.is_connected():
        try:
            with open(backup_filename, 'r') as backup_file:
                cursor = conn.cursor()
                cursor.execute(f"TRUNCATE TABLE {table}")  # Очистка таблицы перед восстановлением данных

                for line in backup_file:
                    values = tuple(line.strip().split(','))
                    insert_query = f"INSERT INTO {table} VALUES ({','.join(['%s'] * len(values))})"
                    cursor.execute(insert_query, values)

                conn.commit()
                print(f"Data restored into table '{table}' from '{backup_filename}' successfully")
        except Error as e:
            print(f"Error: '{e}'")
        finally:
            cursor.close()
            conn.close()
            print("Connection closed\n")


import csv

def show_backup_info(backup_filename):
    '''Отображает содержимое бэкапа из файла backup_filename'''

    try:
        with open(backup_filename, 'r') as backup_file:
            reader = csv.reader(backup_file)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"Backup file '{backup_filename}' not found")
    except Exception as e:
        print(f"Error: '{e}'")



if __name__ == '__main__':
    # Пример использования
    create_garden_db()
    clear_tables()
    database_name = 'garden'

    # Генерация данных
    fertilizers = new_random_fertilizers(10)
    crops = new_random_crops(10)
    employees = new_random_employees(10)
    gardens = new_random_gardens(10)
    actions = new_random_actions(10)

    print(employees[0])

    # Вставка данных
    insert_into_fertilizers(database_name, fertilizers)
    insert_into_crops(database_name, crops)
    insert_into_employees(database_name, employees)
    insert_into_gardens(database_name, gardens)
    insert_into_actions(database_name, actions)

    backup_filename = 'backup.csv'
    table_name = 'employees'