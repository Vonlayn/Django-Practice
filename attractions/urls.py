from django.urls import path
from .views import CreateReviewView, UpdateReviewView, DeleteReviewView
from . import views

urlpatterns = [
    path("<int:attr_id>", views.reviews, name='reviews'),
    path('', views.index, name='home'),
    path('top/', views.top, name='top'),
    path('<int:id>/review/new/', CreateReviewView.as_view(), name='review-create'),
    path('<int:pk>/review/update/', UpdateReviewView.as_view(), name='review-update'),
    path('<int:pk>/review/delete/', DeleteReviewView.as_view(), name='review-delete')
]
