from django.urls import path
from . import views  # Import the views from users

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Ensure dashboard path is correct
]


