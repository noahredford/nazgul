from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role']  # Display the role in the user list
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Add the role field to the form
    )

admin.site.register(CustomUser, CustomUserAdmin)
