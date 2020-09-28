import django_filters

from django import forms

from .models import Property, Loan, Tenant

from djmoney.models.fields import MoneyField
from django.db import models

class PropertyFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(PropertyFilter, self).__init__(*args, **kwargs)

        strings_to_replace = ("loan", "tenant")

        for string in strings_to_replace:
            for k, f in self.filters.items():
                if string in f.field_name:
                    formatted_name = f.field_name.replace((string + "__"), " ").replace("_", " ")
                    self.filters[k].label = formatted_name

    class Meta:
        model = Property
        fields = {
            'address': ['icontains'],
            'estimated_value': ['exact'],
            'property_type': ['exact'],
            'bought_for' : ['exact'],
            'loan__interest_rate': ['exact'],
            'loan__down_payment': ['exact'],
            'loan__program' : ['exact'],
            'loan__monthly_payment': ['exact'],
            'tenant__name': ['icontains'],
            'tenant__rent_payment': ['exact']
        }

        filter_overrides = {
            MoneyField: {
                'filter_class': django_filters.RangeFilter,
                'extra': lambda f: {
                    'widget': django_filters.widgets.RangeWidget(attrs={'class':'form-control flex-child', 'style':'width:48%'}),
                },
            },
            models.FloatField: {
                'filter_class': django_filters.RangeFilter,
                'extra': lambda f: {
                    'widget': django_filters.widgets.RangeWidget(attrs={'class':'form-control flex-child', 'style':'width:48%'}),
                },
            },
        }

