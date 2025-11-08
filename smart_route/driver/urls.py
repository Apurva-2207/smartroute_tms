# from django.urls import path
# from . import views

# app_name = 'driver'

# urlpatterns = [
#     path('register/', views.driver_register, name='register'),
#     path('login/', views.driver_login, name='login'),
#     path('dashboard/', views.driver_dashboard, name='dashboard'),
# ]


from django.urls import path
from . import views

app_name = 'driver'

urlpatterns = [
    # Authentication URLs
    path('register/', views.driver_register, name='register'),
    path('login/', views.driver_login, name='login'),
    path('logout/', views.driver_logout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uuid:token>/', views.reset_password, name='reset_password'),
    
    # Dashboard URLs
    path('dashboard/', views.driver_dashboard, name='dashboard'),
    path('deliveries/', views.my_deliveries, name='my_deliveries'),
    path('deliveries/<int:delivery_id>/', views.delivery_detail, name='delivery_detail'),
    path('delivery/<int:delivery_id>/update/<str:status>/', views.update_delivery_status, name='update_delivery_status'),
    path('vehicle/', views.vehicle_info, name='vehicle_info'),
    path('earnings/', views.earnings, name='earnings'),
    path('settings/', views.settings, name='settings'),
]