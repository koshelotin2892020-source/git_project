from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


class Teacher(models.Model):
    """Основная информация о преподавателе"""

    # Существующие поля
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    hire_date = models.DateField(verbose_name="Дата найма")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # НОВЫЕ ПОЛЯ (4-5 штук)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)],
        verbose_name="Рейтинг преподавателя",
        help_text="Рейтинг от 0 до 5"
    )

    position = models.CharField(
        max_length=100,
        choices=[
            ('junior', 'Младший преподаватель'),
            ('middle', 'Преподаватель'),
            ('senior', 'Старший преподаватель'),
            ('professor', 'Профессор'),
        ],
        default='middle',
        verbose_name="Должность"
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        verbose_name="Зарплата"
    )

    telegram = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^@[\w_]{5,32}$',
                message='Telegram должен начинаться с @ и содержать 5-32 символов'
            )
        ],
        verbose_name="Telegram"
    )

    work_experience = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        verbose_name="Стаж работы (лет)"
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['last_name', 'first_name']
        # Исправленный CheckConstraint (используем 'condition' вместо 'check')
        constraints = [
            models.CheckConstraint(
                condition=models.Q(work_experience__gte=0),
                name='work_experience_positive'
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TeacherInfo(models.Model):
    """Расширенная информация о преподавателе (связь 1:1)"""

    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name="Преподаватель"
    )
    bio = models.TextField(blank=True, verbose_name="Биография")
    education = models.CharField(max_length=255, blank=True, verbose_name="Образование")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Лет опыта")
    office_number = models.CharField(max_length=10, blank=True, verbose_name="Кабинет")
    github_link = models.URLField(blank=True, unique=True, null=True, verbose_name="GitHub")

    # НОВЫЕ ПОЛЯ
    certifications = models.TextField(
        blank=True,
        verbose_name="Сертификаты",
        help_text="Список сертификатов через запятую"
    )

    languages = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Языки",
        help_text="Какими языками владеет (через запятую)"
    )

    def __str__(self):
        return f"Профиль: {self.teacher}"

    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


class Course(models.Model):
    """Курс, который ведет преподаватель"""

    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name="Уровень")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration_weeks = models.PositiveIntegerField(verbose_name="Длительность (недели)")
    start_date = models.DateField(verbose_name="Дата старта")
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name="Преподаватель"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # НОВЫЕ ПОЛЯ
    max_students = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        verbose_name="Максимум студентов"
    )

    prerequisites = models.TextField(
        blank=True,
        verbose_name="Требования к студентам",
        help_text="Какие знания необходимы для прохождения курса"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликован"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        unique_together = ['title', 'teacher']

    def __str__(self):
        return self.title


class Student(models.Model):
    """Студент, который может записываться на курсы"""

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    courses = models.ManyToManyField(Course, related_name='students', blank=True, verbose_name="Курсы")
    registration_date = models.DateTimeField(auto_now_add=True)

    # НОВЫЕ ПОЛЯ
    student_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Номер студенческого билета"
    )

    average_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Средний балл"
    )

    parent_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон родителя"
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Город"
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
