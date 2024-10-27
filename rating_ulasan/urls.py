from django.urls import path
from . import views

app_name = "review"

urlpatterns = [
    path('', views.review_list, name= "review_list"),
    path('show-json/', views.show_json, name='show_json'),
    path('get-review/<int:pk>/', views.get_review_json, name='get_review_json'),
    path('add_review/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete/<int:review_id>/', views.delete_review, name='delete_review'),
]