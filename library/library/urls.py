# library/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),  # Подключаем URL-ы приложения catalog
]

handler404 = 'catalog.views.custom_page_not_found'
