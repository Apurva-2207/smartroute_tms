# # transporter/urls.py
# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# app_name = 'transporter'

# urlpatterns = [
#     # Authentication URLs
#     path('login/', views.transporter_login, name='login'),
#     path('register/', views.transporter_register, name='register'),
#     path('logout/', views.transporter_logout, name='logout'),
    
#     # Password Reset URLs
#     path('password-reset/', 
#          auth_views.PasswordResetView.as_view(
#              template_name='transporter/password_reset.html',
#              email_template_name='transporter/password_reset_email.html',
#              subject_template_name='transporter/password_reset_subject.txt'
#          ), 
#          name='password_reset'),
    
#     path('password-reset/done/', 
#          auth_views.PasswordResetDoneView.as_view(
#              template_name='transporter/password_reset_done.html'
#          ), 
#          name='password_reset_done'),
    
#     path('password-reset-confirm/<uidb64>/<token>/', 
#          auth_views.PasswordResetConfirmView.as_view(
#              template_name='transporter/password_reset_confirm.html'
#          ), 
#          name='password_reset_confirm'),
    
#     path('password-reset-complete/', 
#          auth_views.PasswordResetCompleteView.as_view(
#              template_name='transporter/password_reset_complete.html'
#          ), 
#          name='password_reset_complete'),
    
#     # Dashboard URL
#     path('dashboard/', views.transporter_dashboard, name='dashboard'),
# ]



# transporter/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'transporter'

urlpatterns = [
    # Authentication URLs
    path('login/', views.transporter_login, name='login'),
    path('register/', views.transporter_register, name='register'),
    path('logout/', views.transporter_logout, name='logout'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='transporter/password_reset.html',
             email_template_name='transporter/password_reset_email.html',
             subject_template_name='transporter/password_reset_subject.txt'
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='transporter/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='transporter/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='transporter/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # Dashboard and Profile URLs
    path('dashboard/', views.transporter_dashboard, name='dashboard'),
    path('profile/', views.transporter_profile, name='profile'),
]