from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('users/', views.user_list, name='user_list'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('friends/add/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('friends/accept/<str:username>/', views.accept_friend_request, name='accept_friend_request'),
    path('friends/reject/<str:username>/', views.reject_friend_request, name='reject_friend_request'),
    path('friends/remove/<str:username>/', views.remove_friend, name='remove_friend'),
]
