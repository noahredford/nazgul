from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser  # Import your custom user model
from django.contrib.admin.models import LogEntry
from django.shortcuts import get_object_or_404
from .forms import UserCreateForm  # Ensure this is added to import the form
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.contrib.auth import login



# Helper function to check if the user is an admin
def is_admin(user):
    return user.role == 'ADMIN'

def admin_only_view(request):
    # Admin Dashboard content
    users = CustomUser.objects.all()
    user_count = users.count()
    return render(request, 'dashboard/admin-dashboard.html', {
        'users': users,
        'user_count': user_count,
    })

# Helper function to check if the user is a property manager
def is_property_manager(user):
    return user.role == 'PROPERTY_MANAGER'

@login_required
def client_dashboard(request):
    return render(request, 'dashboard/client_dashboard.html')

# Property Manager-only view
@login_required
@user_passes_test(is_property_manager)
def property_manager_view(request):
    return render(request, 'dashboard/property_manager_page.html')

# Helper function to check if the user is a handyman
def is_handyman(user):
    return user.role == 'HANDYMAN'

# Handyman-only view
@login_required
@user_passes_test(is_handyman)
def handyman_view(request):
    return render(request, 'dashboard/handyman_page.html')

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser  # Ensure CustomUser is imported
from .forms import UserEditForm  # Ensure the form is imported

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')
def admin_dashboard(request):
    query = request.GET.get('q')
    
    if query:
        users = CustomUser.objects.filter(username__icontains=query) | CustomUser.objects.filter(email__icontains=query)
    else:
        users = CustomUser.objects.all()

    user_count = users.count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]

    return render(request, 'dashboard/admin-dashboard.html', {
        'users': users,
        'user_count': user_count,
        'recent_users': recent_users,
        'query': query,
    })

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(username__icontains=query) | CustomUser.objects.filter(email__icontains=query)
    else:
        users = CustomUser.objects.all()

    user_count = users.count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    
    return render(request, 'dashboard/admin-dashboard.html', {
        'users': users,
        'user_count': user_count,
        'recent_users': recent_users,
        'query': query,  # To keep search term in the input field
    })

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')  # Or however you check for admin role
def admin_dashboard(request):
    users = CustomUser.objects.all()
    user_count = users.count()
    return render(request, 'dashboard/admin-dashboard.html', {
        'users': users,
        'user_count': user_count,
    })

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'admin/edit_user.html', {'form': form, 'user': user})

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')
    return render(request, 'admin/delete_user.html', {'user': user})

# Role-based redirect view
@login_required
def role_based_redirect(request):
    user = request.user
    if user.role == 'ADMIN':
        return redirect('admin_only_view')  # Redirect to the admin dashboard
    elif user.role == 'PROPERTY_MANAGER':
        return redirect('property_manager_view')  # Redirect to the property manager dashboard
    elif user.role == 'HANDYMAN':
        return redirect('handyman_view')  # Redirect to the handyman dashboard
    else:
        return redirect('client_dashboard')  # Default redirect if no matching role

from django.contrib.admin.models import LogEntry

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')
def admin_dashboard(request):
    users = CustomUser.objects.all()
    user_count = users.count()
    recent_logs = LogEntry.objects.order_by('-action_time')[:10]  # Recent log entries

    return render(request, 'dashboard/admin-dashboard.html', {
        'users': users,
        'user_count': user_count,
        'recent_logs': recent_logs,
    })

@login_required
@user_passes_test(lambda user: user.role == 'ADMIN')
def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserCreateForm()

    return render(request, 'admin/add_user.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')  # Change this based on the role or dashboard
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Log in the user immediately after sign-up
            return redirect('role-redirect')  # Redirect to role-based dashboard after signup
    else:
        form = SignUpForm()  # Display empty form for GET requests
    return render(request, 'auth/signup.html', {'form': form})  # Render signup template


