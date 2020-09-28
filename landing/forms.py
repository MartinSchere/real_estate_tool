from django import forms
from .models import SubscribedUser


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = SubscribedUser
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email me when it is ready'
            })
        }
        labels = {
            'email': ''
        }
