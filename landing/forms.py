from django import forms
from .models import SubscribedUser


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = SubscribedUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email'
            })
        }
        labels = {
            'email': 'Get 20% off on release'
        }
