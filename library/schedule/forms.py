from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
import re
from .models import Teacher, TeacherInfo, Course, Student


# ========== КАСТОМНЫЕ ВАЛИДАТОРЫ ==========

def validate_phone_number(value):
    """Кастомный валидатор для номера телефона"""
    if value:
        # Удаляем все нецифровые символы
        phone_digits = re.sub(r'\D', '', value)
        if len(phone_digits) < 10 or len(phone_digits) > 15:
            raise ValidationError(
                'Номер телефона должен содержать от 10 до 15 цифр',
                code='invalid_phone'
            )


def validate_future_date(value):
    """Кастомный валидатор для даты в будущем"""
    if value and value > date.today():
        raise ValidationError(
            'Дата не может быть в будущем',
            code='future_date'
        )


def validate_name_capitalized(value):
    """Кастомный валидатор - имя должно начинаться с заглавной буквы"""
    if value and not value[0].isupper():
        raise ValidationError(
            'Имя/Фамилия должны начинаться с заглавной буквы',
            code='not_capitalized'
        )


# ========== MODELFORM ДЛЯ TEACHER ==========

class TeacherForm(forms.ModelForm):
    """ModelForm для преподавателя"""
    
    # Дополнительное поле для профиля (не из модели Teacher)
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        label='Биография',
        help_text='Краткая информация о преподавателе'
    )
    
    education = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Образование',
        help_text='Введите информацию об образовании'
    )
    
    experience_years = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=60,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Опыт работы (лет)'
    )
    
    class Meta:
        model = Teacher
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'hire_date', 'position', 'rating', 'salary',
            'telegram', 'work_experience'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иван'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Петров'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ivan@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '5'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'telegram': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'work_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '60'
            }),
        }
        help_texts = {
            'telegram': 'Введите Telegram username, начиная с @',
            'rating': 'Рейтинг от 0 до 5',
            'work_experience': 'Общий стаж работы в годах',
        }
    
    # ========== МЕТОДЫ clean_ ДЛЯ ПОЛЕЙ ==========
    
    def clean_first_name(self):
        """Валидация имени"""
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            # Проверка на заглавную букву
            if not first_name[0].isupper():
                raise ValidationError('Имя должно начинаться с заглавной буквы')
            # Проверка на минимальную длину
            if len(first_name) < 2:
                raise ValidationError('Имя должно содержать минимум 2 символа')
            # Проверка только на буквы
            if not first_name.isalpha():
                raise ValidationError('Имя должно содержать только буквы')
        return first_name
    
    def clean_last_name(self):
        """Валидация фамилии"""
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            if not last_name[0].isupper():
                raise ValidationError('Фамилия должна начинаться с заглавной буквы')
            if len(last_name) < 2:
                raise ValidationError('Фамилия должна содержать минимум 2 символа')
            if not last_name.isalpha():
                raise ValidationError('Фамилия должна содержать только буквы')
        return last_name
    
    def clean_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Используем кастомный валидатор
            validate_phone_number(phone)
        return phone
    
    def clean_hire_date(self):
        """Валидация даты найма"""
        hire_date = self.cleaned_data.get('hire_date')
        if hire_date:
            # Дата не может быть в будущем
            if hire_date > date.today():
                raise ValidationError('Дата найма не может быть в будущем')
            # Дата не может быть слишком старой (раньше 1970 года)
            if hire_date.year < 1970:
                raise ValidationError('Дата найма не может быть раньше 1970 года')
        return hire_date
    
    # ========== МЕТОД clean() ДЛЯ ФОРМЫ ==========
    
    def clean(self):
        """Глобальная валидация формы преподавателя"""
        cleaned_data = super().clean()
        
        # Получаем значения полей
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        work_experience = cleaned_data.get('work_experience')
        position = cleaned_data.get('position')
        rating = cleaned_data.get('rating')
        
        # Валидация 1: Проверка на существование email
        if email:
            # Исключаем текущего преподавателя при обновлении
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                if Teacher.objects.filter(email=email).exclude(pk=instance.pk).exists():
                    raise ValidationError('Преподаватель с таким email уже существует')
            else:
                if Teacher.objects.filter(email=email).exists():
                    raise ValidationError('Преподаватель с таким email уже существует')
        
        # Валидация 2: Соответствие должности и стажа
        if work_experience and position:
            if position == 'junior' and work_experience > 2:
                raise ValidationError(
                    'Младший преподаватель не может иметь стаж более 2 лет. '
                    'Повысьте должность или уменьшите стаж.'
                )
            if position == 'professor' and work_experience < 10:
                raise ValidationError(
                    'Для должности профессора необходим стаж не менее 10 лет.'
                )
        
        # Валидация 3: Соответствие рейтинга и должности
        if rating and position:
            if position == 'professor' and rating < 4.0:
                raise ValidationError(
                    'Рейтинг профессора должен быть не ниже 4.0'
                )
            if position == 'senior' and rating < 3.0:
                raise ValidationError(
                    'Рейтинг старшего преподавателя должен быть не ниже 3.0'
                )
        
        return cleaned_data


# ========== MODELFORM ДЛЯ COURSE ==========

class CourseForm(forms.ModelForm):
    """ModelForm для курса"""
    
    class Meta:
        model = Course
        fields = [
            'title', 'description', 'level', 'price',
            'duration_weeks', 'start_date', 'teacher',
            'max_students', 'prerequisites', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Python для начинающих'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Подробное описание курса...'
            }),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'duration_weeks': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '52'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '200'
            }),
            'prerequisites': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Какие знания необходимы для прохождения курса...'
            }),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Название курса',
            'description': 'Описание',
            'level': 'Уровень сложности',
            'price': 'Цена (руб.)',
            'duration_weeks': 'Длительность (недели)',
            'start_date': 'Дата старта',
            'teacher': 'Преподаватель',
            'max_students': 'Максимум студентов',
            'prerequisites': 'Требования',
            'is_published': 'Опубликовать курс',
        }
    
    # ========== МЕТОДЫ clean_ ДЛЯ ПОЛЕЙ ==========
    
    def clean_title(self):
        """Валидация названия курса"""
        title = self.cleaned_data.get('title')
        if title:
            if len(title) < 5:
                raise ValidationError('Название курса должно содержать минимум 5 символов')
            if not title[0].isupper():
                raise ValidationError('Название курса должно начинаться с заглавной буквы')
        return title
    
    def clean_price(self):
        """Валидация цены"""
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        if price and price > 1000000:
            raise ValidationError('Цена не может превышать 1 000 000 рублей')
        return price
    
    def clean_start_date(self):
        """Валидация даты старта"""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date < date.today():
            raise ValidationError('Дата старта не может быть в прошлом')
        return start_date
    
    # ========== МЕТОД clean() ДЛЯ ФОРМЫ ==========
    
    def clean(self):
        """Глобальная валидация формы курса"""
        cleaned_data = super().clean()
        
        start_date = cleaned_data.get('start_date')
        duration_weeks = cleaned_data.get('duration_weeks')
        max_students = cleaned_data.get('max_students')
        price = cleaned_data.get('price')
        
        # Валидация 1: Проверка уникальности пары (title, teacher)
        title = cleaned_data.get('title')
        teacher = cleaned_data.get('teacher')
        
        if title and teacher:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                if Course.objects.filter(title=title, teacher=teacher).exclude(pk=instance.pk).exists():
                    raise ValidationError(
                        f'Курс с названием "{title}" уже существует у этого преподавателя'
                    )
            else:
                if Course.objects.filter(title=title, teacher=teacher).exists():
                    raise ValidationError(
                        f'Курс с названием "{title}" уже существует у этого преподавателя'
                    )
        
        # Валидация 2: Логика цены и длительности
        if price and duration_weeks:
            price_per_week = price / duration_weeks
            if price_per_week < 500:
                raise ValidationError(
                    f'Слишком низкая цена ({price_per_week:.0f} руб./неделя). '
                    'Минимальная цена за неделю - 500 рублей.'
                )
        
        # Валидация 3: Логика даты старта и максимального количества студентов
        if start_date and max_students:
            days_until_start = (start_date - date.today()).days
            if days_until_start < 30 and max_students > 50:
                raise ValidationError(
                    'При старте курса менее чем через месяц количество мест не может превышать 50'
                )
        
        return cleaned_data


# ========== MODELFORM ДЛЯ STUDENT ==========

class StudentForm(forms.ModelForm):
    """ModelForm для студента"""
    
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'student_id', 'average_grade',
            'parent_phone', 'city', 'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Мария'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Иванова'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'maria@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'STU-2024-001'
            }),
            'average_grade': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 987-65-43'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Москва'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    # ========== МЕТОДЫ clean_ ДЛЯ ПОЛЕЙ ==========
    
    def clean_student_id(self):
        """Валидация номера студенческого билета"""
        student_id = self.cleaned_data.get('student_id')
        if student_id:
            # Проверка формата: STU-ГГГГ-XXX
            import re
            pattern = r'^STU-\d{4}-\d{3}$'
            if not re.match(pattern, student_id):
                raise ValidationError(
                    'Номер студенческого должен быть в формате: STU-2024-001 '
                    '(год и трехзначный номер)'
                )
        return student_id
    
    def clean_date_of_birth(self):
        """Валидация даты рождения"""
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            age = date.today().year - date_of_birth.year
            if age < 16:
                raise ValidationError('Студент должен быть не младше 16 лет')
            if age > 100:
                raise ValidationError('Проверьте дату рождения')
        return date_of_birth
    
    def clean_average_grade(self):
        """Валидация среднего балла"""
        grade = self.cleaned_data.get('average_grade')
        if grade and (grade < 0 or grade > 100):
            raise ValidationError('Средний балл должен быть от 0 до 100')
        return grade
    
    # ========== МЕТОД clean() ДЛЯ ФОРМЫ ==========
    
    def clean(self):
        """Глобальная валидация формы студента"""
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        student_id = cleaned_data.get('student_id')
        phone = cleaned_data.get('phone')
        parent_phone = cleaned_data.get('parent_phone')
        average_grade = cleaned_data.get('average_grade')
        
        # Валидация 1: Проверка уникальности email
        if email:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                if Student.objects.filter(email=email).exclude(pk=instance.pk).exists():
                    raise ValidationError('Студент с таким email уже существует')
            else:
                if Student.objects.filter(email=email).exists():
                    raise ValidationError('Студент с таким email уже существует')
        
        # Валидация 2: Номер студенческого должен быть уникальным
        if student_id:
            instance = getattr(self, 'instance', None)
            if instance and instance.pk:
                if Student.objects.filter(student_id=student_id).exclude(pk=instance.pk).exists():
                    raise ValidationError('Студент с таким номером уже существует')
            else:
                if Student.objects.filter(student_id=student_id).exists():
                    raise ValidationError('Студент с таким номером уже существует')
        
        # Валидация 3: Телефоны не должны совпадать
        if phone and parent_phone and phone == parent_phone:
            raise ValidationError('Телефон студента и телефон родителя не могут совпадать')
        
        # Валидация 4: Логика среднего балла
        if average_grade and average_grade < 60:
            cleaned_data['needs_support'] = True
            self.add_error('average_grade', 
                'Внимание: низкий средний балл. Рекомендуется дополнительная поддержка.')
        
        return cleaned_data