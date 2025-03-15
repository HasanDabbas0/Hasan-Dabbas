import numpy as np  # работа с массивами
import matplotlib.pyplot as plt  # отображение графиков
import pandas as pd  # работа с датафреймами (типа табличек)
from scipy.optimize import curve_fit  # аппроксимация
import os
import re  # две библиотеки для предобработки и очистки файлов

def process_file(filepath, a, b, all_approx_angles, all_approx_omegas):
    try:
        # Поиск напряжения в имени файла
        match = re.search(r'data([−-])?(\d+)\.csv', filepath)
        if match:
            sign = match.group(1) or ''
            U_pr = int(sign + match.group(2))
        else:
            U_pr = 0

        # Чтение данных из CSV
        df = pd.read_csv(filepath, header=None, delimiter=' ')
        data = df.to_numpy()
        time = data[:, 0]
        angle = data[:, 1] * (np.pi / 180)  # Перевод в радианы
        omega = data[:, 2] * (np.pi / 180)

        # Функции для аппроксимации
        def fun(time, a, b):
            return U_pr * a * (time - b * (1 - np.exp(-time / b)))

        def fun2(time, a, b):
            return a * U_pr * (1 - np.exp(-time / b))

        # Аппроксимация данных
        popt, pcov = curve_fit(fun, time, angle)
        popt2, pcov2 = curve_fit(fun2, time, omega)

        # Вывод параметров
        print(f"Результаты для файла: {filepath}")
        print(f"Параметры аппроксимации угла: k={popt[0]}, Tm={popt[1]}, U_pr={U_pr}")
        print(f"Параметры аппроксимации угловой скорости: k={popt2[0]}, Tm={popt2[1]}, U_pr={U_pr}")

        # Графики для каждого файла
        plt.figure(figsize=(10, 5))

        # График угла
        plt.subplot(1, 2, 1)
        plt.plot(time, angle, label='Исходные данные')
        approx_angle = fun(time, *popt)
        plt.plot(time, approx_angle, color='orange', label='Аппроксимация')
        plt.xlabel('time, s')
        plt.ylabel('angle, rad')
        plt.title('График зависимости угла от времени')
        plt.legend()

        # График угловой скорости
        plt.subplot(1, 2, 2)
        plt.plot(time, omega, label='Исходные данные')
        approx_omega = fun2(time, *popt2)
        plt.plot(time, approx_omega, color='orange', label='Аппроксимация')
        plt.xlabel('time, s')
        plt.ylabel('angle speed, rad/s')
        plt.title('График зависимости угловой скорости от времени')
        plt.legend()

        plt.tight_layout()
        plt.show()

        # Сохранение данных для общих графиков
        all_approx_angles.append((time, approx_angle, filepath))
        all_approx_omegas.append((time, approx_omega, filepath))

        # Сохранение параметров для усреднения
        a.append(popt[0])
        a.append(popt2[0])
        b.append(popt[1])
        b.append(popt2[1])

    except Exception as e:
        print(f"Ошибка при обработке файла {filepath}: {e}")

if __name__ == "__main__":
    a = []  # Список для параметров k
    b = []  # Список для параметров Tm
    all_approx_angles = []  # Список для данных аппроксимированных углов
    all_approx_omegas = []  # Список для данных аппроксимированных угловых скоростей

    # Обработка всех CSV-файлов в папке
    folder_path = "lab1"
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            process_file(filepath, a, b, all_approx_angles, all_approx_omegas)

    # Вычисление и вывод средних значений
    k_average = sum(a) / len(a)  # усредненный аргумент k
    Tm_average = sum(b) / len(b)  # усредненный аргумент Tm
    print(f"Среднее k: {k_average}")
    print(f"Среднее Tm: {Tm_average}")

    # Общий график для углов
    plt.figure(figsize=(10, 5))
    for time, approx_angle, filepath in all_approx_angles:
        plt.plot(time, approx_angle, label=f'Аппроксимация {filepath}')
    plt.xlabel('time, s')
    plt.ylabel('angle, rad')
    plt.title('Сравнение аппроксимированных углов для всех файлов')
    plt.legend()
    plt.show()

    # Общий график для угловых скоростей
    plt.figure(figsize=(10, 5))
    for time, approx_omega, filepath in all_approx_omegas:
        plt.plot(time, approx_omega, label=f'Аппроксимация {filepath}')
    plt.xlabel('time, s')
    plt.ylabel('angle speed, rad/s')
    plt.title('Сравнение аппроксимированных угловых скоростей для всех файлов')
    plt.legend()
    plt.show()