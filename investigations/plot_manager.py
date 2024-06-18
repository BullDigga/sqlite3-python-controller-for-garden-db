import matplotlib.pyplot as plt
import timeit
import random
from lib.generators import *  # Импортируйте функцию генерации случайных строк из вашего модуля
from db_manager import measure_query_time, show_database_content
from lib.db_controller import *


def generate_data_for_table(table_name, count):
    """
    Генерирует данные для указанной таблицы.

    Parameters:
    table_name : str
        Название таблицы, в которую будут вставляться данные.
    count : int
        Количество строк данных для вставки.
    """
    with create_connection('garden') as conn:
        if conn:
            with conn.cursor() as cursor:
                if table_name == 'gardens':
                    for name in generator_random_garden(count):
                        insert_into_gardens('garden', [(name, )])
                elif table_name == 'crops':
                    for name, season, watering_frequency, ripening_period in generator_random_crop(count):
                        cursor.execute(
                            insert_into_crops('garden', [(name, season, watering_frequency, ripening_period)])
                        )
                elif table_name == 'fertilizers':
                    for name, amount in generator_random_fertilizer(count):
                        insert_into_fertilizers('garden', [(name, amount)])
                elif table_name == 'beds':
                    for garden_id, crop_id, fertilizer_id in generator_random_bed(count):
                        insert_into_beds('garden', [(garden_id, crop_id, fertilizer_id)])


def plot_generation_graphics(funcs_to_measure, count_generation, title='График времени генерации данных'):
    """
    Построение графика времени выполнения генерации данных для заданных функций.

    Parameters:
    funcs_to_measure : list of tuples
        Список кортежей, каждый кортеж содержит функцию и её аргументы.
    count_generation : int
        Максимальное количество данных, которое будет генерироваться для каждой из функций.
    title : str, optional
        Заголовок графика. По умолчанию 'График времени генерации данных'.

    Returns:
    None
    """
    # Список для хранения результатов времени выполнения
    func_times = {func.__name__: [] for func, _ in funcs_to_measure}

    # Перебор по количеству генерируемых элементов
    for num_instances in range(1, count_generation + 1):
        for func, args in funcs_to_measure:
            # Измеряем время для текущего количества генерируемых элементов
            time_taken = measure_generation_time(func, num_instances, *args)
            func_times[func.__name__].append(time_taken)

    # Подготовка данных для построения графика
    n_values = list(range(1, count_generation + 1))
    labels = [func.__name__ for func, _ in funcs_to_measure]
    plot_data(n_values, [func_times[func_name] for func_name in labels], labels,
              'Количество генерируемых элементов', 'Время генерации (секунды)',
              title, save_path='generation_times.png')

def measure_generation_time(func, num_instances):
    """
    Измеряет время выполнения генерации данных заданной функцией.

    Parameters:
    func : function
        Функция, время выполнения генерации которой нужно измерить.
    num_instances : int
        Количество данных, которое нужно сгенерировать.

    Returns:
    float
        Время выполнения функции в секундах.
    """
    # Подготовка кода для измерения времени выполнения функции генерации
    setup_code = f'''
from __main__ import {func.__name__}
'''

    stmt_code = f'''
list({func.__name__}({num_instances}))
'''

    # Измерение времени выполнения функции генерации
    time_taken = timeit.timeit(stmt=stmt_code, setup=setup_code, number=1)

    return time_taken

def plot_data(x_values, y_values_list, labels, x_label, y_label, title, save_path=None):
    """
    Функция для построения графика с заданными параметрами и сохранения его на диск.

    Parameters:
    x_values : list
        Список значений по оси X.
    y_values_list : list of lists
        Список списков значений по оси Y (каждый вложенный список соответствует отдельному ряду данных).
    labels : list
        Список меток для легенды (должен иметь такое же количество элементов, как и y_values_list).
    x_label : str
        Название оси X.
    y_label : str
        Название оси Y.
    title : str
        Заголовок графика.
    save_path : str, optional
        Путь для сохранения графика на диск. Если не указан, график не сохраняется.

    Returns:
    None
    """
    # Убедимся, что количество рядов данных совпадает с количеством меток для легенды
    assert len(y_values_list) == len(labels), "Количество рядов данных должно совпадать с количеством меток для легенды"

    # Различные стили для линий и маркеров
    line_styles = ['-', '--', '-.', ':']
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'P', 'X']

    # Создание графика
    plt.figure(figsize=(10, 6))

    # Построение каждого ряда данных
    for i, y_values in enumerate(y_values_list):
        line_style = line_styles[i % len(line_styles)]
        marker = markers[i % len(markers)] if len(x_values) < 10 else None
        color = plt.cm.get_cmap('tab10')(i)
        plt.plot(x_values, y_values, marker=marker, linestyle=line_style, color=color, label=labels[i])

    # Добавление заголовка и подписей осей
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Добавление легенды
    plt.legend()

    # Сохранение графика, если указан путь
    if save_path:
        plt.savefig(save_path)

    # Отображение графика
    plt.tight_layout()
    plt.show()


def plot_select_graphics(query_list, title='Построение графиков с запросом SELECT'):
    """
    Функция для построения графиков времени выполнения запросов SELECT.

    Parameters:
    query_list : list of str
        Список запросов SELECT.
    title : str
        Заголовок графика.

    Returns:
    None
    """
    count_rows = [50, 100, 150, 200]
    results = []

    # Генерация данных перед выполнением запросов
    clear_tables()
    for count in count_rows:
        generate_data_for_table('gardens', count)
        generate_data_for_table('crops', count)
        generate_data_for_table('fertilizers', count)
        generate_data_for_table('beds', count)

        times = []
        for query in query_list:
            limited_query = f"{query} LIMIT {count}"
            time_taken = measure_query_time(limited_query)
            times.append(time_taken)
        results.append(times)

    # Транспонируем результаты для корректного отображения на графике
    transposed_results = list(map(list, zip(*results)))

    plot_data(count_rows, transposed_results, query_list, 'Количество строк', 'Время выполнения (секунды)', title)


def measure_insert_time(insert_func, data):
    """
    Измеряет время выполнения вставки данных заданной функцией.

    Parameters:
    insert_func : function
        Функция, которая выполняет вставку данных.
    data : list
        Данные для вставки.

    Returns:
    float
        Время выполнения функции в секундах.
    """
    start_time = timeit.default_timer()
    insert_func('garden', data)
    time_taken = timeit.default_timer() - start_time
    return time_taken

def plot_insert_graphics(insert_funcs, data_generators, count_rows, title='Построение графиков с запросами INSERT'):
    """
    Функция для построения графиков времени выполнения запросов INSERT.

    Parameters:
    insert_funcs : list of tuples
        Список кортежей, каждый кортеж содержит функцию вставки данных и её имя.
    data_generators : list of functions
        Список функций генерации данных для вставки.
    count_rows : list of int
        Список значений количества строк для вставки.
    title : str
        Заголовок графика.

    Returns:
    None
    """
    results = []

    for count in count_rows:
        times = []
        for (insert_func, func_name), data_gen in zip(insert_funcs, data_generators):
            data = list(data_gen(count))
            time_taken = measure_insert_time(insert_func, data)
            times.append(time_taken)
        results.append(times)

    # Транспонируем результаты для корректного отображения на графике
    transposed_results = list(map(list, zip(*results)))

    plot_data(count_rows, transposed_results, [name for _, name in insert_funcs], 'Количество строк', 'Время выполнения (секунды)', title)


if __name__ == '__main__':

    count_generation = 300


    # funcs_to_measure = [
    #     (generator_random_fertilizer, ()),
    #     (generator_random_crop, ()),
    #     (generator_random_action, ())
    # ]
    # plot_generation_graphics(funcs_to_measure, count_generation, title='Время генерации данных (без связи FK)')


    # funcs_to_measure = [
    #     (generator_random_garden, ()),
    #     (generator_random_crop, ()),
    #     (generator_random_fertilizer, ()),
    #     (generator_random_bed, ())
    # ]
    # plot_generation_graphics(funcs_to_measure, count_generation, title='Время генерации данных (со связью FK)')


    # query_list = [
    #     "SELECT * FROM gardens",
    #     "SELECT * FROM crops WHERE season='лето'",
    #     "SELECT * FROM fertilizers WHERE name LIKE 'A%'",
    #     "SELECT * FROM beds WHERE garden_id = 1"
    # ]
    # plot_select_graphics(query_list, title='Время выполнения запросов SELECT')


    # insert_funcs = [
    #     (insert_into_fertilizers, 'insert_into_fertilizers'),
    #     (insert_into_crops, 'insert_into_crops'),
    #     (insert_into_gardens, 'insert_into_gardens')
    # ]
    # data_generators = [
    #     generator_random_fertilizer,
    #     generator_random_crop,
    #     generator_random_garden
    # ]
    # count_rows = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]
    # plot_insert_graphics(insert_funcs, data_generators, count_rows, title='Время выполнения запросов INSERT')
    #
    # show_database_info()