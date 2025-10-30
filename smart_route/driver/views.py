from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import DriverProfile

def driver_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        license_number = request.POST.get('license_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_number = request.POST.get('vehicle_number')
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                
                profile = user.driverprofile
                profile.phone_number = phone
                profile.license_number = license_number
                profile.vehicle_type = vehicle_type
                profile.vehicle_number = vehicle_number
                profile.save()
                
                messages.success(request, 'Driver account created successfully! Please login.')
                return redirect('driver:login')
        else:
            messages.error(request, 'Passwords do not match!')
    
    return render(request, 'driver/register.html')

def driver_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('driver:dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'driver/login.html')

@login_required
def driver_dashboard(request):
    try:
        profile = request.user.driverprofile
    except DriverProfile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile
    }
    return render(request, 'driver/dashboard.html', context)