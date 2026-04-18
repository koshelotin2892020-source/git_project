from django.contrib import admin
from .models import Teacher, TeacherInfo, Course, Student

class TeacherInfoInline(admin.StackedInline):
    model = TeacherInfo
    can_delete = False

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'is_active']
    list_filter = ['is_active', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [TeacherInfoInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'price', 'teacher', 'start_date']
    list_filter = ['level', 'teacher']
    search_fields = ['title']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'registration_date']
    search_fields = ['first_name', 'last_name', 'email']
    filter_horizontal = ['courses']