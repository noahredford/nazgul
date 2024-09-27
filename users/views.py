from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser  # Import your custom user model

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

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'admin/edit_user.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('admin_dashboard')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    users = CustomUser.objects.all()
    user_count = users.count()  # Total users
    active_users = users.filter(is_active=True).count()  # Active users
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]  # Recent sign-ups
    return render(request, 'dashboard/admin-dashboard.html', {
        'user_count': user_count,
        'active_users': active_users,
        'recent_users': recent_users,
    })

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