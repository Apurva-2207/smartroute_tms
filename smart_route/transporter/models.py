from django.db import models

# Create your models here.
# transporter/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class TransporterProfile(models.Model):
    VEHICLE_TYPES = [
        ('mini', 'Mini Vehicle (30-300 kg)'),
        ('lcv', 'LCV (300-1000 kg)'),
        ('mcv', 'MCV (1000-5000 kg)'),
        ('hcv', 'HCV (5000-16000 kg)'),
        ('trailer', 'Trailer (16000-35000 kg)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='transporter_profile')
    company_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    license_number = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = "Transporter Profile"
        verbose_name_plural = "Transporter Profiles"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create transporter profile when user is created
    Note: This is just a placeholder. Actual creation happens in registration view.
    """
    if created:
        # Profile will be created during registration
        pass