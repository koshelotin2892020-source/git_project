def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper


# def require_role(allowed_roles):
#     def wrapper():


@logger
def add(a, b):
    try:
        return a + b
    except:
        print("Надо ввести два числа")


@logger
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Ошибка деления на 0")
    except:
        print("Неизвестная ошибка")


@logger
def greet(name):
    print(f"Hello, {name}")


c = add(2, 10)
# print(c)
divide(12, 0)
d = divide(12, 2)
print(d)
greet("Alex")
