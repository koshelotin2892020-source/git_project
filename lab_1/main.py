import re
import pandas as pd


def task_1():
    print("=== ЗАДАНИЕ 1 ===")
    # Проверка числа на четность
    print('Проверка числа на четность')
    a = int(input("Введите число: "))
    if a % 2 == 0:
        print("Число четное")
    else:
        print("Число нечетное")
    # Проверка числа на деление с остатком на 5
    if a % 5 == 0:
        print("Число делится на 5 без остатка")
    else:
        print("Число делится на 5 с остатком")
    # Проверка числа на деление с остатком на 5
    if a % 7 == 0:
        print("Число делится на 7 без остатка")
    else:
        print("Число делится на 7 с остатком")
    # Проверка: окончивается число на 3 или нет
    if a % 10 == 3:
        print("Число оканчивается на 3")
    else:
        print("Число не оканчивается на 3")


def task_2():
    print("=== ЗАДАНИЕ 2 ===")
    # Сравнение двух чисел
    print('Сравнение двух чисел')
    a, b = map(int, input("Введите два числа через пробел: ").split())
    if a > b:
        print(f"Большее число {a}")
        print(f"Меньшее число {b}")
        print("Не равны")
    elif a < b:
        print(f"Большее число {b}")
        print(f"Меньшее число {a}")
        print("Не равны")
    else:
        print("Равны")
    print('Разность = ', abs(a-b))


def task_3():
    print("=== ЗАДАНИЕ 3 ===")
    print('Таблица умножения числа')
    digit = int(input("Введите число для таблицы умножения: "))
    # Таблица умножения на 2
    table_to_2 = pd.DataFrame(
        [i * 2 for i in range(1, 11)],
        index=range(1, 11),
        columns=[2]
    )
    print('Таблица умножения на 2\n', table_to_2.T)
    # Таблица умножения на число, введенное пользователем
    table_to_digit = pd.DataFrame(
        [i * digit for i in range(1, 11)],
        index=range(1, 11),
        columns=[digit]
    )
    print(f'Таблица умножения на число, введенное пользователем ({digit})',
          '\n', table_to_digit.T)
    # Таблица умножения на 5
    table_to_5 = pd.DataFrame(
        [i * 5 for i in range(1, 11)],
        index=range(1, 11),
        columns=[5]
    )
    print('Таблица умножения на 5\n', table_to_5.T)
    # Таблица умножения на 10
    table_to_10 = pd.DataFrame(
        [i * 10 for i in range(1, 11)],
        index=range(1, 11),
        columns=[10]
    )
    print('Таблица умножения на 10\n', table_to_10.T)


def task_4():
    print("=== ЗАДАНИЕ 4 ===")
    # Сумма чисел в диапазоне
    print('Сумма чисел в диапазоне')
    digit = int(input('Введите число: '))
    s_10 = 0
    for i in range(11):
        s_10 += i
    print(s_10)
    # Количество чисел, сумма четных и нечетных чисел
    s_n = 0
    s_2 = 0
    s_1 = 0
    for i in range(digit + 1):
        s_n += i
        if i % 2 == 0:
            s_2 += i
        if i % 2 != 0:
            s_1 += i
    print(s_n)
    print(s_2)
    print(s_1)


def task_5():
    print("=== ЗАДАНИЕ 5 ===")
    # Возведение в степень
    print('Возведение в степень')
    digit = int(input('Введите число: '))
    stepen = int(input('Введите степень: '))
    print(digit**2)
    print(digit**3)
    print(digit**stepen)
    print(2**stepen)


def task_6():
    print("=== ЗАДАНИЕ 6 ===")
    # Проверка возраста
    print('Проверка возраста')
    age = int(input('Введите возраст: '))
    if age > 0:
        if age % 10 == 0:
            print('Возраст круглый десяток')
        if age <= 18 and age >= 7:
            print('Возраст школьный')
        if 65 > age >= 18:
            print('Совершеннолетний')
        if age >= 65:
            print('Пенсионный')
    else:
        print('Возраст меньше 0')


def task_7():
    print("=== ЗАДАНИЕ 7 ===")
    # Факториал числа
    print('Факториал числа')
    f_3 = 1
    for i in range(1, 4):
        f_3 *= i
    print("Факториал 3 = ", f_3)
    f_5 = 1
    for i in range(1, 6):
        f_5 *= i
    print("Факториал 5 = ", f_5)
    while True:
        digit = int(input('Введите число: '))
        if digit == 0:
            print("Факториал 0 = 1")
            break
        f_n = 1
        for i in range(1, digit + 1):
            f_n *= i
        print(f"Факториал числа, введенного пользователем ({digit}) = ", f_n)


def task_8():
    print("=== ЗАДАНИЕ 8 ===")
    # Работа с цифрами числа
    print('Работа с цифрами числа')
    s = 0
    pr = 1
    digit_2 = input('Введите двузначное число: ')
    if re.search(r"^[1-9][0-9]$", digit_2):
        for i in digit_2:
            s += int(i)
            pr *= int(i)
        print("Сумма цифр = ", s)
        print("Произведение цифр = ", pr)
    else:
        print('Введено не правильное число')
    s = 0
    digit_3 = input('Введите трехзначное число: ')
    if re.search(r"^[1-9][0-9][0-9]$", digit_3):
        for i in digit_3:
            s += int(i)
        print("Сумма цифр = ", s)
        print('Первая: ' + digit_3[0])
        print('Последняя: ' + digit_3[-1])
    else:
        print('Введено не правильное число')


def task_9():
    print("=== ЗАДАНИЕ 9 ===")
    # Проверка символа
    print('Проверка символа')
    a = input('Введите символ: ')
    if re.search('^[0-9]$', a):
        print('Символ является цифрой')
    if re.search('^[a-zA-z]$', a):
        print('Символ является буквой')
        if re.search('^[A-Z]$', a):
            print('Буква является прописной')
        if re.search('^[aeiouAEIOU]$', a):
            print('Буква является гласной')


def task_10():
    print("=== ЗАДАНИЕ 10 ===")
    # Циклы с условием
    print('Циклы с условием')
    s = 0
    print('Введите "0", чтобы выйти из цикла')
    while True:
        digit = input('Введите число: ')
        if digit == '0':
            print(f'Цикл закончен, сумма {s}')
            break
        s += int(digit)
    c = 0
    print("*"*20)
    print('Введите отрицательное число, чтобы выйти из цикла')
    while True:
        digit = input('Введите число: ')
        if int(digit) < 0:
            print(f'Цикл закончен, количество = {c}')
            break
        c += 1
    s = 0
    print("*"*20)
    print('Введите четное число, чтобы выйти из цикла')
    while True:
        digit = input('Введите число: ')
        if int(digit) % 2 == 0:
            print(f'Цикл закончен, сумма {s}')
            break
        s += int(digit)
    s = 0
    c = 0
    print("*"*20)
    print('Введите число больше 100, чтобы выйти из цикла')
    while True:
        a = input('Введите число: ')
        if int(a) > 100:
            s_a = s / c
            print(f'Цикл закончен, среднее арифметическое {s_a}')
            break
        c += 1
        s += int(a)


def main():
    while True:
        print("\nВыберите номер задания (1-10), или 0 для выхода:")
        num = input("Введите номер задания: ")
        if num == '0':
            print("Выход из программы.")
            break
        elif num == '1':
            task_1()
        elif num == '2':
            task_2()
        elif num == '3':
            task_3()
        elif num == '4':
            task_4()
        elif num == '5':
            task_5()
        elif num == '6':
            task_6()
        elif num == '7':
            task_7()
        elif num == '8':
            task_8()
        elif num == '9':
            task_9()
        elif num == '10':
            task_10()
        else:
            print("Нет такого задания. Попробуйте снова.")


if __name__ == "__main__":
    main()
