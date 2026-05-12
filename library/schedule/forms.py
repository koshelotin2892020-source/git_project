from django import forms
from .models import Teacher, Student, Course


class TeacherForm(forms.ModelForm):

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'phone', 'hire_date',
                  'login', 'password', 'rating', 'position', 'work_years',
                  'bio', 'education', 'languages']  # Добавлены поля
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
            'bio': forms.Textarea(attrs={'rows': 4}),  # Для биографии текстовое поле
        }

    def clean_first_name(self):
        return self.cleaned_data.get('first_name', '').strip().capitalize()

    def clean_last_name(self):
        return self.cleaned_data.get('last_name', '').strip().capitalize()

    def clean(self):
        cleaned_data = super().clean()
        # Автоматически ставим должность по стажу
        work_years = cleaned_data.get('work_years', 0)
        if work_years < 1:
            cleaned_data['position'] = 'jun'
        elif work_years < 3:
            cleaned_data['position'] = 'mid'
        else:
            cleaned_data['position'] = 'sen'
        return cleaned_data


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 
                  'login', 'password', 'student_card', 'average_grade']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
        }

    def clean_first_name(self):
        return self.cleaned_data.get('first_name', '').strip().capitalize()

    def clean_last_name(self):
        return self.cleaned_data.get('last_name', '').strip().capitalize()

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('student_card'):
            import random
            cleaned_data['student_card'] = f"STU-{random.randint(1000000, 9999999)}"
        return cleaned_data


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price', 'duration_weeks', 'start_date',
                  'teacher', 'max_students', 'is_published']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_title(self):
        return self.cleaned_data.get('title', '').strip().capitalize()
