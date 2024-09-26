from django.contrib import admin
from django.urls import path, include  # Include is necessary to link app-level URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),  # Include the URLs from the users app
]
