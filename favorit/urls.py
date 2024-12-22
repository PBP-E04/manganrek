from django.urls import path
from favorit.views import show_favorit, show_json_favorit, show_json_rumah_makan_by_favorit, update_favorit_restoran, update_favorit_favorit, update_favorit_flutter

app_name = 'favorit'

urlpatterns = [
    path('', show_favorit, name='show_favorit'),
    path('json-favorit/',show_json_favorit, name='show_json_favorit'),
    path('json-rm-favorit/<str:id_rumah_makan>/',show_json_rumah_makan_by_favorit, name='show_json_rumah_makan_by_favorit'),
    path('update-favorit-restoran/<uuid:id>/',update_favorit_restoran, name='update_favorit_restoran'),
    path('update-favorit-favorit/<uuid:id>/',update_favorit_favorit, name='update_favorit_favorit'),
    path('update-favorit-flutter/<uuid:id>/',update_favorit_flutter, name='update_favorit_flutter'),
]