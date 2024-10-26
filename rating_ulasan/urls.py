from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path('', views.show_review_page, name= "review_page"),
    path('search/', views.search_restaurants, name="search_resto"),
    path('show-json/', views.show_json, name='show_json'),
    path('get-review/<int:book_id>/', views.get_review_json, name='get_review_json'),
    # path('<str:rumah_makan_nama>/review-page/', views.review_page, name='review_page'),
]
