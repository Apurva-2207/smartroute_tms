from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('transporter', 'Transporter'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
    # Personal Information
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True)
    
    # Address Information
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    
    # Business Information (for transporters)
    company_name = models.CharField(max_length=255, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    
    profile_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} ({self.user_type})"

class CustomerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
    preferred_communication = models.CharField(
        max_length=20, 
        choices=(('email', 'Email'), ('phone', 'Phone'), ('whatsapp', 'WhatsApp')),
        default='email'
    )
    
    default_pickup_address = models.TextField(blank=True)
    default_delivery_instructions = models.TextField(blank=True)
    
    loyalty_points = models.IntegerField(default=0)
    member_since = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Customer Profile - {self.user_profile.user.username}"

# Signal to create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()