from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='customer_dashboard'),  # example page
]