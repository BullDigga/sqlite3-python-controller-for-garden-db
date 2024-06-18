import matplotlib.pyplot as plt
import timeit
import random
from lib.generators import *  # Импортируйте функцию генерации случайных строк из вашего модуля


def plot_generation_graphics(funcs_to_measure, count_generation):
    """
    Построение графика времени выполнения генерации данных для заданных функций.

    Parameters:
    funcs_to_measure : list of tuples
        Список кортежей, каждый кортеж содержит функцию и её аргументы.
    count_generation : int
        Максимальное количество данных, которое будет генерироваться для каждой из функций.

    Returns:
    None
    """
    # Список для хранения результатов времени выполнения
    func_times = {func.__name__: [] for func, _ in funcs_to_measure}

    # Перебор по количеству генерируемых элементов
    for num_instances in range(1, count_generation + 1):
        for func, args in funcs_to_measure:
            # Измеряем время для текущего количества генерируемых элементов
            time_taken = measure_generation_time(func, num_instances)
            func_times[func.__name__].append(time_taken)

    # Подготовка данных для построения графика
    n_values = list(range(1, count_generation + 1))
    labels = [func.__name__ for func, _ in funcs_to_measure]
    plot_data(n_values, [func_times[func_name] for func_name in labels], labels,
              'Количество генерируемых элементов', 'Время генерации (секунды)',
              'Время генерации данных', save_path='generation_times.png')


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
        color = plt.cm.get_cmap('tab10')(i)  # Используем цветовую карту для различных цветов
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


if __name__ == '__main__':
    count_generation = 9

    funcs_to_measure = [
        (generator_random_fertilizer, ()),
        (generator_random_crop, ()),
        (generator_random_action, ())
    ]

    plot_generation_graphics(funcs_to_measure, count_generation)
