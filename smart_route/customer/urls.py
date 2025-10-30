from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('register/', views.customer_register, name='register'),
    path('login/', views.customer_login, name='login'),
    path('dashboard/', views.customer_dashboard, name='dashboard'),
]