from django.urls import path
from . import views  
from django.contrib.auth import views as auth_views

from profil.views import (
    user_profile_list,
    user_profile_detail,
    user_profile_update,
    login_user,
    logout_user,
    register_user,
    follow_user,
    unfollow_user,
    delete_account,
)

app_name = 'profil'

urlpatterns = [
    path('user-profilelist/', user_profile_list, name='user_profile_list'),  # URL untuk daftar profil pengguna
    path('user-profile/<uuid:user_profile_id>/', user_profile_detail, name='user_profile_detail'),  # Pastikan ini sesuai
    path('user-profile/<uuid:user_profile_id>/update/', user_profile_update, name='user_profile_update'),
    path('login/', login_user, name='login'),  # Pastikan ini ada
    path('logout/', logout_user, name='logout'),  # URL untuk logout
    path('register/', register_user, name='register'),  # URL untuk mendaftar
    path('user-profile/follow/<uuid:user_profile_id>/', follow_user, name='follow_user'),  # Pastikan ini ada
    path('user-profile/unfollow/<uuid:user_profile_id>/', unfollow_user, name='unfollow_user'),  # Pastikan ini ada
    path('delete-account/', delete_account, name='delete_account'),
]
