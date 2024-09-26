from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    print("Dashboard view is being called.")  # Debugging: to verify view is hit
    return render(request, 'dashboard/admin.html')  # Force render the admin.html for now
