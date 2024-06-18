import random

from mysql.connector import Error
from lib.db_controller import create_connection


def generate_random_string(length):
    '''
    Генерирует случайную строку заданной длины из строчных букв русского алфавита.

    Параметры:
    -----------
    length : int
        Длина строки.

    Возвращает:
    --------
    генератор str
        Генератор случайных строк заданной длины.
    '''
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    while True:
        rand_string = ''.join(random.choice(alphabet) for i in range(length))
        yield rand_string


def generator_random_fertilizer(num_instances):
    '''
    Генерирует случайные данные для удобрений.

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров удобрений для генерации.

    Возвращает:
    --------
    генератор tuple
        Кортежи (название удобрения, количество) случайных удобрений.
    '''
    # Генератор случайных названий удобрений
    new_name_gen = generate_random_string(random.randint(4, 10))

    for _ in range(num_instances):
        new_name = next(new_name_gen)
        new_count = random.randint(0, 100)
        yield new_name, new_count


def generator_random_crop(num_instances):
    '''
    Генерирует случайные данные для культур.

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров культур для генерации.

    Возвращает:
    --------
    генератор tuple
        Кортежи (название культуры, сезон, частота полива, срок созревания) случайных культур.
    '''
    seasons = ['весна', 'лето', 'осень', 'зима']
    new_name_gen = generate_random_string(random.randint(4, 10))

    for _ in range(num_instances):
        new_name = next(new_name_gen)
        new_season = random.choice(seasons)
        new_watering_frequency = random.randint(1, 10)
        new_ripening_period = random.randint(10, 60)
        yield new_name, new_season, new_watering_frequency, new_ripening_period


def generator_random_employee(num_instances):
    '''
    Генерирует случайные данные для сотрудников.

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров сотрудников для генерации.

    Возвращает:
    --------
    генератор tuple
        Кортежи (ФИО, должность) случайных сотрудников.
    '''
    new_name_gen = generate_random_string(random.randint(4, 10))
    new_surname_gen = generate_random_string(random.randint(4, 10))
    new_patronymic_gen = generate_random_string(random.randint(4, 10))

    for _ in range(num_instances):
        new_name = next(new_name_gen)
        new_surname = next(new_surname_gen)
        new_patronymic = next(new_patronymic_gen)
        new_fullname = f"{new_name} {new_surname} {new_patronymic}"
        new_post = next(generate_random_string(random.randint(4, 10)))
        yield new_fullname, new_post


def generator_random_garden(num_instances):
    '''
    Генерирует случайные данные для садов.

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров садов для генерации.

    Возвращает:
    --------
    генератор str
        Строки с названиями случайных садов.
    '''
    new_name_gen = generate_random_string(random.randint(4, 10))

    for _ in range(num_instances):
        new_name = f"Сад {next(new_name_gen)}"
        yield new_name


def generator_random_action(num_instances):
    '''
    Генерирует случайные данные для действий.

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров действий для генерации.

    Возвращает:
    --------
    генератор str
        Строки с названиями случайных действий.
    '''
    new_name_gen = generate_random_string(random.randint(4, 10))

    for _ in range(num_instances):
        new_name = next(new_name_gen)
        yield new_name


def generator_random_bed(num_instances):
    '''
    Генерирует случайные данные для грядок.

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров грядок для генерации.

    Возвращает:
    --------
    генератор tuple
        Кортежи с идентификаторами случайного сада, культуры и удобрения.
    '''
    garden_ids, crop_ids, fertilizer_ids = [], [], []

    # Получаем ID созданных садов, культур и удобрений из базы данных
    with create_connection('garden') as connection:
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM gardens")
                    garden_ids = [row[0] for row in cursor.fetchall()]

                    cursor.execute("SELECT id FROM crops")
                    crop_ids = [row[0] for row in cursor.fetchall()]

                    cursor.execute("SELECT id FROM fertilizers")
                    fertilizer_ids = [row[0] for row in cursor.fetchall()]
            except Error as e:
                print(f"The error '{e}' occurred")

    for _ in range(num_instances):
        garden_id = random.choice(garden_ids)
        crop_id = random.choice(crop_ids)
        fertilizer_id = random.choice(fertilizer_ids)
        yield garden_id, crop_id, fertilizer_id


def generator_random_garden_employee(num_instances):
    '''
    Генерирует случайные данные для отношений "Сад-Сотрудник".

    Параметры:
    -----------
    num_instances : int
        Количество экземпляров отношений для генерации.

    Возвращает:
    --------
    генератор tuple
        Кортежи с идентификаторами случайного сада и случайного сотрудника.
    '''
    with create_connection('garden') as connection:
        if connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM gardens")
                    garden_ids = [row[0] for row in cursor.fetchall()]

                    cursor.execute("SELECT id FROM employees")
                    employee_ids = [row[0] for row in cursor.fetchall()]

                    for _ in range(num_instances):
                        garden_id = random.choice(garden_ids)
                        employee_id = random.choice(employee_ids)
                        yield garden_id, employee_id

            except Error as e:
                print(f"The error '{e}' occurred")
