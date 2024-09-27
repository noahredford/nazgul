from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']  # Allow admin to change roles

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))



class Meta:
    model = CustomUser
    fields = ['username', 'email', 'role']  # Adjust fields as needed
    widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }


User = get_user_model()

class SignUpForm(UserCreationForm):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('PROPERTY_MANAGER', 'Property Manager'),
        ('HANDYMAN', 'Handyman'),
        ('CLIENT', 'Client'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Select Your Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']  # Added role field here