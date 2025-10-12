from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='transporter_dashboard'),  # example page
]