from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Инициализация логирования и подключение сигналов при старте Django."""
        from .logging_config import setup_logging
        setup_logging()

        # Подключаем сигналы аутентификации (login / logout / login_failed)
        import users.signals  # noqa: F401
