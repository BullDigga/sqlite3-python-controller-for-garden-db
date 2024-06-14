'''Данный модуль содержит функции, генерирующие новые строки к таблицам для БД'''

import random


def generate_random_string(length):
    '''Возвращает случайное слово длины lenght, состоящее из строчных букв русского алфавита'''
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rand_string = ''.join(random.choice(alphabet) for i in range(length))
    return rand_string


def new_random_fertilizer():
    '''Возвращает случайное удобрение (ID, название и количество)'''
    if not hasattr(new_random_fertilizer, "id_count"):
        new_random_fertilizer.id_count = 0
    new_random_fertilizer.id_count += 1

    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    new_count = random.randint(0, 100)

    return new_random_fertilizer.id_count, new_name, new_count


def new_random_fertilizers(count):
    '''Возвращает список из count удобрений'''
    fertilizers_list = [new_random_fertilizer() for _ in range(count)]
    return fertilizers_list


def new_random_crop():
    '''Возвращает случайную культуру (ID, название, сезон, частота полива, срок созревания)'''
    if not hasattr(new_random_crop, "id_count"):
        new_random_crop.id_count = 0
    new_random_crop.id_count += 1

    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    seasons = ['весна', 'лето', 'осень', 'зима']
    new_season = random.choice(seasons)

    new_watering_frequency = random.randint(1, 10)

    new_ripening_period = random.randint(10, 60)

    return new_random_crop.id_count, new_name, new_season, new_watering_frequency, new_ripening_period


def new_random_crops(count):
    '''Возвращает список из count культур'''
    crops_list = [new_random_crop() for _ in range(count)]
    return crops_list


def new_random_employee():
    '''Возвращает случайного сотрудника (ID, ФИО, должность)'''
    if not hasattr(new_random_employee, "id_count"):
        new_random_employee.id_count = 0
    new_random_employee.id_count += 1

    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    new_surname_len = random.randint(4, 10)
    new_surname = generate_random_string(new_surname_len)

    new_patronymic_len = random.randint(4, 10)
    new_patronymic = generate_random_string(new_patronymic_len)

    new_fullname = new_name + ' ' + new_surname + ' ' + new_patronymic

    new_post_len = random.randint(4, 10)
    new_post= generate_random_string(new_post_len)

    return new_random_employee.id_count, new_fullname, new_post


def new_random_employees(count):
    '''Возвращает список из count сотрудников'''
    employees_list = [new_random_employee() for _ in range(count)]
    return employees_list


def new_random_garden():
    '''Возвращает случайный сад (ID, название сада)'''
    if not hasattr(new_random_garden, "id_count"):
        new_random_garden.id_count = 0
    new_random_garden.id_count += 1

    new_name_len = random.randint(4, 10)
    new_name = 'Сад ' + generate_random_string(new_name_len)

    return new_random_garden.id_count, new_name


def new_random_gardens(count):
    '''Возвращает список из count садов'''
    gardens_list = [new_random_garden() for _ in range(count)]
    return gardens_list


def new_random_action():
    '''Возвращает случайное действие (ID, название действия)'''
    if not hasattr(new_random_action, "id_count"):
        new_random_action.id_count = 0
    new_random_action.id_count += 1

    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    return new_random_action.id_count, new_name


def new_random_actions(count):
    '''Возвращает список из count действий'''
    actions_list = [new_random_action() for _ in range(count)]
    return actions_list


if __name__ == '__main__':
    pass