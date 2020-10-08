import json
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
            'address':  map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap', 'data-autocomplete-options': json.dumps({
                'componentRestrictions': {'country': 'us'}
            })}),
            'geolocation': forms.HiddenInput(),
            'owned_since': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD'
            }),
            'bought_for': CustomMoneyWidget(attrs={'class': 'form-control'})
        }


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['rental_property']


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ('rental_property',)
        widgets = {
            'rent_payment': CustomMoneyWidget(attrs={'class': 'form-control'})
        }
