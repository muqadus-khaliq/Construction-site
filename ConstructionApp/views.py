from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Service, Project,Review
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages

def index(request):
    services = Service.objects.all()
    projects = Project.objects.all().order_by('-start_date')[:6]
    clients = Client.objects.all()
    context = {
        'services': services,
        'projects': projects,
        'clients' : clients,
    }
    return render(request, 'index.html', context)
# Display all services
def service_list(request):
    services = Service.objects.all()
    return render(request, 'Services.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)  
    return render(request, 'service_detail.html', {'service': service})

def project_list(request):
    projects = Project.objects.all()
    # statuses = dict(Project.STATUS_CHOICES)  # Convert STATUS_CHOICES to a dictionary for easy lookup
    return render(request, 'project_list.html', {
        'projects': projects,
        # 'project_statuses': statuses.items(),  # Pass as items for easy iteration in the template
        # 'status_display': None  # Indicates we are viewing all projects
    })

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

    
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})
def review_detail(request, review_id):
    project = get_object_or_404(Review, id=review_id)
    return render(request, 'review_detail.html', {'review': review})
 
def client_list(request):
    clients = Client.objects.all()   
    return render(request, 'client.html', {'clients': clients}) 

# Display a single client's details
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)  # Fixed typo here
    return render(request, 'client_detail.html', {'client': client})


from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_backends

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        # Specify the backend explicitly
        backend = get_backends()[0]  # Use the first authentication backend
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
        
        auth_login(request, user)
        messages.success(request, "Signup successful!")
        return redirect('index')

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')
