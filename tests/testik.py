import sqlite3
import os
from investigations.orm import Fertilizer, Crop, BaseModel


def main():
    # Настройка: создание тестовой базы данных и таблиц
    db_name = 'test_garden.db'

    @classmethod
    def get_test_connection(cls):
        return sqlite3.connect(db_name, isolation_level=None)

    BaseModel.get_connection = get_test_connection

    # Создание таблиц
    Fertilizer.create_table()
    Crop.create_table()

    # Очистка таблиц перед тестами
    conn = BaseModel.get_connection()
    with conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM fertilizers')
        cur.execute('DELETE FROM crops')
    conn.close()  # Закрываем соединение

    print("Тестирование создания и чтения записи в таблице 'fertilizers'")
    fertilizer = Fertilizer(name='Азофоска', amount=50)
    fertilizer.save()
    fertilizers = Fertilizer.get_all()
    assert len(fertilizers) == 1, f"Expected 1 fertilizer, got {len(fertilizers)}"
    assert fertilizers[0].name == 'Азофоска', f"Expected name 'Азофоска', got {fertilizers[0].name}"
    assert fertilizers[0].amount == 50, f"Expected amount 50, got {fertilizers[0].amount}"
    print("Тест создания и чтения записи в таблице 'fertilizers' пройден.")

    print("Тестирование обновления записи в таблице 'fertilizers'")
    fertilizer.amount = 75
    fertilizer.update()
    updated_fertilizer = Fertilizer.get_by_id(fertilizer.id)
    assert updated_fertilizer.amount == 75, f"Expected amount 75, got {updated_fertilizer.amount}"
    print("Тест обновления записи в таблице 'fertilizers' пройден.")

    print("Тестирование удаления записи из таблицы 'fertilizers'")
    fertilizer.delete()
    fertilizers = Fertilizer.get_all()
    assert len(fertilizers) == 0, f"Expected 0 fertilizers, got {len(fertilizers)}"
    print("Тест удаления записи из таблицы 'fertilizers' пройден.")

    print("Тестирование создания и чтения записи в таблице 'crops'")
    crop = Crop(name='Пшеница', season='весна', watering_frequency=3, ripening_period=30)
    crop.save()
    crops = Crop.get_all()
    assert len(crops) == 1, f"Expected 1 crop, got {len(crops)}"
    assert crops[0].name == 'Пшеница', f"Expected name 'Пшеница', got {crops[0].name}"
    assert crops[0].season == 'весна', f"Expected season 'весна', got {crops[0].season}"
    assert crops[0].watering_frequency == 3, f"Expected watering frequency 3, got {crops[0].watering_frequency}"
    assert crops[0].ripening_period == 30, f"Expected ripening period 30, got {crops[0].ripening_period}"
    print("Тест создания и чтения записи в таблице 'crops' пройден.")

    # Очистка: удаление тестовой базы данных
    os.remove(db_name)


if __name__ == '__main__':
    main()
