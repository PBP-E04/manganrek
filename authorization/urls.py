from django.urls import path
from authorization.views import login,register,logout,get_users

app_name = 'authorization'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('get-users/',get_users, name='get_user')
]