from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
     path('admin-dashboard/', views.admin_only_view, name='admin_only_view'),
    path('property-manager/', views.property_manager_view, name='property_manager_view'),
    path('handyman/', views.handyman_view, name='handyman_view'),
    path('client/', views.client_dashboard, name='client_dashboard'),  # Add this for clients
    path('role-redirect/', views.role_based_redirect, name='role_based_redirect'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
]
    # Add any other views you need here




