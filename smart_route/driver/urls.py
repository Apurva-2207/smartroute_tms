from django.urls import path
from . import views

app_name = 'driver'

urlpatterns = [
    path('register/', views.driver_register, name='register'),
    path('login/', views.driver_login, name='login'),
    path('dashboard/', views.driver_dashboard, name='dashboard'),
]