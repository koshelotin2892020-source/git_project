import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

logger = logging.getLogger(__name__)  # 'users.signals'


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    """Успешный вход → INFO."""
    ip = _get_client_ip(request)
    logger.info(
        "User logged in: username='%s', email='%s', ip='%s'",
        user.username,
        user.email,
        ip,
    )


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    """Неудачный вход → WARNING."""
    ip = _get_client_ip(request)
    attempted_username = credentials.get('username', '<unknown>')
    logger.warning(
        "Failed login attempt for username='%s', ip='%s'",
        attempted_username,
        ip,
    )


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    """Выход из системы → INFO."""
    username = user.username if user else '<anonymous>'
    ip = _get_client_ip(request)
    logger.info(
        "User logged out: username='%s', ip='%s'",
        username,
        ip,
    )


def _get_client_ip(request) -> str:
    """Извлекает IP клиента с учётом прокси."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')
