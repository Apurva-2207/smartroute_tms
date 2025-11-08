# smart_route/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


@login_required
def settings_view(request):
    """
    Redirect user to appropriate dashboard based on profile presence.
    """
    # If user is a customer (has CustomerProfile), go to customer dashboard
    if hasattr(request.user, 'customerprofile'):
        return redirect('customer:dashboard')
    # Add checks for other profile types if you have them
    # Fallback: redirect to home
    return redirect('home')