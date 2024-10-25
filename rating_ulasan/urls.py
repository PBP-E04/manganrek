from django.urls import path
from . import views

urlpatterns = [
    path('<str:rumah_makan_nama>/review-page/', views.review_page, name='review_page'),
    path('<str:rumah_makan_nama>/edit-review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('<str:rumah_makan_nama>/delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]
