from django.contrib import admin
from .models import Teacher, Course, Student


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'position']
    list_filter = ['position']
    search_fields = ['first_name', 'last_name', 'email', 'login']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'duration_weeks', 'start_date', 'teacher']
    list_filter = ['is_published']
    list_editable = ['price']
    search_fields = ['title', 'teacher__first_name', 'teacher__last_name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'average_grade']
    search_fields = ['first_name', 'last_name', 'email', 'login']
    filter_horizontal = ['courses']
