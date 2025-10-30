# transporter/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TransporterRegistrationForm
from .models import TransporterProfile

def transporter_login(request):
    """
    Handle transporter login functionality
    """
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        if hasattr(request.user, 'transporter_profile'):
            return redirect('transporter:dashboard')
        else:
            messages.warning(request, 'You are logged in but not as a transporter.')
            return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if hasattr(user, 'transporter_profile'):
                login(request, user)
                
                # Handle remember me functionality
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                
                # Redirect to next page if specified, otherwise to dashboard
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('transporter:dashboard')
            else:
                messages.error(request, 'This account is not registered as a transporter.')
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    
    return render(request, 'transporter/login.html')

def transporter_register(request):
    """
    Handle transporter registration
    """
    # If user is already authenticated, redirect appropriately
    if request.user.is_authenticated:
        if hasattr(request.user, 'transporter_profile'):
            return redirect('transporter:dashboard')
        else:
            messages.warning(request, 'You are already logged in with a different account type.')
            return redirect('home')
    
    if request.method == 'POST':
        form = TransporterRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name']
                )
                
                # Create transporter profile
                transporter_profile = TransporterProfile.objects.create(
                    user=user,
                    company_name=form.cleaned_data['company_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    zip_code=form.cleaned_data['zip_code'],
                    vehicle_type=form.cleaned_data['vehicle_type'],
                    license_number=form.cleaned_data['license_number']
                )
                
                # Log the user in
                login(request, user)
                messages.success(request, f'Welcome to SmartRoute, {user.first_name}! Your transporter account has been created successfully.')
                return redirect('transporter:dashboard')
                
            except Exception as e:
                messages.error(request, f'An error occurred during registration: {str(e)}')
        else:
            # Form is invalid, show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = TransporterRegistrationForm()
    
    return render(request, 'transporter/register.html', {'form': form})

@login_required
def transporter_logout(request):
    """
    Handle transporter logout
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def transporter_dashboard(request):
    """
    Transporter dashboard view
    """
    # Ensure user is a transporter
    if not hasattr(request.user, 'transporter_profile'):
        messages.error(request, 'Access denied. Transporter account required.')
        return redirect('home')
    
    transporter_profile = request.user.transporter_profile
    
    # You can add context data here for the dashboard
    context = {
        'transporter': transporter_profile,
        'active_shipments': [],  # Add your actual data here
        'completed_shipments': [],  # Add your actual data here
        'revenue': 0,  # Add your actual data here
    }
    
    return render(request, 'transporter/dashboard.html', context)

def transporter_profile(request):
    """
    Transporter profile management
    """
    if not request.user.is_authenticated or not hasattr(request.user, 'transporter_profile'):
        messages.error(request, 'Please login as a transporter to access this page.')
        return redirect('transporter:login')
    
    transporter_profile = request.user.transporter_profile
    
    if request.method == 'POST':
        # Handle profile updates here
        pass
    
    context = {
        'transporter': transporter_profile
    }
    
    return render(request, 'transporter/profile.html', context)