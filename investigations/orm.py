import sys
import os
from mysql.connector import Error
from lib.db_controller import create_connection, MySQLCursorManager
from lib.randomik import *
from lib.generators import *
from db_manager import show_database_content

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Field:
    """
    Класс, представляющий поле в таблице базы данных.

    Атрибуты
    --------
    column_type : str
        тип данных колонки
    primary_key : bool
        указывает, является ли поле первичным ключом (по умолчанию False)
    """

    def __init__(self, column_type, primary_key=False):
        self.column_type = column_type
        self.primary_key = primary_key


class IntegerField(Field):
    """
    Класс, представляющий поле с целочисленным значением в таблице базы данных.

    Наследуется от Field.

    Атрибуты
    --------
    min_value : int
        минимальное значение (по умолчанию None)
    max_value : int
        максимальное значение (по умолчанию None)
    """

    def __init__(self, primary_key=False, min_value=None, max_value=None):
        super().__init__('INT', primary_key)
        self.min_value = min_value
        self.max_value = max_value


class StringField(Field):
    """
    Класс, представляющий поле со строковым значением в таблице базы данных.

    Наследуется от Field.

    Атрибуты
    --------
    max_length : int
        максимальная длина строки (по умолчанию 255)
    """

    def __init__(self, max_length=255, choices=None):
        super().__init__(f'VARCHAR({max_length})')
        self.choices = choices


class ForeignKey(Field):
    """
    Класс, представляющий поле внешнего ключа в таблице базы данных.

    Наследуется от Field.

    Атрибуты
    --------
    reference_table : str
        таблица, на которую ссылается этот внешний ключ
    """

    def __init__(self, reference_table):
        super().__init__('INT')
        self.reference_table = reference_table


class ModelMeta(type):
    """
    Мета-класс, используемый для определения метаданных и создания таблиц для моделей.

    Методы
    ------
    __new__(cls, name, bases, attrs)
        Инициализирует новый класс модели с колонками, основанными на docstring и атрибутах класса.
    """

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)

        columns = {}

        doc = attrs.get('__doc__', '')
        for line in doc.splitlines():
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) < 2:
                    continue  # Пропускаем строки, где нет ':'

                column_name = parts[0].strip()
                column_type = parts[1].strip().lower()

                if column_type.startswith('charfield'):
                    max_length = int(parts[2].split('=')[1]) if len(parts) > 2 and 'max_length' in parts[2] else 255
                    choices = None
                    if len(parts) > 3 and 'choices' in parts[3]:
                        choices = parts[3].split('=')[1].strip().replace("'", "").split(',')
                    columns[column_name] = StringField(max_length=max_length, choices=choices)
                elif column_type == 'integerfield':
                    min_value = None
                    max_value = None
                    if len(parts) > 2 and 'min' in parts[2]:
                        min_value = int(parts[2].split('=')[1].strip())
                    if len(parts) > 3 and 'max' in parts[3]:
                        max_value = int(parts[3].split('=')[1].strip())
                    columns[column_name] = IntegerField(min_value=min_value, max_value=max_value)
                elif column_type == 'foreignkey':
                    reference_table = parts[2].split('=')[1].strip() if len(parts) > 2 else None
                    columns[column_name] = ForeignKey(reference_table=reference_table)

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                columns[attr_name] = attr_value

        attrs['_columns'] = columns
        return super().__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)


class Model(metaclass=ModelMeta):
    """
    Базовый класс для всех моделей, использующий метакласс ModelMeta.

    Методы
    ------
    create_table()
        Создает таблицу базы данных для модели.
    save()
        Сохраняет экземпляр в базу данных.
    get(**kwargs)
        Извлекает экземпляр из базы данных на основе предоставленных ключевых аргументов.
    """

    @classmethod
    def create_table(cls):
        """
        Создает таблицу базы данных для модели.
        """
        columns = []
        for name, field in cls._columns.items():
            if isinstance(field, Field):
                column_def = f"{name} {field.column_type}"
                if field.primary_key:
                    column_def += " PRIMARY KEY"
                if isinstance(field, ForeignKey):
                    column_def += f" REFERENCES {field.reference_table}(id)"
                columns.append(column_def)
        columns_str = ", ".join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()}s ({columns_str})"

        with create_connection('garden') as conn:
            if conn:
                try:
                    with MySQLCursorManager(conn) as cursor:
                        cursor.execute(create_table_query)
                        print(f"Таблица '{cls.__name__.lower()}s' успешно создана")
                except Error as e:
                    print(f"Ошибка: '{e}'")

    def save(self):
        """
        Сохраняет экземпляр в базу данных.
        """
        columns = []
        values = []
        for name, field in self._columns.items():
            if isinstance(field, Field):
                columns.append(name)
                values.append(getattr(self, name))

        columns_str = ", ".join(columns)
        placeholders_str = ", ".join(['%s'] * len(values))
        insert_query = f"INSERT INTO {self.__class__.__name__.lower()}s ({columns_str}) VALUES ({placeholders_str})"

        with create_connection('garden') as conn:
            if conn:
                try:
                    with MySQLCursorManager(conn) as cursor:
                        cursor.execute(insert_query, values)
                        last_id = cursor.lastrowid
                        setattr(self, 'id', last_id)
                        print(f"Объект сохранен в таблицу '{self.__class__.__name__.lower()}s'")
                except Error as e:
                    print(f"Ошибка: '{e}'")

    @classmethod
    def get(cls, **kwargs):
        """
        Извлекает экземпляр из базы данных на основе предоставленных ключевых аргументов.

        Параметры
        ---------
        **kwargs : dict
            Ключевые аргументы для фильтрации запроса.
        """
        column = list(kwargs.keys())[0]
        value = list(kwargs.values())[0]
        select_query = f"SELECT * FROM {cls.__name__.lower()}s WHERE {column} = %s"

        with create_connection('garden') as conn:
            if conn:
                try:
                    with MySQLCursorManager(conn) as cursor:
                        cursor.execute(select_query, (value,))
                        result = cursor.fetchone()
                        if result:
                            obj = cls()
                            for idx, column in enumerate(cursor.column_names):
                                setattr(obj, column, result[idx])
                            return obj
                        else:
                            return None
                except Error as e:
                    print(f"Ошибка: '{e}'")
                    return None


class Fertilizer(Model):
    """
    Класс, представляющий удобрение.

    Наследуется от Model.

    :Attributes:
        id: IntegerField
            первичный ключ удобрения
        name: StringField
            название удобрения
        amount: IntegerField
            количество доступного удобрения
    """

    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount

    def save(self):
        query = "INSERT INTO fertilizers (name, amount) VALUES (%s, %s)"
        values = (self.name, self.amount)
        with create_connection('garden') as connection:
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, values)
                        connection.commit()
                        print("Fertilizer saved successfully")
                except Error as e:
                    print(f"The error '{e}' occurred")


class Crop(Model):
    """
    Класс, представляющий культуру.

    :Attributes:
        id: IntegerField
            первичный ключ культуры
        name: StringField
            название культуры
        season: StringField
            сезон выращивания культуры
        watering_frequency: IntegerField
            частота полива культуры
        ripening_period: IntegerField
            срок созревания культуры
    """

    def __init__(self, name=None, season=None, watering_frequency=None, ripening_period=None):
        self.name = name
        self.season = season
        self.watering_frequency = watering_frequency
        self.ripening_period = ripening_period

    @classmethod
    def create_table(cls, min_watering_frequency=None, max_watering_frequency=None, possible_seasons=None):
        """
        Создает таблицу базы данных для модели Crop с учетом ограничений частоты полива и возможных сезонов.

        Параметры
        ---------
        min_watering_frequency : int, optional
            Минимальное значение частоты полива.
        max_watering_frequency : int, optional
            Максимальное значение частоты полива.
        possible_seasons : list of str, optional
            Список допустимых сезонов для атрибута season.
        """
        cls.min_watering_frequency = min_watering_frequency
        cls.max_watering_frequency = max_watering_frequency
        cls.possible_seasons = possible_seasons
        super().create_table()

    def save(self):
        """
        Сохраняет экземпляр культуры в базе данных.

        Поддерживает проверку ограничений, определенных при создании таблицы,
        а также обязательное значение для атрибута season, если possible_seasons задано.
        """
        # Проверяем, что значение season соответствует одному из допустимых значений, если они заданы
        if self.possible_seasons is not None:
            if self.season not in self.possible_seasons:
                raise ValueError(f"Сезон выращивания должен быть одним из: {', '.join(self.possible_seasons)}")

        # Проверяем, что значение watering_frequency соответствует заданным ограничениям
        if self.watering_frequency is not None:
            if (self.min_watering_frequency is not None and self.watering_frequency < self.min_watering_frequency) or \
               (self.max_watering_frequency is not None and self.watering_frequency > self.max_watering_frequency):
                raise ValueError(f"Значение частоты полива должно быть между {self.min_watering_frequency} и {self.max_watering_frequency}")

        query = "INSERT INTO crops (name, season, watering_frequency, ripening_period) VALUES (%s, %s, %s, %s)"
        values = (self.name, self.season, self.watering_frequency, self.ripening_period)
        with create_connection('garden') as connection:
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, values)
                        connection.commit()
                        print("Crop saved successfully")
                except Error as e:
                    print(f"The error '{e}' occurred")


class Employee(Model):
    """
    Класс, представляющий сотрудника.

    :Attributes:
        id: IntegerField
            первичный ключ сотрудника
        fullname: StringField
            полное имя сотрудника
        post: StringField
            должность сотрудника
    """

    def __init__(self, fullname=None, post=None):
        self.fullname = fullname
        self.post = post

    def save(self):
        query = "INSERT INTO employees (fullname, post) VALUES (%s, %s)"
        values = (self.fullname, self.post)
        with create_connection('garden') as connection:
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, values)
                        connection.commit()
                        print("Employee saved successfully")
                except Error as e:
                    print(f"The error '{e}' occurred")


class Garden(Model):
    """
    Класс, представляющий сад.

    Наследуется от Model.

    :Attributes:
        id: IntegerField
            первичный ключ сада
        name: StringField
            название сада
    """

    def __init__(self, name=None):
        self.name = name

    def save(self):
        query = "INSERT INTO gardens (name) VALUES (%s)"
        values = (self.name,)
        with create_connection('garden') as connection:
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, values)
                        connection.commit()
                        print("Garden saved successfully")
                except Error as e:
                    print(f"The error '{e}' occurred")

class Action(Model):
    """
    Класс, представляющий действие в саду.

    Наследуется от Model.

    :Attributes:
        id: IntegerField
            первичный ключ действия
        name: StringField
            описание действия
    """

    def __init__(self, name=None):
        self.name = name

    def save(self):
        query = "INSERT INTO actions (name) VALUES (%s)"
        values = (self.name,)
        with create_connection('garden') as connection:
            if connection:
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(query, values)
                        connection.commit()
                        print("Action saved successfully")
                except Error as e:
                    print(f"The error '{e}' occurred")

def generate(model, n):
    """
    Генерирует n экземпляров заданного класса model.

    Параметры
    ----------
    model : type
        Класс модели для генерации экземпляров.
    n : int
        Количество экземпляров для создания.

    Возвращает
    ----------
    list
        Список экземпляров заданного класса.
    """
    if model == Crop:
        return list(generator_random_crop(n))
    elif model == Fertilizer:
        return list(generator_random_fertilizer(n))
    elif model == Garden:
        return list(generator_random_garden(n))
    elif model == Action:
        return list(generator_random_action(n))
    elif model == Employee:
        return list(generator_random_employee(n))
    else:
        raise ValueError("Неверный класс модели")

# Пример использования:
if __name__ == '__main__':
    Crop.create_table()
    crops = generate(Crop, 10)
    for crop_params in crops:
        crop = Crop(*crop_params)
        crop.save()

    Fertilizer.create_table()
    fertilizers = generate(Fertilizer, 10)
    for fertilizer_params in fertilizers:
        fertilizer = Fertilizer(*fertilizer_params)
        fertilizer.save()

    Garden.create_table()
    gardens = generate(Garden, 10)
    for garden_params in gardens:
        garden = Garden(garden_params)
        garden.save()

    Action.create_table()
    actions = generate(Action, 10)
    for action_params in actions:
        action = Action(action_params)
        action.save()

    Employee.create_table()
    employees = generate(Employee, 10)
    for employee_params in employees:
        employee = Employee(*employee_params)
        employee.save()

    show_database_content()