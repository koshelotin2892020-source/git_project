# schedule/validators.py
import re
from django.core.exceptions import ValidationError


def validate_login(login):
    """Валидатор: логин учителя/студента"""
    pattern = r'^[a-zA-Z][0-9a-zA-Z_]{3,18}[0-9a-zA-Z]$'
    if not re.match(pattern, login):
        raise ValidationError(
            'Логин должен начинаться с буквы, содержать 5-20 символов '
            '(буквы, цифры, подчеркивание) и заканчиваться буквой или цифрой'
        )


def validate_password(password):
    """Валидатор: надежный пароль"""
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$'
    if not re.match(pattern, password):
        raise ValidationError(
            'Пароль должен содержать минимум 8 символов: '
            'заглавные и строчные буквы, цифры и спецсимволы (!@#$%^&*)'
        )


def validate_email_domain(email):
    """Валидатор: email только разрешенных доменов"""
    domains = [r'gmail\.com$', r'yandex\.ru$', r'edu\.ru$']
    for dom in domains:
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*\@' + dom
        if re.match(pattern, email):
            return email
    raise ValidationError('Email должен быть на доменах: gmail.com, yandex.ru, edu.ru')


def validate_phone_number(phone):
    """Валидатор: российский номер телефона"""
    # Очищаем от лишних символов
    cleaned = re.sub(r'\-|\s|[()]', '', phone)
    pattern = r'^\+?[78]\d{10}$'
    if not re.match(pattern, cleaned):
        raise ValidationError(
            'Введите корректный российский номер телефона '
            '(например: +7 952 603-02-10 или 89526030210)'
        )
    return cleaned  # возвращаем очищенный номер


def validate_date_format(date_str):
    """Валидатор: дата в разных форматах"""
    patterns = [
        r'\d{1,2}.\d{1,2}.\d{2,4}',
        r'\d{1,2}-\d{1,2}-\d{2,4}',
        r'\d{1,2}/\d{1,2}/\d{2,4}'
    ]
    for pattern in patterns:
        if re.match(pattern, str(date_str)):
            return True
    raise ValidationError('Дата должна быть в формате: ДД.ММ.ГГГГ или ДД-ММ-ГГГГ')
