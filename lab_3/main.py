from decimal import Decimal
from fractions import Fraction
from datetime import datetime, date
import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


# Собственный генератор
class Countdown:
    def __init__(self, n):
        self.n = n
        self.final_number = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n > self.final_number:
            result = self.n
            self.n -= 1
            return result
        else:
            raise StopIteration


def fibonacci(n):
    a, b = 0, 1
    for __ in range(n):
        yield a
        a, b = b, a + b


def calc_finance(P, r, t):
    # getcontext().prec = 10
    P = Decimal(P)
    r = Decimal(r)
    t = Decimal(t)
    S = P * (1 + r/(100 * 12))**(12*t)
    F = S - P
    return float(S), float(F)


def task_1():
    print("=== ЗАДАНИЕ 1 ===")
    # Простое преобразование
    print('Простое преобразование')
    print([i**2 for i in range(1, 11)])


def task_2():
    print("=== ЗАДАНИЕ 2 ===")
    # Фильтрация
    print('Фильтрация')
    print([i for i in range(1, 21) if i % 2 == 0])


def task_3():
    print("=== ЗАДАНИЕ 3 ===")
    # Работа со строками
    print('Работа со строками')
    words = ['python', 'Java', 'C++', 'Rust', 'go']
    print([i.upper() for i in words if len(i) > 3])


def task_4():
    print("=== ЗАДАНИЕ 4 ===")
    # Собственный итератор
    print('Собственный итератор')
    for i in Countdown(5):
        print(i)


def task_5():
    print("=== ЗАДАНИЕ 5 ===")
    # Собственный генератор
    print('Собственный генератор')
    for i in fibonacci(5):
        print(i)


def task_6():
    print("=== ЗАДАНИЕ 6 ===")
    # Точные вычисления
    print('Точные вычисления')
    total, interest = calc_finance(1000, 5, 2)
    print(round(total, 2), round(interest, 2))


def task_7():
    print("=== ЗАДАНИЕ 7 ===")
    # Рациональьные дроби
    print('Рациональные дроби')
    a = Fraction(3, 4)  # 3/4
    b = Fraction(5, 6)  # 5/6
    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)


def task_8():
    print("=== ЗАДАНИЕ 8 ===")
    # Текущая дата и время
    print('Текущая дата и время')
    datetime_1 = str(datetime.now())
    dat, tim = datetime_1.split()
    print(datetime.now())
    print(dat)
    print(tim)


def task_9():
    print("=== ЗАДАНИЕ 9 ===")
    # Разница дат
    print('Разница дат')
    birth = date(2006, 3, 5)
    today = date.today()
    print(today - birth)
    next_birthday = date(today.year, birth.month, birth.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, birth.month, birth.day)
    print((next_birthday - today).days)


def task_10():
    print("=== ЗАДАНИЕ 10 ===")
    # Форматирование строк
    print('Форматирование строк')

    def form_str(dtm):
        formatted = dtm.strftime("Сегодня %d %B %Y года, время %H:%M:%S")
        return formatted
    print(form_str(datetime.now()))


def main():
    while True:
        print("\n" + "="*50)
        print("ДОСТУПНЫЕ ЗАДАНИЯ:")
        print("1 - Простое преобразование")
        print("2 - Фильтрация")
        print("3 - Работа со строками")
        print("4 - Собственный итератор")
        print("5 - Собственный генератор")
        print("6 - Точные вычисления")
        print("7 - Рациональные дроби")
        print("8 - Текущая дата и время")
        print("9 - Разница дат")
        print("10 - Форматирование строк")
        print("0 - Выход")
        print("="*50)
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
