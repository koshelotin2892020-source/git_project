def logger(func):
    def wrapper(*args, **kwargs):
        if kwargs:
            print(f"Вызов функции {func.__name__} с аргументами {args} и {kwargs}")
        else:
            print(f"Вызов функции {func.__name__} с аргументами {args}")
        result = func(*args)
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper


def require_role(allowed_roles):
    def decorator(func):
        def wrapper(*args):
            if args[0] in users:
                if users[args[0]] in allowed_roles:
                    return func(args[0])
                else:
                    print(f"Доступ запрещён пользователю {args[0]}")
            else:
                print(f"{args[0]} нету в users")
        return wrapper
    return decorator


roles = ["admin"]

users = {
    "Alex": "admin",
    "Ben": "manager"
         }


@logger
def add(a, b):
    try:
        return a + b
    except TypeError:
        print("ОШИБКА - Надо ввести два числа")


@logger
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Ошибка деления на 0")


@logger
def greet(name):
    print(f"Hello, {name}")


print("*"*20)
add(2, 10)
print("*"*20)
divide(12, 0)
print("*"*20)
divide(12, 2)
print("*"*20)
greet("Alex")

@logger
@require_role(roles)
@logger
def delete_database(user):
    print(f"База данных удалена пользователем {user}")


print("*"*20)
delete_database("Ben")
