# courses/urls.py
from django.urls import path, re_path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:author_id>/', views.author_detail, name='author_detail'),
    re_path(r'^info', views.info, name='info'),
]

# Обработчик 404
handler404 = 'catalog.views.custom_page_not_found'
