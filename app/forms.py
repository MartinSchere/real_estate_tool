from django import forms
from django.forms import inlineformset_factory

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from djmoney.forms.widgets import MoneyWidget
from django_google_maps import widgets as map_widgets


from .models import Property, Loan, Tenant, Setting


class CustomMoneyWidget(MoneyWidget):
    template_name = 'widgets/money.html'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ['address', 'owned_since',
                  'geolocation', 'bought_for', 'property_type']
        widgets = {
            'address':  map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'}),
            'geolocation': forms.HiddenInput(),
            'owned_since': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD'
            }),
            'bought_for': CustomMoneyWidget(attrs={'class': 'form-control'})
        }


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['down_payment', 'total_price', 'interest_rate', 'program', 'rental_property']
        widgets = {
            'down_payment': CustomMoneyWidget(attrs={'class': 'form-control'}),
            'total_price': CustomMoneyWidget(attrs={'class': 'form-control'})
        }


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
        widgets = {
            'rent_payment': CustomMoneyWidget(attrs={'class': 'form-control'})
        }
