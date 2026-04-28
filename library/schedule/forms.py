from django import forms
from .models import Teacher
from django.core.validators import MinLengthValidator, EmailValidator


class TeacherForm(forms.Form):
    """Форма для добавления преподавателя"""

    first_name = forms.CharField(
        max_length=100,
        label="Имя",
        help_text="Введите имя преподавателя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Иван',
            'id': 'first_name'
        }),
        validators=[MinLengthValidator(2, 'Имя должно содержать минимум 2 символа')]
    )

    last_name = forms.CharField(
        max_length=100,
        label="Фамилия",
        help_text="Введите фамилию преподавателя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Петров',
            'id': 'last_name'
        }),
        validators=[MinLengthValidator(2, 'Фамилия должна содержать минимум 2 символа')]
    )

    email = forms.EmailField(
        label="Email",
        help_text="Введите email преподавателя (будет использован для связи)",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ivan.petrov@example.com',
            'id': 'email'
        }),
        validators=[EmailValidator('Введите корректный email адрес')]
    )

    phone = forms.CharField(
        max_length=20,
        required=False,  # Это поле сделано необязательным
        label="Телефон",
        help_text="Введите номер телефона (необязательно)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67',
            'id': 'phone'
        })
    )

    hire_date = forms.DateField(
        label="Дата найма",
        help_text="Выберите дату начала работы",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'hire_date'
        })
    )

    bio = forms.CharField(
        required=False,
        label="Биография",
        help_text="Краткая информация о преподавателе (необязательно)",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Расскажите об образовании, опыте работы, достижениях...',
            'id': 'bio'
        })
    )

    education = forms.CharField(
        required=False,
        label="Образование",
        help_text="Введите информацию об образовании (необязательно)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'МГУ им. Ломоносова, факультет ВМиК, 2010',
            'id': 'education'
        })
    )

    experience_years = forms.IntegerField(
        required=False,
        label="Опыт работы (лет)",
        help_text="Укажите количество лет опыта",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '5',
            'id': 'experience_years',
            'min': '0'
        })
    )

    def clean_email(self):
        """Дополнительная валидация email"""
        email = self.cleaned_data.get('email')
        if Teacher.objects.filter(email=email).exists():
            raise forms.ValidationError('Преподаватель с таким email уже существует')
        return email

    def clean_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 10:
            raise forms.ValidationError('Введите корректный номер телефона (минимум 10 символов)')
        return phone


class CourseForm(forms.Form):
    """Форма для добавления курса"""

    title = forms.CharField(
        max_length=200,
        label="Название курса",
        help_text="Введите полное название курса",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например: Python для начинающих',
            'id': 'title'
        })
    )

    description = forms.CharField(
        label="Описание",
        help_text="Подробное описание курса",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Опишите содержание курса, требования, результаты обучения...',
            'id': 'description'
        })
    )

    level = forms.ChoiceField(
        choices=[
            ('beginner', 'Начальный'),
            ('intermediate', 'Средний'),
            ('advanced', 'Продвинутый'),
        ],
        label="Уровень сложности",
        help_text="Выберите уровень подготовки",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'level'
        })
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Цена (руб.)",
        help_text="Укажите стоимость курса",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '15000.00',
            'id': 'price',
            'step': '0.01',
            'min': '0'
        })
    )

    duration_weeks = forms.IntegerField(
        label="Длительность (недели)",
        help_text="Сколько недель длится курс",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '8',
            'id': 'duration_weeks',
            'min': '1'
        })
    )

    start_date = forms.DateField(
        label="Дата старта",
        help_text="Выберите дату начала курса",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'start_date'
        })
    )

    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        label="Преподаватель",
        help_text="Выберите преподавателя, который будет вести курс",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'teacher'
        }),
        empty_label="Выберите преподавателя"
    )


class StudentForm(forms.Form):
    """Форма для добавления студента"""

    first_name = forms.CharField(
        max_length=100,
        label="Имя",
        help_text="Введите имя студента",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Мария',
            'id': 'first_name'
        })
    )

    last_name = forms.CharField(
        max_length=100,
        label="Фамилия",
        help_text="Введите фамилию студента",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванова',
            'id': 'last_name'
        })
    )

    email = forms.EmailField(
        label="Email",
        help_text="Введите email студента",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'maria.ivanova@example.com',
            'id': 'email'
        })
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Телефон",
        help_text="Введите номер телефона (необязательно)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67',
            'id': 'phone'
        })
    )

    date_of_birth = forms.DateField(
        required=False,
        label="Дата рождения",
        help_text="Укажите дату рождения (необязательно)",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date_of_birth'
        })
    )
