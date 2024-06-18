"""
Модуль: randomik

Этот модуль предоставляет функции для генерации случайных данных, которые могут быть использованы для заполнения таблиц в базе данных.
"""

import random

def generate_random_string(length):
    """
    Генерирует случайную строку из строчных букв русского алфавита заданной длины.

    Параметры:
    -----------
    length : int
        Длина генерируемой строки.

    Возвращает:
    --------
    str
        Случайная строка из строчных букв русского алфавита.
    """
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rand_string = ''.join(random.choice(alphabet) for _ in range(length))
    return rand_string


def new_random_fertilizer():
    """
    Генерирует случайное удобрение с названием и количеством.

    Возвращает:
    --------
    tuple
        Кортеж с названием и количеством случайного удобрения.
    """
    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    new_count = random.randint(0, 100)

    return new_name, new_count


def new_random_fertilizers(count):
    """
    Генерирует список случайных удобрений.

    Параметры:
    -----------
    count : int
        Количество случайных удобрений для генерации.

    Возвращает:
    --------
    list
        Список кортежей с названием и количеством случайных удобрений.
    """
    fertilizers_list = [new_random_fertilizer() for _ in range(count)]
    return fertilizers_list


def new_random_crop():
    """
    Генерирует случайную культуру с названием, сезоном, частотой полива и сроком созревания.

    Возвращает:
    --------
    tuple
        Кортеж с названием, сезоном, частотой полива и сроком созревания случайной культуры.
    """
    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    seasons = ['весна', 'лето', 'осень', 'зима']
    new_season = random.choice(seasons)

    new_watering_frequency = random.randint(1, 10)

    new_ripening_period = random.randint(10, 60)

    return new_name, new_season, new_watering_frequency, new_ripening_period


def new_random_crops(count):
    """
    Генерирует список случайных культур.

    Параметры:
    -----------
    count : int
        Количество случайных культур для генерации.

    Возвращает:
    --------
    list
        Список кортежей с названием, сезоном, частотой полива и сроком созревания случайных культур.
    """
    crops_list = [new_random_crop() for _ in range(count)]
    return crops_list


def new_random_employee():
    """
    Генерирует случайного сотрудника с ФИО и должностью.

    Возвращает:
    --------
    tuple
        Кортеж с ФИО и должностью случайного сотрудника.
    """
    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    new_surname_len = random.randint(4, 10)
    new_surname = generate_random_string(new_surname_len)

    new_patronymic_len = random.randint(4, 10)
    new_patronymic = generate_random_string(new_patronymic_len)

    new_fullname = new_name + ' ' + new_surname + ' ' + new_patronymic

    new_post_len = random.randint(4, 10)
    new_post= generate_random_string(new_post_len)

    return new_fullname, new_post


def new_random_employees(count):
    """
    Генерирует список случайных сотрудников.

    Параметры:
    -----------
    count : int
        Количество случайных сотрудников для генерации.

    Возвращает:
    --------
    list
        Список кортежей с ФИО и должностью случайных сотрудников.
    """
    employees_list = [new_random_employee() for _ in range(count)]
    return employees_list


def new_random_garden():
    """
    Генерирует случайное название сада.

    Возвращает:
    --------
    str
        Случайное название сада.
    """
    new_name_len = random.randint(4, 10)
    new_name = 'Сад ' + generate_random_string(new_name_len)

    return new_name


def new_random_gardens(count):
    """
    Генерирует список случайных названий садов.

    Параметры:
    -----------
    count : int
        Количество случайных названий садов для генерации.

    Возвращает:
    --------
    list
        Список строк со случайными названиями садов.
    """
    gardens_list = [new_random_garden() for _ in range(count)]
    return gardens_list


def new_random_action():
    """
    Генерирует случайное название действия.

    Возвращает:
    --------
    str
        Случайное название действия.
    """
    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    return new_name


def new_random_actions(count):
    """
    Генерирует список случайных названий действий.

    Параметры:
    -----------
    count : int
        Количество случайных названий действий для генерации.

    Возвращает:
    --------
    list
        Список строк со случайными названиями действий.
    """
    actions_list = [new_random_action() for _ in range(count)]
    return actions_list


if __name__ == '__main__':
    pass  # Заглушка, чтобы модуль не выполнялся при импорте
