import mysql.connector
import subprocess
import datetime
import os

from mysql.connector import Error
from lib.randomik import *


class MySQLConnectionManager:
    def __init__(self, database=None):
        self.database = database
        self.conn = None

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='admin',
                password='root',
                database=self.database
            )
            if self.conn.is_connected():
                print(f"Successfully connected to the MySQL server{' and database ' + self.database if self.database else ''}")
                return self.conn
        except Error as e:
            print(f"Error: '{e}'")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connection closed\n")


class MySQLCursorManager:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = None

    def __enter__(self):
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()


def create_connection(database=None):
    '''Создаёт и возвращает соединение с сервером MySQL или указанной базой данных'''
    return MySQLConnectionManager(database)


def create_database(db_name):
    '''Создаёт базу данных с указанным именем'''
    with create_connection() as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                    print(f"Database '{db_name}' created successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_fertilizers_table(db_name='garden'):
    '''Конструктор таблицы удобрений для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS fertilizers (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255),
                                    amount INT
                                    )''')
                    print(f"Table 'fertilizers' in database '{db_name}' created successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_crops_table(db_name='garden'):
    '''Конструктор таблицы культур для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS crops (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255),
                                    season VARCHAR(255),
                                    watering_frequency INT,
                                    ripening_period INT
                                    )''')
                    print(f"Table 'crops' in database '{db_name}' created successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_employees_table(db_name='garden'):
    '''Конструктор таблицы сотрудников для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS employees (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    fullname VARCHAR(255),
                                    post VARCHAR(255)
                                    )''')
                    print(f"Table 'employees' in database '{db_name}' created successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_gardens_table(db_name='garden'):
    '''Конструктор таблицы садов для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS gardens (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255)
                                    )''')
                    print(f"Table 'gardens' in database '{db_name}' created successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_actions_table(db_name='garden'):
    '''Конструктор таблицы действий для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS actions (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255)
                                    )''')
                    print(f"Table 'actions' in database '{db_name}' created successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_beds_table(db_name='garden'):
    '''Конструктор таблицы грядок для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS beds (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    garden_id INT,
                                    crop_id INT,
                                    fertilizer_id INT,
                                    FOREIGN KEY (garden_id) REFERENCES gardens(id),
                                    FOREIGN KEY (crop_id) REFERENCES crops(id),
                                    FOREIGN KEY (fertilizer_id) REFERENCES fertilizers(id)
                                    )''')
                    print(f"Table 'beds' in database '{db_name}' created successfully")
            except mysql.connector.Error as e:
                print(f"Error creating table 'beds' in database '{db_name}': {e}")


def create_garden_employee_table(db_name='garden'):
    '''Конструктор таблицы связи Сады_Сотрудники для garden'''
    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cur:
                    cur.execute('''CREATE TABLE IF NOT EXISTS garden_employees (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    garden_id INT,
                                    employee_id INT,
                                    FOREIGN KEY (garden_id) REFERENCES gardens(id),
                                    FOREIGN KEY (employee_id) REFERENCES employees(id)
                                    )''')
                    print(f"Table 'garden_employee' in database '{db_name}' created successfully")
            except mysql.connector.Error as e:
                print(f"Error creating table 'garden_employee' in database '{db_name}': {e}")

def create_garden_db(dbname='garden'):
    '''Создаёт базу данных garden с таблицами: удобрения, культуры, сотрудники, сады, действия, грядки и связи Сады_Сотрудники'''
    create_database(dbname)
    create_fertilizers_table(dbname)
    create_crops_table(dbname)
    create_employees_table(dbname)
    create_gardens_table(dbname)
    create_actions_table(dbname)
    create_beds_table(dbname)
    create_garden_employee_table(dbname)


def clear_tables():
    '''Очищает все данные из таблиц в БД'''
    tables = ['beds', 'garden_employees', 'fertilizers', 'crops', 'employees', 'gardens', 'actions']

    with create_connection('garden') as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    for table in tables:
                        cursor.execute(f"DELETE FROM {table}")
                        print(f"Table {table} cleared successfully.")
            except mysql.connector.Error as e:
                print(f"Error clearing table {table}: {e}")

def copy_tables(source_db, target_db):
    '''Копирует схемы таблиц из source_db в target_db'''
    with create_connection(source_db) as source_conn, create_connection(target_db) as target_conn:
        if source_conn and target_conn:
            try:
                with MySQLCursorManager(source_conn) as source_cur, MySQLCursorManager(target_conn) as target_cur:
                    source_cur.execute("SHOW TABLES")
                    tables = source_cur.fetchall()

                    for table in tables:
                        table_name = table[0]
                        source_cur.execute(f"SHOW CREATE TABLE {table_name}")
                        create_table_query = source_cur.fetchone()[1]

                        target_cur.execute(create_table_query)

                    print(f"Tables copied from '{source_db}' to '{target_db}' successfully")
            except Error as e:
                print(f"Error: '{e}'")


def copy_data(source_db, target_db):
    '''Копирует данные из таблиц source_db в соответствующие таблицы target_db'''
    with create_connection(source_db) as source_conn, create_connection(target_db) as target_conn:
        if source_conn and target_conn:
            try:
                with MySQLCursorManager(source_conn) as source_cur, MySQLCursorManager(target_conn) as target_cur:
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

                    print(f"Data copied from '{source_db}' to '{target_db}' successfully")
            except Error as e:
                print(f"Error: '{e}'")


def create_sandbox(source_db, sandbox_db):
    '''Создаёт песочницу для указанной базы данных'''
    create_database(sandbox_db)
    copy_tables(source_db, sandbox_db)


def insert_into_fertilizers(database, fertilizers):
    '''Вставляет данные в таблицу fertilizers'''
    with create_connection(database) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    insert_query = "INSERT INTO fertilizers (name, amount) VALUES (%s, %s)"
                    cursor.executemany(insert_query, fertilizers)
                    print(f"{cursor.rowcount} rows inserted into fertilizers")
            except Error as e:
                print(f"Error: '{e}'")


def insert_into_crops(database, crops):
    '''Вставляет данные в таблицу crops'''
    with create_connection(database) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    insert_query = "INSERT INTO crops (name, season, watering_frequency, ripening_period) VALUES (%s, %s, %s, %s)"
                    cursor.executemany(insert_query, crops)
                    print(f"{cursor.rowcount} rows inserted into crops")
            except Error as e:
                print(f"Error: '{e}'")


def insert_into_employees(database, employees):
    '''Вставляет данные в таблицу employees'''
    with create_connection(database) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    insert_query = "INSERT INTO employees (fullname, post) VALUES (%s, %s)"
                    cursor.executemany(insert_query, employees)
                    print(f"{cursor.rowcount} rows inserted into employees")
            except Error as e:
                print(f"Error: '{e}'")


def insert_into_gardens(database, gardens):
    '''Вставляет данные в таблицу gardens'''
    with create_connection(database) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    insert_query = "INSERT INTO gardens (name) VALUES (%s)"
                    cursor.executemany(insert_query, gardens)
                    print(f"{cursor.rowcount} rows inserted into gardens")
            except Error as e:
                print(f"Error: '{e}'")


def insert_into_actions(database, actions):
    '''Вставляет данные в таблицу actions'''
    with create_connection(database) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    insert_query = "INSERT INTO actions (name) VALUES (%s)"
                    cursor.executemany(insert_query, actions)
                    print(f"{cursor.rowcount} rows inserted into actions")
            except Error as e:
                print(f"Error: '{e}'")


def populate_fertilizers_table(database, n):
    '''Заполняет таблицу fertilizers случайными данными'''
    fertilizers = [new_random_fertilizer() for _ in range(n)]
    insert_into_fertilizers(database, fertilizers)


def populate_crops_table(database, n):
    '''Заполняет таблицу crops случайными данными'''
    crops = [new_random_crop() for _ in range(n)]
    insert_into_crops(database, crops)


def populate_employees_table(database, n):
    '''Заполняет таблицу employees случайными данными'''
    employees = [new_random_employee() for _ in range(n)]
    insert_into_employees(database, employees)


def populate_gardens_table(database, n):
    '''Заполняет таблицу gardens случайными данными'''
    gardens = [(garden,) for garden in new_random_gardens(n)]
    insert_into_gardens(database, gardens)


def populate_actions_table(database, n):
    '''Заполняет таблицу actions случайными данными'''
    actions = [(action,) for action in new_random_actions(n)]
    insert_into_actions(database, actions)


def populate_garden_db(database, n):
    '''Заполняет таблицы в базе данных garden случайными данными'''
    populate_fertilizers_table(database, n)
    populate_crops_table(database, n)
    populate_employees_table(database, n)
    populate_gardens_table(database, n)
    populate_actions_table(database, n)


def show_database_info(database='garden'):
    host = 'localhost'
    user = 'admin'
    password = 'root'

    try:
        # Подключение к базе данных
        with mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        ) as conn:
            if conn.is_connected():
                with conn.cursor() as cursor:
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
                            print(f"{column[0]} ({column[1]})")

                        # Получение данных из таблицы
                        cursor.execute(f"SELECT * FROM {table_name}")
                        rows = cursor.fetchall()
                        print("Data:")
                        for row in rows:
                            print(row)
                        print("\n")

    except mysql.connector.Error as e:
        print(f"Error: '{e}'")


def execute_query(query):
    '''Выполняет переданный SQL-запрос и возвращает результат'''
    with create_connection('garden') as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    return rows
            except Error as e:
                print(f"Error: '{e}'")
                return None


def drop_tables(db_name='garden'):

    drop_table_query = "DROP TABLE IF EXISTS {}"

    with create_connection(db_name) as conn:
        if conn:
            try:
                with MySQLCursorManager(conn) as cursor:
                    # Disable foreign key checks temporarily
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

                    # Drop tables in the correct order to avoid foreign key constraints errors
                    tables_to_drop = ['beds', 'fertilizers', 'crops', 'employees', 'gardens', 'actions', 'garden_employees']

                    for table in tables_to_drop:
                        try:
                            cursor.execute(drop_table_query.format(table))
                            print(f"Table '{table}' dropped successfully")
                        except mysql.connector.Error as e:
                            print(f"Error dropping table '{table}': {e}")

                    # Enable foreign key checks back
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            except mysql.connector.Error as e:
                print(f"Error: '{e}'")


def create_backup(host='localhost', user='admin', password='root', database='garden', backup_path='./backups'):
    """Создает бэкап базы данных MySQL."""
    try:
        # Создаем путь для сохранения бэкапа
        os.makedirs(backup_path, exist_ok=True)

        # Генерируем имя файла бэкапа на основе текущей даты и времени
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_file = f'{database}_backup_{timestamp}.sql'
        backup_file_path = os.path.join(backup_path, backup_file)

        # Устанавливаем соединение с базой данных
        with mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',  # Установим кодировку UTF-8
                collation='utf8mb4_unicode_ci'
        ) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    # Открываем файл для записи бэкапа
                    with open(backup_file_path, 'w', encoding='utf-8') as f:
                        for table in ['fertilizers', 'crops', 'employees', 'gardens', 'actions', 'beds', 'garden_employees']:
                            # Получаем данные из таблицы и записываем их в файл
                            cursor.execute(f"SELECT * FROM {table}")
                            rows = cursor.fetchall()
                            f.write(f"-- Table: {table}\n")
                            for row in rows:
                                f.write(str(row) + '\n')
                            f.write('\n')

                    print(f'Backup created successfully: {backup_file_path}')

    except Error as e:
        print(f'Error creating backup: {e}')


def restore_backup(backup_file_path, host='localhost', user='admin', password='root', target_database='garden_backup_test'):
    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=target_database  # Используем целевую базу данных для восстановления
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Чтение содержимого бэкапа
            with open(backup_file_path, 'rb') as backup_file:
                content = backup_file.read().decode('utf-8', errors='ignore')

                # Разделение содержимого на отдельные блоки таблиц
                table_blocks = content.split('-- Table: ')

                for block in table_blocks[1:]:  # Начинаем с 1, чтобы пропустить первый пустой элемент
                    lines = block.strip().splitlines()

                    table_name = lines[0].strip()  # Название таблицы
                    values = [line.strip('()') for line in lines[1:] if line.startswith('(')]

                    # Вставка данных в таблицу
                    if values:
                        insert_query = f"INSERT INTO {table_name} VALUES ({'), ('.join(values)}) ON DUPLICATE KEY UPDATE id=id;"
                        try:
                            cursor.execute(insert_query)
                        except mysql.connector.Error as e:
                            print(f"Error executing SQL command: {e}")

            # Фиксация изменений и закрытие соединения
            connection.commit()
            cursor.close()
            connection.close()

            print(f'Backup restored successfully from: {backup_file_path} to database: {target_database}')

    except mysql.connector.Error as e:
        print(f'Error restoring backup: {e}')


if __name__ == '__main__':
    # drop_tables()
    # create_garden_db()
    # clear_tables()
    # show_database_info()

    # create_backup()
    test_db_name = 'garden_backup_test'
    drop_tables(test_db_name)
    create_garden_db(test_db_name)
    restore_backup(backup_file_path='backups/garden_backup_2024-06-18_16-43-49.sql', target_database=test_db_name)
    show_database_info(test_db_name)