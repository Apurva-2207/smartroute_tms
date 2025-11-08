# customer/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, CustomerProfile

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile and CustomerProfile when User is created
    """
    if created:
        try:
            # Create UserProfile if it doesn't exist
            user_profile, profile_created = UserProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'user_type': 'customer'
                }
            )
            
            # Create CustomerProfile if it doesn't exist
            CustomerProfile.objects.get_or_create(user_profile=user_profile)
            print(f"✓ Auto-created profiles for {instance.username}")
            
        except Exception as e:
            print(f"✗ Error creating profiles for {instance.username}: {e}")