import sys
import os
from mysql.connector import Error
from lib.db_controller import create_connection, MySQLCursorManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


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
    """

    def __init__(self, primary_key=False):
        super().__init__('INT', primary_key)


class StringField(Field):
    """
    Класс, представляющий поле со строковым значением в таблице базы данных.

    Наследуется от Field.

    Атрибуты
    --------
    max_length : int
        максимальная длина строки (по умолчанию 255)
    """

    def __init__(self, max_length=255):
        super().__init__(f'VARCHAR({max_length})')


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
                    max_length = int(parts[2].split('=')[1]) if len(parts) > 2 else 255
                    columns[column_name] = StringField(max_length=max_length)
                elif column_type == 'integerfield':
                    columns[column_name] = IntegerField()
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

    id = IntegerField(primary_key=True)
    name = StringField(max_length=255)
    amount = IntegerField()


class Crop(Model):
    """
    Класс, представляющий культуру.

    Наследуется от Model.

    :Attributes:
        id: IntegerField
            первичный ключ культуры
        name: StringField
            название культуры
        plant_date: StringField
            дата посадки культуры
    """

    id = IntegerField(primary_key=True)
    name = StringField(max_length=255)
    plant_date = StringField(max_length=255)


class Employee(Model):
    """
    Класс, представляющий сотрудника.

    Наследуется от Model.

    :Attributes:
        id: IntegerField
            первичный ключ сотрудника
        fullname: StringField
            полное имя сотрудника
        position: StringField
            должность сотрудника
    """

    id = IntegerField(primary_key=True)
    fullname = StringField(max_length=255)
    position = StringField(max_length=255)


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

    id = IntegerField(primary_key=True)
    name = StringField(max_length=255)


class Action(Model):
    """
    Класс, представляющий действие в саду.

    Наследуется от Model.

    :Attributes:
        id: IntegerField
            первичный ключ действия
        description: StringField
            описание действия
    """

    id = IntegerField(primary_key=True)
    description = StringField(max_length=255)


if __name__ == "__main__":
    # Создание таблицы для модели Fertilizer
    Fertilizer.create_table()

    # Создание таблицы для модели Crop
    Crop.create_table()

    # Создание таблицы для модели Employee
    Employee.create_table()

    # Создание таблицы для модели Garden
    Garden.create_table()

    # Создание таблицы для модели Action
    Action.create_table()
