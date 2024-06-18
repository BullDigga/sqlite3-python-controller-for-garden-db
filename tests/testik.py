import unittest
from unittest.mock import patch

from lib.randomik import *
from lib.generators import *
from lib.db_controller import create_connection

class TestRandomFunctions(unittest.TestCase):

    def test_new_random_fertilizer(self):
        # Тестирование генерации случайного удобрения
        new_name, new_count = new_random_fertilizer()
        self.assertIsInstance(new_name, str)  # Убеждаемся, что имя удобрения - строка
        self.assertTrue(4 <= len(new_name) <= 10)  # Проверяем длину имени удобрения
        self.assertTrue(0 <= new_count <= 100)  # Проверяем, что количество удобрения находится в допустимых пределах

    def test_new_random_fertilizers(self):
        # Тестирование генерации списка случайных удобрений
        count = 5
        fertilizers_list = new_random_fertilizers(count)
        self.assertEqual(len(fertilizers_list), count)  # Проверяем количество сгенерированных удобрений
        for name, count in fertilizers_list:
            self.assertIsInstance(name, str)  # Убеждаемся, что имя удобрения - строка
            self.assertTrue(4 <= len(name) <= 10)  # Проверяем длину имени удобрения
            self.assertTrue(0 <= count <= 100)  # Проверяем, что количество удобрения находится в допустимых пределах

    def test_new_random_crop(self):
        # Тестирование генерации случайной культуры
        new_name, new_season, new_watering_frequency, new_ripening_period = new_random_crop()
        self.assertIsInstance(new_name, str)  # Убеждаемся, что имя культуры - строка
        self.assertTrue(4 <= len(new_name) <= 10)  # Проверяем длину имени культуры
        seasons = ['весна', 'лето', 'осень', 'зима']
        self.assertIn(new_season, seasons)  # Убеждаемся, что сезон в списке допустимых значений
        self.assertTrue(1 <= new_watering_frequency <= 10)  # Проверяем, что частота полива находится в допустимых пределах
        self.assertTrue(10 <= new_ripening_period <= 60)  # Проверяем, что срок созревания находится в допустимых пределах

    def test_new_random_crops(self):
        # Тестирование генерации списка случайных культур
        count = 5
        crops_list = new_random_crops(count)
        self.assertEqual(len(crops_list), count)  # Проверяем количество сгенерированных культур
        for name, season, watering_frequency, ripening_period in crops_list:
            self.assertIsInstance(name, str)  # Убеждаемся, что имя культуры - строка
            self.assertTrue(4 <= len(name) <= 10)  # Проверяем длину имени культуры
            seasons = ['весна', 'лето', 'осень', 'зима']
            self.assertIn(season, seasons)  # Убеждаемся, что сезон в списке допустимых значений
            self.assertTrue(1 <= watering_frequency <= 10)  # Проверяем, что частота полива находится в допустимых пределах
            self.assertTrue(10 <= ripening_period <= 60)  # Проверяем, что срок созревания находится в допустимых пределах

    def test_new_random_employee(self):
        # Тестирование генерации случайного сотрудника
        new_fullname, new_post = new_random_employee()
        self.assertIsInstance(new_fullname, str)  # Убеждаемся, что ФИО - строка
        parts = new_fullname.split()
        self.assertEqual(len(parts), 3)  # Убеждаемся, что ФИО содержит три части (имя, фамилия, отчество)
        self.assertTrue(4 <= len(parts[0]) <= 10)  # Проверяем длину имени
        self.assertTrue(4 <= len(parts[1]) <= 10)  # Проверяем длину фамилии
        self.assertTrue(4 <= len(parts[2]) <= 10)  # Проверяем длину отчества
        self.assertIsInstance(new_post, str)  # Убеждаемся, что должность - строка
        self.assertTrue(4 <= len(new_post) <= 10)  # Проверяем длину должности

    def test_new_random_employees(self):
        # Тестирование генерации списка случайных сотрудников
        count = 5
        employees_list = new_random_employees(count)
        self.assertEqual(len(employees_list), count)  # Проверяем количество сгенерированных сотрудников
        for fullname, post in employees_list:
            self.assertIsInstance(fullname, str)  # Убеждаемся, что ФИО - строка
            parts = fullname.split()
            self.assertEqual(len(parts), 3)  # Убеждаемся, что ФИО содержит три части (имя, фамилия, отчество)
            self.assertTrue(4 <= len(parts[0]) <= 10)  # Проверяем длину имени
            self.assertTrue(4 <= len(parts[1]) <= 10)  # Проверяем длину фамилии
            self.assertTrue(4 <= len(parts[2]) <= 10)  # Проверяем длину отчества
            self.assertIsInstance(post, str)  # Убеждаемся, что должность - строка
            self.assertTrue(4 <= len(post) <= 10)  # Проверяем длину должности

    def test_new_random_garden(self):
        # Тестирование генерации случайного названия сада
        new_name = new_random_garden()
        self.assertIsInstance(new_name, str)  # Убеждаемся, что название сада - строка
        self.assertTrue(new_name.startswith('Сад '))  # Убеждаемся, что название начинается с "Сад "
        self.assertTrue(4 <= len(new_name) <= 14)  # Проверяем длину названия сада

    def test_new_random_gardens(self):
        # Тестирование генерации списка случайных названий садов
        count = 5
        gardens_list = new_random_gardens(count)
        self.assertEqual(len(gardens_list), count)  # Проверяем количество сгенерированных названий садов
        for name in gardens_list:
            self.assertIsInstance(name, str)  # Убеждаемся, что название сада - строка
            self.assertTrue(name.startswith('Сад '))  # Убеждаемся, что название начинается с "Сад "
            self.assertTrue(4 <= len(name) <= 14)  # Проверяем длину названия сада

    def test_new_random_action(self):
        # Тестирование генерации случайного названия действия
        new_name = new_random_action()
        self.assertIsInstance(new_name, str)  # Убеждаемся, что название действия - строка
        self.assertTrue(4 <= len(new_name) <= 10)  # Проверяем длину назв


class TestGenerators(unittest.TestCase):

    def test_generate_random_string(self):
        length = 10
        gen = generate_random_string(length)
        rand_string = next(gen)
        self.assertEqual(len(rand_string), length)  # Проверяем длину строки
        self.assertTrue(rand_string.islower())  # Убеждаемся, что все символы в нижнем регистре
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.assertTrue(all(char in alphabet for char in rand_string))  # Проверяем, что все символы из русского алфавита

    def test_generator_random_fertilizer(self):
        count = 5
        gen = generator_random_fertilizer(count)
        for _ in range(count):
            name, quantity = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(4 <= len(name) <= 10)
            self.assertIsInstance(quantity, int)
            self.assertTrue(0 <= quantity <= 100)

    def test_generator_random_crop(self):
        count = 5
        gen = generator_random_crop(count)
        seasons = ['весна', 'лето', 'осень', 'зима']
        for _ in range(count):
            name, season, watering_frequency, ripening_period = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(4 <= len(name) <= 10)
            self.assertIn(season, seasons)
            self.assertIsInstance(watering_frequency, int)
            self.assertTrue(1 <= watering_frequency <= 10)
            self.assertIsInstance(ripening_period, int)
            self.assertTrue(10 <= ripening_period <= 60)

    def test_generator_random_employee(self):
        count = 5
        gen = generator_random_employee(count)
        for _ in range(count):
            fullname, post = next(gen)
            self.assertIsInstance(fullname, str)
            parts = fullname.split()
            self.assertEqual(len(parts), 3)
            self.assertTrue(all(4 <= len(part) <= 10 for part in parts))
            self.assertIsInstance(post, str)
            self.assertTrue(4 <= len(post) <= 10)

    def test_generator_random_garden(self):
        count = 5
        gen = generator_random_garden(count)
        for _ in range(count):
            name = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(name.startswith('Сад '))
            self.assertTrue(4 <= len(name) <= 14)

    def test_generator_random_action(self):
        count = 5
        gen = generator_random_action(count)
        for _ in range(count):
            name = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(4 <= len(name) <= 10)


class TestGenerators(unittest.TestCase):

    def test_generate_random_string(self):
        length = 10
        gen = generate_random_string(length)
        rand_string = next(gen)
        self.assertEqual(len(rand_string), length)  # Проверяем длину строки
        self.assertTrue(rand_string.islower())  # Убеждаемся, что все символы в нижнем регистре
        alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.assertTrue(all(char in alphabet for char in rand_string))  # Проверяем, что все символы из русского алфавита

    def test_generator_random_fertilizer(self):
        count = 5
        gen = generator_random_fertilizer(count)
        for _ in range(count):
            name, quantity = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(4 <= len(name) <= 10)
            self.assertIsInstance(quantity, int)
            self.assertTrue(0 <= quantity <= 100)

    def test_generator_random_crop(self):
        count = 5
        gen = generator_random_crop(count)
        seasons = ['весна', 'лето', 'осень', 'зима']
        for _ in range(count):
            name, season, watering_frequency, ripening_period = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(4 <= len(name) <= 10)
            self.assertIn(season, seasons)
            self.assertIsInstance(watering_frequency, int)
            self.assertTrue(1 <= watering_frequency <= 10)
            self.assertIsInstance(ripening_period, int)
            self.assertTrue(10 <= ripening_period <= 60)

    def test_generator_random_employee(self):
        count = 5
        gen = generator_random_employee(count)
        for _ in range(count):
            fullname, post = next(gen)
            self.assertIsInstance(fullname, str)
            parts = fullname.split()
            self.assertEqual(len(parts), 3)
            self.assertTrue(all(4 <= len(part) <= 10 for part in parts))
            self.assertIsInstance(post, str)
            self.assertTrue(4 <= len(post) <= 10)

    def test_generator_random_garden(self):
        count = 5
        gen = generator_random_garden(count)
        for _ in range(count):
            name = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(name.startswith('Сад '))
            self.assertTrue(4 <= len(name) <= 14)

    def test_generator_random_action(self):
        count = 5
        gen = generator_random_action(count)
        for _ in range(count):
            name = next(gen)
            self.assertIsInstance(name, str)
            self.assertTrue(4 <= len(name) <= 10)


if __name__ == '__main__':
    unittest.main()
