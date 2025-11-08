from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Driver(models.Model):
    VEHICLE_TYPES = [
        ('mini', '🚗 Mini Vehicle (30-300 kg)'),
        ('lcv', '🚐 LCV (300-1000 kg)'),
        ('mcv', '🚛 MCV (1000-5000 kg)'),
        ('hcv', '🚚 HCV (5000-16000 kg)'),
        ('trailer', '🚛 Trailer (16000-35000 kg)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='driver_profiles/', null=True, blank=True)
    has_own_vehicle = models.BooleanField(default=False)
    assigned_vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def email(self):
        return self.user.email

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('mini', '🚗 Mini Vehicle'),
        ('lcv', '🚐 LCV'),
        ('mcv', '🚛 MCV'),
        ('hcv', '🚚 HCV'),
        ('trailer', '🚛 Trailer'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    registration_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    assigned_to = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='vehicles')
    current_location = models.CharField(max_length=100, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_vehicle_type_display()} - {self.registration_number}"

class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned to Driver'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='deliveries')
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15)
    package_description = models.TextField()
    package_weight = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_fare = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_at = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Delivery #{self.id} - {self.customer_name}"

class Earnings(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='earnings')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Earning - {self.driver.user.username} - {self.amount}"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    def __str__(self):
        return f"Password reset for {self.user.username}"