# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.db import transaction
# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from .models import Driver, Vehicle, Delivery, Earnings, PasswordResetToken
# import uuid
# from datetime import timedelta

# # Authentication Views
# def driver_register(request):
#     if request.method == 'POST':
#         try:
#             with transaction.atomic():
#                 # Get form data
#                 first_name = request.POST.get('first_name')
#                 last_name = request.POST.get('last_name')
#                 username = request.POST.get('username')
#                 email = request.POST.get('email')
#                 phone = request.POST.get('phone')
#                 license_number = request.POST.get('license_number')
#                 password1 = request.POST.get('password1')
#                 password2 = request.POST.get('password2')
#                 has_own_vehicle = request.POST.get('has_own_vehicle') == 'yes'
#                 vehicle_type = request.POST.get('vehicle_type')
#                 vehicle_number = request.POST.get('vehicle_number')
#                 profile_image = request.FILES.get('profile_image')
#                 address = request.POST.get('address')
#                 city = request.POST.get('city')
#                 state = request.POST.get('state')
#                 pincode = request.POST.get('pincode')
                
#                 # Validate passwords match
#                 if password1 != password2:
#                     messages.error(request, "Passwords do not match")
#                     return redirect('driver:register')
                
#                 # Check if username exists
#                 if User.objects.filter(username=username).exists():
#                     messages.error(request, "Username already exists")
#                     return redirect('driver:register')
                
#                 # Check if email exists
#                 if User.objects.filter(email=email).exists():
#                     messages.error(request, "Email already exists")
#                     return redirect('driver:register')
                
#                 # Create user
#                 user = User.objects.create_user(
#                     username=username,
#                     email=email,
#                     password=password1,
#                     first_name=first_name,
#                     last_name=last_name
#                 )
                
#                 # Create driver profile
#                 driver = Driver.objects.create(
#                     user=user,
#                     phone=phone,
#                     license_number=license_number,
#                     has_own_vehicle=has_own_vehicle,
#                     address=address,
#                     city=city,
#                     state=state,
#                     pincode=pincode,
#                     status='pending'
#                 )
                
#                 # Add vehicle information if driver has own vehicle
#                 if has_own_vehicle and vehicle_type and vehicle_number:
#                     driver.vehicle_type = vehicle_type
#                     driver.vehicle_number = vehicle_number
                
#                 # Handle profile image
#                 if profile_image:
#                     driver.profile_image = profile_image
                
#                 driver.save()
                
#                 messages.success(request, "Registration successful! Please wait for admin approval.")
#                 return redirect('driver:login')
                
#         except Exception as e:
#             messages.error(request, f"Registration failed: {str(e)}")
#             return redirect('driver:register')
    
#     return render(request, 'driver/register.html')

# def driver_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         remember_me = request.POST.get('remember')
        
#         user = authenticate(request, username=username, password=password)
        
#         if user is not None:
#             try:
#                 driver = Driver.objects.get(user=user)
#                 if driver.status == 'approved':
#                     login(request, user)
#                     if not remember_me:
#                         request.session.set_expiry(0)  # Session expires when browser closes
#                     messages.success(request, f"Welcome back, {driver.user.first_name}!")
#                     return redirect('driver:dashboard')
#                 elif driver.status == 'pending':
#                     messages.warning(request, "Your account is pending approval. Please wait for admin approval.")
#                 elif driver.status == 'rejected':
#                     messages.error(request, "Your account has been rejected. Please contact admin.")
#                 elif driver.status == 'suspended':
#                     messages.error(request, "Your account has been suspended. Please contact admin.")
#             except Driver.DoesNotExist:
#                 messages.error(request, "Driver profile not found.")
#         else:
#             messages.error(request, "Invalid username or password")
    
#     return render(request, 'driver/login.html')

# @login_required
# def driver_logout(request):
#     logout(request)
#     messages.success(request, "You have been logged out successfully")
#     return redirect('driver:login')

# # Password Reset Views
# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
        
#         try:
#             user = User.objects.get(email=email)
#             driver = Driver.objects.get(user=user)
            
#             # Create password reset token
#             expires_at = timezone.now() + timedelta(hours=24)
#             reset_token = PasswordResetToken.objects.create(
#                 user=user,
#                 expires_at=expires_at
#             )
            
#             # Send email
#             reset_link = f"{request.scheme}://{request.get_host()}/driver/reset-password/{reset_token.token}/"
            
#             subject = "Password Reset Request - SmartRoute"
#             html_message = render_to_string('driver/email/password_reset.html', {
#                 'driver_name': driver.full_name,
#                 'reset_link': reset_link,
#             })
#             plain_message = strip_tags(html_message)
            
#             send_mail(
#                 subject,
#                 plain_message,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 html_message=html_message,
#                 fail_silently=False,
#             )
            
#             messages.success(request, "Password reset link has been sent to your email.")
#             return redirect('driver:login')
            
#         except (User.DoesNotExist, Driver.DoesNotExist):
#             messages.error(request, "No account found with this email address.")
    
#     return render(request, 'driver/forgot_password.html')

# def reset_password(request, token):
#     try:
#         reset_token = PasswordResetToken.objects.get(token=token, is_used=False)
        
#         if not reset_token.is_valid():
#             messages.error(request, "This reset link has expired or is invalid.")
#             return redirect('driver:forgot_password')
        
#         if request.method == 'POST':
#             password1 = request.POST.get('password1')
#             password2 = request.POST.get('password2')
            
#             if password1 != password2:
#                 messages.error(request, "Passwords do not match.")
#                 return redirect('driver:reset_password', token=token)
            
#             # Update password
#             user = reset_token.user
#             user.set_password(password1)
#             user.save()
            
#             # Mark token as used
#             reset_token.is_used = True
#             reset_token.save()
            
#             messages.success(request, "Password reset successfully. You can now login with your new password.")
#             return redirect('driver:login')
        
#         return render(request, 'driver/reset_password.html', {'token': token})
    
#     except PasswordResetToken.DoesNotExist:
#         messages.error(request, "Invalid reset link.")
#         return redirect('driver:forgot_password')

# # Dashboard Views
# @login_required
# def driver_dashboard(request):
#     try:
#         driver = Driver.objects.get(user=request.user)
        
#         if driver.status != 'approved':
#             messages.warning(request, "Your account is not approved yet. Please wait for admin approval.")
#             return redirect('driver:login')
        
#         # Get driver statistics
#         total_deliveries = Delivery.objects.filter(driver=driver).count()
#         completed_deliveries = Delivery.objects.filter(driver=driver, status='delivered').count()
#         pending_deliveries = Delivery.objects.filter(driver=driver, status__in=['assigned', 'picked_up', 'in_transit']).count()
#         total_earnings = Earnings.objects.filter(driver=driver, is_paid=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
#         # Get recent deliveries
#         recent_deliveries = Delivery.objects.filter(driver=driver).order_by('-assigned_at')[:5]
        
#         # Get weekly performance data
#         today = timezone.now().date()
#         week_ago = today - timedelta(days=7)
#         weekly_deliveries = Delivery.objects.filter(
#             driver=driver, 
#             assigned_at__date__range=[week_ago, today]
#         ).values('assigned_at__date').annotate(count=models.Count('id')).order_by('assigned_at__date')
        
#         context = {
#             'driver': driver,
#             'total_deliveries': total_deliveries,
#             'completed_deliveries': completed_deliveries,
#             'pending_deliveries': pending_deliveries,
#             'total_earnings': total_earnings,
#             'recent_deliveries': recent_deliveries,
#             'weekly_deliveries': list(weekly_deliveries),
#         }
        
#         return render(request, 'driver/dashboard.html', context)
        
#     except Driver.DoesNotExist:
#         messages.error(request, "Driver profile not found")
#         return redirect('driver:login')
from django.db import models   
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Driver, Vehicle, Delivery, Earnings, PasswordResetToken
import uuid
from datetime import timedelta

# Authentication Views
def driver_register(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Get form data
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')
                phone = request.POST.get('phone')
                license_number = request.POST.get('license_number')
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                has_own_vehicle = request.POST.get('has_own_vehicle') == 'yes'
                vehicle_type = request.POST.get('vehicle_type')
                vehicle_number = request.POST.get('vehicle_number')
                profile_image = request.FILES.get('profile_image')
                address = request.POST.get('address')
                city = request.POST.get('city')
                state = request.POST.get('state')
                pincode = request.POST.get('pincode')
                
                # Validate passwords match
                if password1 != password2:
                    messages.error(request, "Passwords do not match")
                    return redirect('driver:register')
                
                # Check if username exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists")
                    return redirect('driver:register')
                
                # Check if email exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('driver:register')
                
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Create driver profile
                driver = Driver.objects.create(
                    user=user,
                    phone=phone,
                    license_number=license_number,
                    has_own_vehicle=has_own_vehicle,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                    is_active=True  # Auto-activate driver
                )
                
                # Add vehicle information if driver has own vehicle
                if has_own_vehicle and vehicle_type and vehicle_number:
                    driver.vehicle_type = vehicle_type
                    driver.vehicle_number = vehicle_number
                
                # Handle profile image
                if profile_image:
                    driver.profile_image = profile_image
                
                driver.save()
                
                # Auto-login after registration
                user = authenticate(request, username=username, password=password1)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome to SmartRoute, {first_name}! Your driver account has been created successfully.")
                    return redirect('driver:login')
                
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            return redirect('driver:register')
    
    return render(request, 'driver/register.html')

def driver_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                driver = Driver.objects.get(user=user)
                if driver.is_active:
                    login(request, user)
                    if not remember_me:
                        request.session.set_expiry(0)  # Session expires when browser closes
                    messages.success(request, f"Welcome back, {driver.user.first_name}!")
                    return redirect('driver:dashboard')
                else:
                    messages.error(request, "Your account has been deactivated. Please contact support.")
            except Driver.DoesNotExist:
                messages.error(request, "Driver profile not found.")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'driver/login.html')

@login_required
def driver_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('home')  # Redirect to homepage

# Password Reset Views (keep the same as before)
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            driver = Driver.objects.get(user=user)
            
            # Create password reset token
            expires_at = timezone.now() + timedelta(hours=24)
            reset_token = PasswordResetToken.objects.create(
                user=user,
                expires_at=expires_at
            )
            
            # Send email
            reset_link = f"{request.scheme}://{request.get_host()}/driver/reset-password/{reset_token.token}/"
            
            subject = "Password Reset Request - SmartRoute"
            html_message = render_to_string('driver/email/password_reset.html', {
                'driver_name': driver.full_name,
                'reset_link': reset_link,
            })
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('driver:login')
            
        except (User.DoesNotExist, Driver.DoesNotExist):
            messages.error(request, "No account found with this email address.")
    
    return render(request, 'driver/forgot_password.html')

def reset_password(request, token):
    try:
        reset_token = PasswordResetToken.objects.get(token=token, is_used=False)
        
        if not reset_token.is_valid():
            messages.error(request, "This reset link has expired or is invalid.")
            return redirect('driver:forgot_password')
        
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('driver:reset_password', token=token)
            
            # Update password
            user = reset_token.user
            user.set_password(password1)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            messages.success(request, "Password reset successfully. You can now login with your new password.")
            return redirect('driver:login')
        
        return render(request, 'driver/reset_password.html', {'token': token})
    
    except PasswordResetToken.DoesNotExist:
        messages.error(request, "Invalid reset link.")
        return redirect('driver:forgot_password')

# Dashboard Views (remove approval checks)
@login_required
def driver_dashboard(request):
    try:
        driver = Driver.objects.get(user=request.user)
        
        # Get driver statistics
        total_deliveries = Delivery.objects.filter(driver=driver).count()
        completed_deliveries = Delivery.objects.filter(driver=driver, status='delivered').count()
        pending_deliveries = Delivery.objects.filter(driver=driver, status__in=['assigned', 'picked_up', 'in_transit']).count()
        total_earnings = Earnings.objects.filter(driver=driver, is_paid=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        # Get recent deliveries
        recent_deliveries = Delivery.objects.filter(driver=driver).order_by('-assigned_at')[:5]
        
        context = {
            'driver': driver,
            'total_deliveries': total_deliveries,
            'completed_deliveries': completed_deliveries,
            'pending_deliveries': pending_deliveries,
            'total_earnings': total_earnings,
            'recent_deliveries': recent_deliveries,
        }
        
        return render(request, 'driver/dashboard.html', context)
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found")
        return redirect('driver:login')

# Other views remain the same (my_deliveries, delivery_detail, update_delivery_status, vehicle_info, earnings, settings)  
    
    
    

@login_required
def my_deliveries(request):
    try:
        driver = Driver.objects.get(user=request.user)
        
        status_filter = request.GET.get('status', 'all')
        deliveries = Delivery.objects.filter(driver=driver)
        
        if status_filter != 'all':
            deliveries = deliveries.filter(status=status_filter)
        
        deliveries = deliveries.order_by('-assigned_at')
        
        context = {
            'driver': driver,
            'deliveries': deliveries,
            'status_filter': status_filter,
        }
        
        return render(request, 'driver/my_deliveries.html', context)
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found")
        return redirect('driver:login')

@login_required
def delivery_detail(request, delivery_id):
    try:
        driver = Driver.objects.get(user=request.user)
        delivery = get_object_or_404(Delivery, id=delivery_id, driver=driver)
        
        context = {
            'driver': driver,
            'delivery': delivery,
        }
        
        return render(request, 'driver/delivery_detail.html', context)
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found")
        return redirect('driver:login')

@login_required
def update_delivery_status(request, delivery_id, status):
    try:
        driver = Driver.objects.get(user=request.user)
        delivery = Delivery.objects.get(id=delivery_id, driver=driver)
        
        valid_statuses = ['picked_up', 'in_transit', 'delivered']
        if status in valid_statuses:
            delivery.status = status
            if status == 'picked_up':
                delivery.picked_up_at = timezone.now()
            elif status == 'delivered':
                delivery.delivered_at = timezone.now()
                # Create earning record
                Earnings.objects.create(
                    driver=driver,
                    delivery=delivery,
                    amount=delivery.estimated_fare,
                    date=timezone.now().date()
                )
            delivery.save()
            messages.success(request, f"Delivery status updated to {status.replace('_', ' ').title()}")
        
        return redirect('driver:my_deliveries')
        
    except (Driver.DoesNotExist, Delivery.DoesNotExist):
        messages.error(request, "Delivery not found")
        return redirect('driver:my_deliveries')

@login_required
def vehicle_info(request):
    try:
        driver = Driver.objects.get(user=request.user)
        
        context = {
            'driver': driver,
        }
        
        return render(request, 'driver/vehicle_info.html', context)
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found")
        return redirect('driver:login')


@login_required
def earnings(request):
    try:
        driver = Driver.objects.get(user=request.user)
        
        earnings_list = Earnings.objects.filter(driver=driver).order_by('-date')
        total_earnings = earnings_list.filter(is_paid=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
        pending_earnings = earnings_list.filter(is_paid=False).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        # Monthly earnings (SQLite compatible and bug-free)
        monthly_earnings = earnings_list.filter(is_paid=True).extra(
            select={'month': "strftime('%%m', date)"}
        ).values('month').annotate(total=models.Sum('amount')).order_by('month')
        
        context = {
            'driver': driver,
            'earnings_list': earnings_list,
            'total_earnings': total_earnings,
            'pending_earnings': pending_earnings,
            'monthly_earnings': list(monthly_earnings),
        }
        
        return render(request, 'driver/earnings.html', context)
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found")
        return redirect('driver:login')
@login_required
def settings(request):
    try:
        driver = Driver.objects.get(user=request.user)
        
        if request.method == 'POST':
            # Handle profile update
            if 'update_profile' in request.POST:
                driver.user.first_name = request.POST.get('first_name')
                driver.user.last_name = request.POST.get('last_name')
                driver.user.email = request.POST.get('email')
                driver.phone = request.POST.get('phone')
                driver.address = request.POST.get('address')
                driver.city = request.POST.get('city')
                driver.state = request.POST.get('state')
                driver.pincode = request.POST.get('pincode')
                
                if 'profile_image' in request.FILES:
                    driver.profile_image = request.FILES['profile_image']
                
                driver.user.save()
                driver.save()
                
                messages.success(request, "Profile updated successfully")
            
            # Handle password change
            elif 'change_password' in request.POST:
                current_password = request.POST.get('current_password')
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                
                if not request.user.check_password(current_password):
                    messages.error(request, "Current password is incorrect")
                elif new_password1 != new_password2:
                    messages.error(request, "New passwords do not match")
                else:
                    request.user.set_password(new_password1)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, "Password changed successfully")
        
        context = {
            'driver': driver,
        }
        
        return render(request, 'driver/settings.html', context)
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver profile not found")
        return redirect('driver:login')