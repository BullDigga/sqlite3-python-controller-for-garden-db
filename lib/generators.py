import random

def generate_random_string(length):
    '''Возвращает случайное слово длины length, состоящее из строчных букв русского алфавита'''
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    while True:
        rand_string = ''.join(random.choice(alphabet) for i in range(length))
        yield rand_string

def generator_random_fertilizer(num_instances):
    '''Возвращает случайные удобрения (название и количество)'''
    new_name_gen = generate_random_string(random.randint(4, 10))
    for _ in range(num_instances):
        new_name = next(new_name_gen)
        new_count = random.randint(0, 100)
        yield new_name, new_count

def generator_random_crop(num_instances):
    '''Возвращает случайные культуры (название, сезон, частота полива, срок созревания)'''
    seasons = ['весна', 'лето', 'осень', 'зима']
    new_name_gen = generate_random_string(random.randint(4, 10))
    for _ in range(num_instances):
        new_name = next(new_name_gen)
        new_season = random.choice(seasons)
        new_watering_frequency = random.randint(1, 10)
        new_ripening_period = random.randint(10, 60)
        yield new_name, new_season, new_watering_frequency, new_ripening_period

def generator_random_employee(num_instances):
    '''Возвращает случайных сотрудников (ФИО, должность)'''
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
    '''Возвращает случайные сады (название сада)'''
    new_name_gen = generate_random_string(random.randint(4, 10))
    for _ in range(num_instances):
        new_name = f"Сад {next(new_name_gen)}"
        yield new_name

def generator_random_action(num_instances):
    '''Возвращает случайные действия (название действия)'''
    new_name_gen = generate_random_string(random.randint(4, 10))
    for _ in range(num_instances):
        new_name = next(new_name_gen)
        yield new_name