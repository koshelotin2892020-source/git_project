from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с дополнительными полями"""

    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    phone = forms.CharField(required=False, label="Номер телефона", max_length=20)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', 'role')
        labels = {
            'username': 'Логин',
            'role': 'Роль',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone', 'birth_date', 'bio', 'avatar')
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'phone': 'Телефон',
            'birth_date': 'Дата рождения',
            'bio': 'О себе',
            'avatar': 'Аватар',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

