from django.urls import path
from . import views

app_name = 'schedule'  # Пространство имен для маршрутов

urlpatterns = [
    # Главная страница приложения schedule
    path('', views.index, name='index'),
    path('info/', views.info_page, name='info'),

    # Маршруты для преподавателей (Teachers)
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_detail,
         name='teacher_detail'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/<int:teacher_id>/update/', views.teacher_update,
         name='teacher_update'),
    path('teachers/<int:teacher_id>/delete/', views.teacher_delete,
         name='teacher_delete'),

    # Маршруты для курсов (Courses)
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/update/', views.course_update,
         name='course_update'),
    path('courses/<int:course_id>/delete/', views.course_delete,
         name='course_delete'),
    path('courses/<int:course_id>/add-student/', views.add_student_to_course,
         name='add_student_to_course'),

    # Маршруты для студентов (Students)
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_detail,
         name='student_detail'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:student_id>/update/', views.student_update,
         name='student_update'),
    path('students/<int:student_id>/delete/', views.student_delete,
         name='student_delete'),

    # Действия со студентами и курсами
    path('students/<int:student_id>/enroll/<int:course_id>/',
         views.enroll_student, name='enroll_student'),
    path('students/<int:student_id>/unenroll/<int:course_id>/',
         views.unenroll_student, name='unenroll_student'),
    path('quick-enroll/', views.quick_enroll, name='quick_enroll'),
]
