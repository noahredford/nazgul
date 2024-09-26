from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Helper function to check if the user is an admin
def is_admin(user):
    return user.role == 'ADMIN'

# Admin-only view
@login_required
@user_passes_test(is_admin)
def admin_only_view(request):
    return render(request, 'dashboard/admin_page.html')

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