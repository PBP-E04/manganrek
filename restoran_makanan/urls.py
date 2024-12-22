from django.urls import path
from restoran_makanan.views import show_json_menu, show_json_rumah_makan, show_json_menu_by_id, show_json_rumah_makan_by_id, show_json_menu_by_rumah_makan, show_rumahmakan_makanan, show_detail_rumah_makan
from restoran_makanan.views import add_rumah_makan, edit_rumah_makan, delete_rumah_makan
from restoran_makanan.views import add_menu, edit_menu, delete_menu
from restoran_makanan.views import create_rumah_makan_flutter, edit_rumah_makan_flutter, delete_rumah_makan_flutter
from restoran_makanan.views import create_menu_flutter, edit_menu_flutter, delete_menu_flutter

app_name = 'restoran_makanan'

urlpatterns = [
    path('', show_rumahmakan_makanan, name='show_rumahmakan_makanan'),
    path('json-menu/', show_json_menu, name='show_json_menu'),
    path('json-rumahmakan/', show_json_rumah_makan, name='show_json_rumah_makan'),
    path('json-menu/<str:id>/', show_json_menu_by_id, name='show_json_menu_by_id'),
    path('json-rumahmakan/<str:id>/', show_json_rumah_makan_by_id, name='show_json_rumah_makan_by_id'),
    path('json-menu-by-rumahmakan/<str:id_rumah_makan>/', show_json_menu_by_rumah_makan, name='show_json_menu_by_rumah_makan'),
    path('detail/<str:id_rumah_makan>/', show_detail_rumah_makan, name='detail_rumah_makan'),
    path('add-rm/', add_rumah_makan, name='add_rumah_makan'),
    path('edit-rm/<str:id>/', edit_rumah_makan, name='edit_rumah_makan'),
    path('delete-rm/<str:id>/', delete_rumah_makan, name='delete_rumah_makan'),
    path('add-menu/<uuid:id_rumah_makan>/', add_menu, name='add_menu'),
    path('edit-menu/<uuid:id>/', edit_menu, name='edit_menu'),
    path('delete-menu/<uuid:id>/', delete_menu, name='delete_menu'),
    path('create-rm-flutter/', create_rumah_makan_flutter, name='create_rumah_makan_flutter'),
    path('edit-rm-flutter/<str:id>/', edit_rumah_makan_flutter, name='edit_rumah_makan_flutter'),
    path('delete-rm-flutter/<str:id>/', delete_rumah_makan_flutter, name='delete_rumah_makan_flutter'),
    path('create-menu-flutter/', create_menu_flutter, name='create_menu_flutter'),
    path('edit-menu-flutter/<str:id>/', edit_menu_flutter, name='edit_menu_flutter'),
    path('delete-menu-flutter/<str:id>/', delete_menu_flutter, name='delete_menu_flutter'),
]