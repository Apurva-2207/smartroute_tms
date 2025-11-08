from django.urls import path
from . import views
app_name = 'customer'

urlpatterns = [
    path('register/', views.customer_register, name='register'),
    path('login/', views.customer_login, name='login'),
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    path('logout/', views.customer_logout, name='logout'),
    
    path('shipments/', views.shipments_list, name='shipments'),
    path('tracking/<str:tracking_id>/', views.shipment_tracking, name='tracking'),
    path('payments/', views.payments_list, name='payments'),
    path('support/', views.support_tickets, name='support'),
    path('create-shipment/', views.create_shipment, name='create_shipment'),
    path('profile/', views.profile_view, name='profile'),
    path('invoice/pdf/<int:payment_id>/', views.download_invoice_pdf, name='download_invoice_pdf'),
    path('receipt/pdf/<int:payment_id>/', views.download_receipt_pdf, name='download_receipt_pdf'),
]