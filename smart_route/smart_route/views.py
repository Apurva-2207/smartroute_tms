from django.shortcuts import render

def home(request):
    # Major modules with links and icons
    modules = [
        {'name': 'Customer', 'url': '/customer/', 'icon': 'images/icons/customer.png'},
        {'name': 'Driver', 'url': '/driver/', 'icon': 'images/icons/driver.png'},
        {'name': 'Transporter', 'url': '/transporter/', 'icon': 'images/icons/transporter.png'},
    ]
    return render(request, 'home.html', {'modules': modules})