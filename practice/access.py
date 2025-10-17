def require_role(allowed_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if args[0] in allowed_roles:
                print(123)
            return func(*args)
        return wrapper
    return decorator


roles = {"Alex": "admin",
         "Ben": "manager"
         }


@require_role(roles)
def delete_database(user):
    print(f"База данных удалена пользователем {user['name']}")


delete_database("admin")
