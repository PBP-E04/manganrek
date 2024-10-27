from django.urls import path
from . import views  
from django.contrib.auth import views as auth_views

from profil.views import (
    user_profile_list,
    user_profile_create,
    user_profile_detail,
    user_profile_update,
    user_profile_delete,
    add_food_preference,
    list_user_food_preferences,
    add_search_history,
    list_user_search_history,
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
    path('create/', user_profile_create, name='user_profile_create'),  # URL untuk membuat profil baru
    path('user-profile/<uuid:user_profile_id>/', user_profile_detail, name='user_profile_detail'),  # Pastikan ini sesuai
    path('user-profile/<uuid:user_profile_id>/update/', user_profile_update, name='user_profile_update'),
    path('user-profile-delete/', user_profile_delete, name='user_profile_delete'),  # URL untuk menghapus profil
    path('list-user-food-preferences/', list_user_food_preferences, name='list_user_food_preferences'),  # URL untuk preferensi makanan
    path('add-food-preference/', add_food_preference, name='add_food_preference'),  # URL untuk menambahkan preferensi makanan
    path('list-user-search-history/', list_user_search_history, name='list_user_search_history'),  # URL untuk riwayat pencarian
    path('add-search-history/', add_search_history, name='add_search_history'),  # URL untuk menambahkan riwayat pencarian
    path('login/', login_user, name='login'),  # Pastikan ini ada
    path('logout/', logout_user, name='logout'),  # URL untuk logout
    path('register-user/', register_user, name='register_user'),  # URL untuk mendaftar
    path('user-profile/follow/<uuid:user_profile_id>/', follow_user, name='follow_user'),  # Pastikan ini ada
    path('user-profile/unfollow/<uuid:user_profile_id>/', unfollow_user, name='unfollow_user'),  # Pastikan ini ada
    path('delete-account/', delete_account, name='delete_account'),
]
