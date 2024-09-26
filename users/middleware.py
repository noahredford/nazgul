from django.shortcuts import redirect

class RoleBasedAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Redirect all non-admins away from admin-specific URLs
        if request.path.startswith('/admin-only/') and not request.user.is_superuser:
            return redirect('home')  # Redirect to home if not an admin

        response = self.get_response(request)
        return response