from django.db import models


# 1. Модель Teacher и TeacherInfo (Связь 1:1)
class Teacher(models.Model):
    """Основная информация о преподавателе"""
    # Строковые поля
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True,
                             verbose_name="Телефон")
    hire_date = models.DateField(verbose_name="Дата найма")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['last_name', 'first_name']


class TeacherInfo(models.Model):
    """Расширенная информация о преподавателе (связь 1:1)"""
    # Связь 1:1 с преподавателем.
    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,
        related_name='info',
        verbose_name="Преподаватель"
    )
    bio = models.TextField(blank=True, verbose_name="Биография")
    education = models.CharField(max_length=255, blank=True,
                                 verbose_name="Образование")
    experience_years = models.PositiveIntegerField(default=0,
                                                   verbose_name="Лет опыта")
    office_number = models.CharField(max_length=10, blank=True,
                                     verbose_name="Кабинет")

    # Дополнительное поле с ограничением повторных записей (unique=True)
    github_link = models.URLField(blank=True, unique=True, null=True,
                                  verbose_name="GitHub")

    def __str__(self):
        return f"Профиль: {self.teacher}"

    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


# 2. Модель Course (Связь 1:N с Teacher)
class Course(models.Model):
    """Курс, который ведет преподаватель"""
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES,
                             default='beginner', verbose_name="Уровень")
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name="Цена")
    duration_weeks = models.PositiveIntegerField(verbose_name="Длительность (недели)")
    start_date = models.DateField(verbose_name="Дата старта")

    # Связь 1:N с преподавателем.
    # on_delete=SET_NULL
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='courses',
        verbose_name="Преподаватель"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        unique_together = ['title', 'teacher']


# 3. Модель Student и связь N:N с Course
class Student(models.Model):
    """Студент, который может записываться на курсы"""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    date_of_birth = models.DateField(null=True, blank=True,
                                     verbose_name="Дата рождения")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    # Связь N:N с курсами.
    courses = models.ManyToManyField(
        Course,
        related_name='students',
        blank=True,
        verbose_name="Курсы"
    )

    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']
