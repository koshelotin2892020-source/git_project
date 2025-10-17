import random
from collections import Counter


def task1():
    print("=== ЗАДАНИЕ 1 ===")
    # Таблица умножения
    print("Таблица умножения:")
    for i in range(1, 10):
        for j in range(1, 10):
            print(i, '*', j, '=', i * j, end='\t')
        print()
    print()
    # Сумма нечетных чисел
    s = 0
    for i in range(1, 100):
        if i % 2 == 1:
            s += i
    print(f"Сумма нечетных чисел от 1 до 99: {s}")
    print()
    # Делители числа
    digit = int(input('Введите число: '))
    print(f'Делители числа {digit}:')
    for i in range(1, digit):
        if digit % i == 0:
            print(i, end=' ')
    print('\n')
    # Факториал
    fact = 1
    digit = int(input('Введите число: '))
    if digit == 0:
        fact = 1
    else:
        for i in range(1, digit + 1):
            fact *= i
    print(f'Факториал числа "{digit}" = {fact}')
    print()
    # Последовательность Фибоначчи
    mass = [0, 1]
    n = int(input("Введите длину последовательности Фибоначчи: "))
    if n == 1:
        mass = [0]
    elif n == 2:
        mass = [0, 1]
    else:
        for i in range(2, n):
            next_num = mass[i-1] + mass[i-2]
            mass.append(next_num)
    print("Последовательность Фибоначчи:", ", ".join(map(str, mass)))
    print()


def task2():
    print("=== ЗАДАНИЕ 2 ===")
    # Массив случайных чисел
    numbers = [random.randint(-50, 50) for _ in range(10)]
    print('Массив случайных чисел: ', numbers)
    # Четные элементы
    print('Четные элементы списка numbers:')
    for i in numbers:
        if i % 2 == 0:
            print(i, end=' ')
    print()
    # Минимальное и максимальное число
    mx = numbers[0]
    mn = numbers[0]
    for i in numbers:
        if mn > i:
            mn = i
        if mx < i:
            mx = i
    print(f'Минимальное число: {mn}, Максимальное число: {mx}')
    print()
    # Ввод 5 чисел и сортировка
    mass = []
    for i in range(5):
        num = int(input(f'Введите число {i+1}/5: '))
        mass.append(num)
    mass.sort()
    print('Отсортированный массив:', mass)
    print()
    # Удаление дубликатов
    numbers_0 = [12, 45, 0, 4, 4, 5, 5, 12]
    print('Массив с дубликатами: ', numbers_0)
    unique_list = []
    for i in numbers_0:
        if i not in unique_list:
            unique_list.append(i)
    print('Массив без дубликатов: ', unique_list)
    print()
    # Обмен первого и последнего элемента
    if len(numbers) > 0:
        numbers[0], numbers[-1] = numbers[-1], numbers[0]
        print('Поменял местами первый и последний элементы: ', numbers)
    print()


def task3():
    print("=== ЗАДАНИЕ 3 ===")
    # Средний балл студентов
    dict_0 = {'Alex': [3, 3, 4, 2, 2],
              'Ben': [5, 5, 4, 5, 4],
              'YaoYao': [3, 2, 2, 2]}
    for i, j in dict_0.items():
        sr_a = sum(j)/len(j)
        print(f'Имя: {i}, Средний балл: {sr_a:.2f}')
    print()
    # Частота символов в строке
    str_0 = input('Введите строку: ')
    dict_1 = {}
    for i in str_0:
        if i in dict_1:
            dict_1[i] += 1
        else:
            dict_1[i] = 1
    print('Частота символов:', dict_1)
    print()
    # Квадраты чисел
    dict_2 = {}
    for i in range(1, 11):
        dict_2[i] = i**2
    print('Квадраты чисел от 1 до 10:', dict_2)
    print()
    # Объединение списков в словарь
    keys = ['Keya', 'Ember', 'Nina']
    values = [1000, 2000, 2289]
    dict_3 = dict(zip(keys, values))
    print('Объединенный словарь:', dict_3)
    print()


def task4():
    print("=== ЗАДАНИЕ 4 ===")
    # Операции с множествами
    A = {12, 15, 41}
    B = {12, 54, 30}
    print(f'Множество A: {A}')
    print(f'Множество B: {B}')
    print(f'Объединение (A | B): {A | B}')
    print(f'Пересечение (A & B): {A & B}')
    print()
    # Множество из строки
    str_0 = set(input('Введите строку (слова через пробел): ').split())
    print('Множество слов:', str_0)
    print()
    # Общие элементы списков
    A_list = [12, 15, 41]
    B_list = [12, 54, 30]
    common = set(A_list) & set(B_list)
    print(f'Список A: {A_list}')
    print(f'Список B: {B_list}')
    print(f'Общие элементы: {common}')
    print()
    # Проверка подмножества
    A_set = {12, 15, 41}
    B_set = {12, 41}
    print(f'Множество A: {A_set}')
    print(f'Множество B: {B_set}')
    print(f'B является подмножеством A: {B_set.issubset(A_set)}')
    print()
    # Удаление элементов меньше n
    A = {12, 15, 41, 5, 8, 20}
    print(f'Исходное множество: {A}')
    n = int(input('Введите число: '))
    A = {x for x in A if x >= n}
    print(f'Множество после удаления элементов меньше {n}: {A}')
    print()


def task5():
    print("=== ЗАДАНИЕ 5 ===")
    # Уникальные значения
    numbers = [random.randint(-10, 10) for _ in range(20)]
    print('Массив случайных чисел: ', numbers)
    dict_0 = {}
    for i in numbers:
        dict_0[i] = numbers.count(i)
    print(dict_0)
    m = []
    for i, j in dict_0.items():
        if j == 1:
            m.append(i)
    print(m)
    # print("Уникальные значения:", list(set(numbers)))
    
    print()
    # Частота элементов
    mass = [12, 12, 54, 99, 12, 54]
    dict_1 = {}
    for i in mass:
        dict_1[i] = mass.count(i)
    print('Массив:', mass)
    print('Частота элементов:', dict_1)
    print()
    # Слова длиннее 5 символов
    mass_1 = ['Яблоко', 'Нож', 'Лицо', 'Рекогносцировка']
    set_0 = {i for i in mass_1 if len(i) > 5}
    print('Список слов:', mass_1)
    print('Слова длиннее 5 символов:', set_0)
    print()
    # Частота слов в строке
    str_0 = input('Введите строку: ').split()
    dict_1 = {}
    for i in str_0:
        if i in dict_1:
            dict_1[i] += 1
        else:
            dict_1[i] = 1
    print('Частота слов:', dict_1)
    print()
    # Уникальные значения
    numbers_0 = [12, 45, 88, 12, 88]
    print('Массив чисел: ', numbers_0)
    print("Уникальные значения:", list(set(numbers_0)))
    print()
    # Самый дорогой товар
    dict_2 = {
        'Селедка': 125,
        'Лед на палочке': 50,
        'Жигули': 200000
    }
    max_product = max(dict_2, key=dict_2.get)
    print('Товары и цены:', dict_2)
    print(f'Самый дорогой товар: {max_product} ({dict_2[max_product]} руб.)')
    print()
    # Имена более одного раза
    names = ['Иван', 'Олег', 'Иван', 'Иван', 'Роберт', 'Лютик', 'Олег', 'Иван']
    names = Counter(names)
    print(names)
    print('Имена, встречающиеся более 1 раза')
    dig = 0
    for key, val in names.items():
        if val > dig:
            dig = val
        if val > 1:
            print(key)
    for key, val in names.items():
        if val == dig:
            print(f'Самое частое имя: {key}')
    print()
    # Словарь из строки
    stroka = input('Введите строку: ')
    dict_1 = {}
    n = -1
    for i in stroka:
        n += 1
        if i in dict_1:
            continue
        dict_1[i] = n
    print(dict_1)


# Основная программа
def main():
    tasks = {
        '1': task1,
        '2': task2,
        '3': task3,
        '4': task4,
        '5': task5
    }
    while True:
        print("\n" + "="*50)
        print("ДОСТУПНЫЕ ЗАДАНИЯ:")
        print("1 - Базовые циклы и вычисления")
        print("2 - Работа со списками")
        print("3 - Работа со словарями")
        print("4 - Работа с множествами")
        print("5 - Комбинированные задачи")
        print("0 - Выход")
        print("="*50)
        choice = input("Введите номер задания (1-5) или 0 для выхода: ")
        if choice == '0':
            print("Выход из программы...")
            break
        elif choice in tasks:
            print()
            tasks[choice]()
            input("\nНажмите Enter чтобы продолжить...")
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
