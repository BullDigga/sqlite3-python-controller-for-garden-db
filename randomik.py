'''Данный модуль содержит функции, генерирующие новые строки к таблицам для БД'''

import random


def generate_random_string(length):
    '''Возвращает случайное слово длины lenght, состоящее из строчных букв русского алфавита'''
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    rand_string = ''.join(random.choice(alphabet) for i in range(length))
    return rand_string


def new_random_fertilizer():
    '''Возвращает случайное удобрение (название и количество)'''
    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    new_count = random.randint(0, 100)

    return new_name, new_count


def new_random_crop():
    '''Возвращает случайную культуру (название, сезон, частота полива, срок созревания)'''
    new_name_len = random.randint(4, 10)
    new_name = generate_random_string(new_name_len)

    seasons = ['весна', 'лето', 'осень', 'зима']
    new_season = random.choice(seasons)

    new_watering_frequency = random.randint(1, 10)

    new_ripening_period = random.randint(10, 60)

    return new_name, new_season, new_watering_frequency, new_ripening_period


if __name__ == '__main__':
    pass