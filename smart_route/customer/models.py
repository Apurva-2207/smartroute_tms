# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class CustomerProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    # Add customer-specific fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Customer: {self.user_profile.user.username}"









# class UserProfile(models.Model):
#     USER_TYPE_CHOICES = (
#         ('customer', 'Customer'),
#         ('driver', 'Driver'),
#         ('transporter', 'Transporter'),
#     )
    
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
#     phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    
#     # Personal Information
#     date_of_birth = models.DateField(null=True, blank=True)
#     gender = models.CharField(max_length=10, choices=(('male', 'Male'), ('female', 'Female'), ('other', 'Other')), blank=True)
    
#     # Address Information
#     address_line_1 = models.CharField(max_length=255)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=10)
#     country = models.CharField(max_length=100, default='India')
    
#     # Business Information (for transporters)
#     company_name = models.CharField(max_length=255, blank=True)
#     gst_number = models.CharField(max_length=15, blank=True)
    
#     profile_completed = models.BooleanField(default=False)
    
#     def __str__(self):
#         return f"{self.user.username} ({self.user_type})"

# class CustomerProfile(models.Model):
#     user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    
#     preferred_communication = models.CharField(
#         max_length=20, 
#         choices=(('email', 'Email'), ('phone', 'Phone'), ('whatsapp', 'WhatsApp')),
#         default='email'
#     )
    
#     default_pickup_address = models.TextField(blank=True)
#     default_delivery_instructions = models.TextField(blank=True)
    
#     loyalty_points = models.IntegerField(default=0)
#     member_since = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"Customer Profile - {self.user_profile.user.username}"









# # Signal to create UserProfile when User is created
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()
    
# Add these after your existing CustomerProfile model

class Shipment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    tracking_id = models.CharField(max_length=20, unique=True)
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    goods_type = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    estimated_delivery = models.DateTimeField()
    actual_delivery = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tracking_id} - {self.customer.user_profile.user.username}"

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('netbanking', 'Net Banking'),
    )
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SupportTicket(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    )
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
   
   
   
   
  

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('netbanking', 'Net Banking'),
        ('wallet', 'Digital Wallet'),
    )
    
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    upi_id = models.CharField(max_length=100, blank=True)
    card_last_four = models.CharField(max_length=4, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number: INV-YYYYMM-XXXXX
            today = date.today()
            base_invoice = f"INV-{today.strftime('%Y%m')}-"
            last_invoice = Payment.objects.filter(
                invoice_number__startswith=base_invoice
            ).order_by('-invoice_number').first()
            
            if last_invoice:
                last_num = int(last_invoice.invoice_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
                
            self.invoice_number = f"{base_invoice}{new_num:05d}"
        
        # Calculate GST (18% example)
        if not self.gst_amount and self.amount:
            self.gst_amount = round(self.amount * 0.18, 2)
            self.sgst = round(self.gst_amount / 2, 2)  # 9% SGST
            self.cgst = round(self.gst_amount / 2, 2)  # 9% CGST
            self.total_amount = self.amount + self.gst_amount
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - ₹{self.amount}"

class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    notes = models.TextField(blank=True)
    terms_and_conditions = models.TextField(blank=True)
    
    def __str__(self):
        return f"Invoice for {self.payment.invoice_number}" 