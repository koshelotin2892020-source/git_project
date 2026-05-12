from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import (
    validate_login, validate_password, validate_email_domain,
    validate_phone_number, validate_date_format
)


class Student(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия"
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email_domain],
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
        verbose_name="Телефон"
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    courses = models.ManyToManyField(
        'Course',
        related_name='students',
        blank=True,
        verbose_name="Курсы"
    )

    login = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_login],
        verbose_name="Логин"
    )
    password = models.CharField(
        max_length=128,
        validators=[validate_password],
        verbose_name="Пароль"
    )
    student_card = models.CharField(
        max_length=7,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер студенческого"
    )
    average_grade = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=2.00,
        validators=[MinValueValidator(2.00), MaxValueValidator(5.00)],
        verbose_name="Средний балл"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(
        unique=True,
        validators=[validate_email_domain],
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[validate_phone_number],
        verbose_name="Телефон"
    )
    hire_date = models.DateField(verbose_name="Дата найма")

    login = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_login],
        verbose_name="Логин"
    )
    password = models.CharField(
        max_length=128,
        validators=[validate_password],
        verbose_name="Пароль"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name="Рейтинг"
    )
    position = models.CharField(
        max_length=50,
        choices=[
            ('jun', 'Junior'),
            ('mid', 'Middle'),
            ('sen', 'Senior')
        ], 
        default='mid',
        verbose_name="Должность"
    )
    work_years = models.PositiveIntegerField(
        default=0,
        verbose_name="Стаж работы (лет)"
    )

    bio = models.TextField(blank=True, verbose_name="Биография")
    education = models.CharField(max_length=255, blank=True, verbose_name="Образование")
    languages = models.CharField(max_length=200, blank=True, verbose_name="Языки")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена"
    )
    duration_weeks = models.PositiveIntegerField(verbose_name="Длительность (недели)")
    start_date = models.DateField(
        validators=[validate_date_format],
        verbose_name="Дата старта"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name="Преподаватель"
    )
    max_students = models.PositiveIntegerField(
        default=30,
        verbose_name="Максимум студентов"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликован"
    )

    def __str__(self):
        return self.title
