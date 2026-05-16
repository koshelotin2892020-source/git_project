from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    # Обязательные поля (email уже есть в AbstractUser, делаем его уникальным)
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    bio = models.TextField(blank=True, verbose_name="О себе")

    # Роли пользователей
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Роль")

    # Друзья (симметричная связь)
    friends = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True,
        verbose_name="Друзья",
    )

    # Входящие заявки в друзья (несимметричная — храним только «ожидающие»)
    friend_requests = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='pending_requests',
        verbose_name="Заявки в друзья",
    )

    def is_friend(self, user):
        return self.friends.filter(pk=user.pk).exists()

    def has_sent_request(self, user):
        return self.friend_requests.filter(pk=user.pk).exists()

    def __str__(self):
        return self.username
