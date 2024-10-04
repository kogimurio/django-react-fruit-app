from django.urls import path
from .import views

urlpatterns = [
    path('productlist/', views.product_list),
    path('productdetail/<int:pk>/', views.product_detail),
    path('contact/', views.contact_submission, name='contact_submission'),
]