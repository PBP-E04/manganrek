from django.urls import path
from .views import show_json_menu, show_json_rumah_makan, show_json_menu_by_id, show_json_rumah_makan_by_id, show_json_menu_by_rumah_makan
from rating_ulasan.views import review_page

app_name = 'restoran_makanan'

urlpatterns = [
    path('<str:rumah_makan_nama>/', review_page, name='review_page'),
    path('<str:rumah_makan_nama>/review-page/', review_page, name='review_page'),
    path('json-menu/', show_json_menu, name='show_json_menu'),
    path('json-rumahmakan/', show_json_rumah_makan, name='show_json_rumah_makan'),
    path('json-menu/<str:id>/', show_json_menu_by_id, name='show_json_menu_by_id'),
    path('json-rumahmakan/<str:id>/', show_json_rumah_makan_by_id, name='show_json_rumah_makan_by_id'),
    path('json-menu-by-rumahmakan/<str:id_rumah_makan>/', show_json_menu_by_rumah_makan, name='show_json_menu_by_rumah_makan'),
]