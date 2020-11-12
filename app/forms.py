import json
from django import forms
from django.forms import NumberInput
from django.forms import inlineformset_factory

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from djmoney.forms.widgets import MoneyWidget
from django_google_maps import widgets as map_widgets

from .models import Property, Loan, Tenant


class CustomMoneyWidget(MoneyWidget):
    template_name = 'widgets/money.html'

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'type': 'number', 'class': 'form-control'}
        super().__init__(*args, **kwargs)


class PercentageWidget(NumberInput):
    template_name = 'widgets/percentage.html'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']


class PropertyForm(forms.ModelForm):

    class Meta:
        model = Property
        fields = ['address', 'owned_since',
                  'geolocation', 'bought_for', 'estimated_value', 'property_type', 'insurance', 'property_taxes']
        widgets = {
            'address':  map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap', 'data-autocomplete-options': json.dumps({
                'componentRestrictions': {'country': 'us'}
            })}),
            'geolocation': forms.HiddenInput(),
            'owned_since': forms.DateInput(attrs={
                'placeholder': 'YYYY-MM-DD'
            }),
            'bought_for': CustomMoneyWidget(),
            'estimated_value': CustomMoneyWidget(),
            'insurance': CustomMoneyWidget(),
            'property_taxes': CustomMoneyWidget(),
        }


class LoanCreateForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['interest_rate', 'term', 'down_payment']
        widgets = {
            'down_payment': CustomMoneyWidget(),
            'interest_rate': PercentageWidget()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['term'].label = "Term (years)"


class LoanEditForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['rental_property', 'interest_rate', 'term', 'down_payment']
        widgets = {
            'down_payment': CustomMoneyWidget(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['term'].label = "Term (years)"


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ('rental_property',)
        widgets = {
            'rent_payment': CustomMoneyWidget(),
        }
