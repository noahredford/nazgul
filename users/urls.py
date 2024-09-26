from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', views.admin_only_view, name='admin_only_view'),
    path('property-manager/', views.property_manager_view, name='property_manager_view'),
    path('handyman/', views.handyman_view, name='handyman_view'),
    path('client/', views.client_dashboard, name='client_dashboard'),  # Add this for clients
    path('role-redirect/', views.role_based_redirect, name='role_based_redirect'),
]
    # Add any other views you need here




