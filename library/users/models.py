from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""
    
    # Дополнительные поля
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    
    # Роли пользователей
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Роль")
    
    def __str__(self):
        return self.username
