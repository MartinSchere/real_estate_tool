from django import forms
from user_settings.models import UserSettings 
from .utils import credit_score_validator

class PropertyFilterSetting(forms.Form):
    filter_by_loans = forms.BooleanField(required=False)
    filter_by_tenants = forms.BooleanField(required=False)

class CreditScoreSetting(forms.Form):
    credit_score = forms.IntegerField(validators = [credit_score_validator], required=False)