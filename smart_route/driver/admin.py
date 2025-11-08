from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Driver, Vehicle, Delivery, Earnings, PasswordResetToken

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'license_number', 'vehicle_type', 'has_own_vehicle', 'is_active', 'created_at']
    list_filter = ['has_own_vehicle', 'vehicle_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone', 'license_number']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']  # Allow quick activation/deactivation

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'vehicle_type', 'capacity', 'status', 'assigned_to', 'created_at']
    list_filter = ['status', 'vehicle_type', 'created_at']
    search_fields = ['registration_number', 'assigned_to__user__username']

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'customer_name', 'status', 'estimated_fare', 'assigned_at']
    list_filter = ['status', 'assigned_at']

@admin.register(Earnings)
class EarningsAdmin(admin.ModelAdmin):
    list_display = ['driver', 'delivery', 'amount', 'date', 'is_paid']
    list_filter = ['is_paid', 'date']

@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']