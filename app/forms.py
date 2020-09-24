from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from djmoney.forms.widgets import MoneyWidget
from django_google_maps import widgets as map_widgets

import django_filters

from .models import Property, Loan, Tenant


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']


class PropertyFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Property
        fields = ['address', 'owned_since', 'geolocation', 'bought_for']


class CustomMoneyWidget(MoneyWidget):
    template_name = 'widgets/money.html'


class PropertyCreateForm(forms.ModelForm):

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


class LoanEditForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LoanEditForm, self).__init__(*args, **kwargs)

        amount, currency = self.fields['amount'].fields

        self.fields['amount'].widget = CustomMoneyWidget(
            amount_widget=amount.widget, currency_widget=currency.widget,
            attrs={'class': 'form-control'})


class TenantCreateForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
        widgets = {
            'rent_payment': CustomMoneyWidget(attrs={'class': 'form-control'})
        }
