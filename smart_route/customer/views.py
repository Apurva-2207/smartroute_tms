from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import UserProfile, CustomerProfile, Shipment, Payment, SupportTicket
from django.http import HttpResponse
from .utils import generate_invoice_pdf, generate_receipt_pdf
from .models import Invoice
from datetime import datetime, timedelta
from django.db import transaction, models


def customer_register(request):
    """
    Handle customer registration with automatic profile creation
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')      
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
            else:
                try:
                    with transaction.atomic():
                        # Create user
                        user = User.objects.create_user(
                            username=username,
                            email=email,
                            password=password1,
                            first_name=first_name,
                            last_name=last_name
                        )
                        
                        # Wait a moment for signals to complete
                        import time
                        time.sleep(0.1)
                        
                        # Refresh user from database
                        user.refresh_from_db()
                        
                        # Get or create UserProfile
                        user_profile, created = UserProfile.objects.get_or_create
                        (
                            user==user,
                            defaults=={
                                'phone_number': phone,
                                'user_type':'customer'
                                'gender'  'gender'  # Add gender here
                            }
                        )
                        
                        # If profile already existed, update it
                        if not created:
                            user_profile.phone_number = phone
                            user_profile.user_type = 'customer'
                            user_profile.gender = gender 
                            user_profile.save()
                        
                        
                        # Create CustomerProfile
                        CustomerProfile.objects.get_or_create(user_profile=user_profile)
                        
                        messages.success(request, 'Account created successfully! Please login.')
                        return redirect('customer:login')
                        
                except Exception as e:
                    messages.error(request, f'Registration failed: {str(e)}')
                    print(f"REGISTRATION ERROR: {str(e)}")
        else:
            messages.error(request, 'Passwords do not match!')
    
    return render(request, 'customer/register.html')


def customer_login(request):
    """
    Handle customer login and redirect to dashboard
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('customer:dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'customer/login.html')


def customer_logout(request):
    """
    Handle customer logout
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('customer:login')


@login_required
def customer_dashboard(request):
    """
    Customer dashboard with comprehensive statistics
    """
    try:
        # Get customer profile with proper error handling
        customer_profile = CustomerProfile.objects.get(user_profile__user=request.user)
    except CustomerProfile.DoesNotExist:
        # Create missing profiles automatically
        try:
            user_profile, created = UserProfile.objects.get_or_create(
                user=request.user,
                defaults={'user_type': 'customer'}
            )
            customer_profile = CustomerProfile.objects.create(user_profile=user_profile)
            messages.info(request, 'Profile setup completed automatically!')
        except Exception as e:
            messages.error(request, 'Profile error. Please contact support.')
            return redirect('customer:login')
    
    # Dashboard statistics
    total_shipments = Shipment.objects.filter(customer=customer_profile).count()
    active_shipments = Shipment.objects.filter(
        customer=customer_profile,
        status__in=['confirmed', 'picked_up', 'in_transit', 'out_for_delivery']
    ).count()
    delivered_shipments = Shipment.objects.filter(
        customer=customer_profile, 
        status='delivered'
    ).count()
    pending_shipments = Shipment.objects.filter(
        customer=customer_profile, 
        status='pending'
    ).count()
    
    # Payment statistics
    total_payments = Payment.objects.filter(customer=customer_profile).count()
    completed_payments = Payment.objects.filter(
        customer=customer_profile, 
        status='completed'
    )
    pending_payments = Payment.objects.filter(
        customer=customer_profile, 
        status='pending'
    )
    
    total_amount_paid = sum(payment.total_amount for payment in completed_payments)
    pending_amount = sum(payment.total_amount for payment in pending_payments)
    
    # Recent data
    recent_shipments = Shipment.objects.filter(
        customer=customer_profile
    ).order_by('-created_at')[:5]
    
    recent_payments = Payment.objects.filter(
        customer=customer_profile
    ).order_by('-created_at')[:3]
    
    recent_tickets = SupportTicket.objects.filter(
        customer=customer_profile
    ).order_by('-created_at')[:3]
    
    # Payment methods breakdown
    payment_methods = Payment.objects.filter(
        customer=customer_profile
    ).values('payment_method').annotate(
        count=models.Count('id'),
        total_amount=models.Sum('total_amount')
    )
    
    context = {
        'customer': customer_profile,
        'total_shipments': total_shipments,
        'active_shipments': active_shipments,
        'delivered_shipments': delivered_shipments,
        'pending_shipments': pending_shipments,
        'total_payments': total_payments,
        'total_amount_paid': total_amount_paid or 0,
        'pending_amount': pending_amount or 0,
        'recent_shipments': recent_shipments,
        'recent_payments': recent_payments,
        'recent_tickets': recent_tickets,
        'payment_methods': payment_methods,
    }
    
    return render(request, 'customer/dashboard.html', context)


@login_required
def shipments_list(request):
    """
    Display all shipments for the customer
    """
    customer_profile = get_object_or_404(CustomerProfile, user_profile__user=request.user)
    shipments = Shipment.objects.filter(customer=customer_profile).order_by('-created_at')
    
    context = {
        'shipments': shipments,
    }
    return render(request, 'customer/shipments.html', context)


@login_required
def shipment_tracking(request, tracking_id):
    """
    Track specific shipment
    """
    customer_profile = get_object_or_404(CustomerProfile, user_profile__user=request.user)
    shipment = get_object_or_404(Shipment, tracking_id=tracking_id, customer=customer_profile)
    
    context = {
        'shipment': shipment,
    }
    return render(request, 'customer/tracking.html', context)


@login_required
def payments_list(request):
    """
    Display all payments for the customer
    """
    customer_profile = get_object_or_404(CustomerProfile, user_profile__user=request.user)
    payments = Payment.objects.filter(customer=customer_profile).order_by('-created_at')
    
    context = {
        'payments': payments,
    }
    return render(request, 'customer/payments.html', context)


@login_required
def support_tickets(request):
    """
    Handle support tickets
    """
    customer_profile = get_object_or_404(CustomerProfile, user_profile__user=request.user)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        priority = request.POST.get('priority', 'medium')
        
        SupportTicket.objects.create(
            customer=customer_profile,
            subject=subject,
            description=description,
            priority=priority
        )
        messages.success(request, 'Support ticket created successfully!')
        return redirect('customer:support')
    
    tickets = SupportTicket.objects.filter(customer=customer_profile).order_by('-created_at')
    
    context = {
        'tickets': tickets,
    }
    return render(request, 'customer/support.html', context)


@login_required
def create_shipment(request):
    """
    Create new shipment
    """
    customer_profile = get_object_or_404(CustomerProfile, user_profile__user=request.user)
    
    if request.method == 'POST':
        pickup_address = request.POST.get('pickup_address')
        delivery_address = request.POST.get('delivery_address')
        goods_type = request.POST.get('goods_type')
        weight = request.POST.get('weight')
        
        # Generate tracking ID
        tracking_id = f"SR{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        Shipment.objects.create(
            customer=customer_profile,
            tracking_id=tracking_id,
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            goods_type=goods_type,
            weight=weight,
            estimated_delivery=timezone.now() + timedelta(days=3)
        )
        
        messages.success(request, f'Shipment created successfully! Tracking ID: {tracking_id}')
        return redirect('customer:shipments')
    
    return render(request, 'customer/create_shipment.html')


@login_required
def profile_view(request):
    """
    Handle customer profile view and updates
    """
    customer_profile = get_object_or_404(CustomerProfile, user_profile__user=request.user)
    user_profile = customer_profile.user_profile
    
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()
        
        # Update user profile
        user_profile.phone_number = request.POST.get('phone_number')
        if hasattr(user_profile, 'address_line_1'):
            user_profile.address_line_1 = request.POST.get('address_line_1')
        if hasattr(user_profile, 'address_line_2'):
            user_profile.address_line_2 = request.POST.get('address_line_2')
        if hasattr(user_profile, 'city'):
            user_profile.city = request.POST.get('city')
        if hasattr(user_profile, 'state'):
            user_profile.state = request.POST.get('state')
        if hasattr(user_profile, 'pincode'):
            user_profile.pincode = request.POST.get('pincode')
        user_profile.save()
        
        # Update customer profile
        if hasattr(customer_profile, 'preferred_communication'):
            customer_profile.preferred_communication = request.POST.get('preferred_communication')
        if hasattr(customer_profile, 'default_pickup_address'):
            customer_profile.default_pickup_address = request.POST.get('default_pickup_address')
        if hasattr(customer_profile, 'default_delivery_instructions'):
            customer_profile.default_delivery_instructions = request.POST.get('default_delivery_instructions')
        customer_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('customer:profile')
    
    context = {
        'customer': customer_profile,
        'user_profile': user_profile,
    }
    return render(request, 'customer/profile.html', context)


@login_required
def download_invoice_pdf(request, payment_id):
    """Download invoice as PDF"""
    return generate_invoice_pdf(payment_id)


@login_required
def download_receipt_pdf(request, payment_id):
    """Download receipt as PDF"""
    return generate_receipt_pdf(payment_id)