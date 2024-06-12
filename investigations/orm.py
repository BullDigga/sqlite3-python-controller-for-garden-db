'''orm'''


import sqlite3

class BaseModel:
    @classmethod
    def get_connection(cls):
        """Возвращает соединение с базой данных."""
        return sqlite3.connect('garden.db', isolation_level=None)

    @classmethod
    def create_table(cls):
        """Создает таблицу для модели."""
        conn = cls.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(cls.table_creation_query)
        conn.close()

    @classmethod
    def get_all(cls):
        """Возвращает все записи из таблицы модели."""
        conn = cls.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.__name__.lower()}s")
            rows = cursor.fetchall()
        conn.close()
        return [cls(**dict(zip(cls.fields, row))) for row in rows]

    @classmethod
    def get_by_id(cls, id):
        """Возвращает запись по ID из таблицы модели."""
        conn = cls.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.__name__.lower()}s WHERE id = ?", (id,))
            row = cursor.fetchone()
        conn.close()
        if row:
            return cls(**dict(zip(cls.fields, row)))
        return None

    def save(self):
        """Сохраняет запись в таблице модели."""
        conn = self.get_connection()
        with conn:
            cursor = conn.cursor()
            fields = ', '.join(self.fields[1:])
            placeholders = ', '.join('?' * (len(self.fields) - 1))
            values = [getattr(self, field) for field in self.fields[1:]]
            cursor.execute(
                f"INSERT INTO {self.__class__.__name__.lower()}s ({fields}) VALUES ({placeholders})",
                values
            )
            self.id = cursor.lastrowid
        conn.close()

    def update(self):
        """Обновляет запись в таблице модели."""
        conn = self.get_connection()
        with conn:
            cursor = conn.cursor()
            assignments = ', '.join(f"{field} = ?" for field in self.fields[1:])
            values = [getattr(self, field) for field in self.fields[1:]]
            values.append(self.id)
            cursor.execute(
                f"UPDATE {self.__class__.__name__.lower()}s SET {assignments} WHERE id = ?",
                values
            )
        conn.close()

    def delete(self):
        """Удаляет запись из таблицы модели."""
        conn = self.get_connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.__class__.__name__.lower()}s WHERE id = ?",
                (self.id,)
            )
        conn.close()

class Fertilizer(BaseModel):
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS fertilizers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        amount INTEGER
    )
    """
    fields = ('id', 'name', 'amount')

    def __init__(self, id=None, name=None, amount=None):
        self.id = id
        self.name = name
        self.amount = amount

class Crop(BaseModel):
    table_creation_query = """
    CREATE TABLE IF NOT EXISTS crops (
        id INTEGER PRIMARY KEY,
        name TEXT,
        season TEXT,
        watering_frequency INTEGER,
        ripening_period INTEGER
    )
    """
    fields = ('id', 'name', 'season', 'watering_frequency', 'ripening_period')

    def __init__(self, id=None, name=None, season=None, watering_frequency=None, ripening_period=None):
        self.id = id
        self.name = name
        self.season = season
        self.watering_frequency = watering_frequency
        self.ripening_period = ripening_period



if __name__ == '__main__':
    # Создание таблиц
    Fertilizer.create_table()
    Crop.create_table()
    
    # Пример использования
    fertilizer = Fertilizer(name='Азофоска', amount=50)
    fertilizer.save()
    
    crop = Crop(name='Пшеница', season='весна', watering_frequency=3, ripening_period=30)
    crop.save()
    
    # Получение всех удобрений
    all_fertilizers = Fertilizer.get_all()
    for fert in all_fertilizers:
        print(fert.id, fert.name, fert.amount)
    
    # Получение удобрения по ID
    fertilizer_from_db = Fertilizer.get_by_id(1)
    
    # Обновление записи
    fertilizer_from_db.amount = 75
    fertilizer_from_db.update()
    
    # Удаление записи
    # fertilizer_from_db.delete()
