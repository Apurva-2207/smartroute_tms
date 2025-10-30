from django.db import models
from django.contrib.auth.models import User

class DriverProfile(models.Model):
    VEHICLE_CHOICES = [
        ('mini', 'Mini Vehicle (30-300 kg)'),
        ('lcv', 'LCV (300-1000 kg)'),
        ('mcv', 'MCV (1000-5000 kg)'),
        ('hcv', 'HCV (5000-16000 kg)'),
        ('trailer', 'Trailer (16000-35000 kg)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_CHOICES)
    vehicle_number = models.CharField(max_length=20)
    vehicle_capacity = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    
    total_deliveries = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.FloatField(default=5.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        capacity_map = {
            'mini': '30-300 kg',
            'lcv': '300-1000 kg', 
            'mcv': '1000-5000 kg',
            'hcv': '5000-16000 kg',
            'trailer': '16000-35000 kg'
        }
        self.vehicle_capacity = capacity_map.get(self.vehicle_type, 'Unknown')
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_vehicle_type_display()}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_driver_profile(sender, instance, created, **kwargs):
    if created:
        DriverProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_driver_profile(sender, instance, **kwargs):
    if hasattr(instance, 'driverprofile'):
        instance.driverprofile.save()