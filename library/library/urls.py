# library/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('catalog.urls')),  # Подключаем URL-ы приложения catalog
    path('', include('schedule.urls')),
    path('auth/', include('django.contrib.auth.urls')),  # стандартные auth URL
    path('auth/', include('users.urls')),  # наши URL для регистрации
]

handler404 = 'schedule.views.custom_404'
# handler404 = 'catalog.views.custom_page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
