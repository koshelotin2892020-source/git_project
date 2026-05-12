from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации с дополнительными полями"""
    
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Имя")
    last_name = forms.CharField(required=True, label="Фамилия")
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')
        labels = {
            'username': 'Логин',
            'role': 'Роль',
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email
