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


if __name__ == '__main__':
    pass