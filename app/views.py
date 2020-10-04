from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django import forms

from django.views.generic import ListView
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User

from multi_form_view import MultiFormView

from .models import Property, Loan, Tenant, Setting
from .forms import UserRegisterForm, LoanForm, PropertyForm, TenantForm
from .user_settings import PropertyFilterSetting, CreditScoreSetting
from .filters import PropertyFilter, PropertyFilterWithoutTenant

from .stats import UserStats
from .utils import get_property_image
from .zillow import get_estimated_value, get_mortgage

from user_settings.utils import get_user_setting, set_user_setting

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


@login_required
def index(request):
    properties = Property.objects.filter(user=request.user)
    property_list_limit = 4
    ctx = {
        'stats': UserStats(user=request.user),
        'properties': properties[:property_list_limit]
    }
    return render(request, 'app/index.html', ctx)

# PROPERTIES


class PropertyListView(LoginRequiredMixin, FilterView):
    template_name = 'app/property_list.html'
    context_object_name = 'properties'

    def get_filterset_class(self):
        print(get_user_setting('filter_by_tenants', request=self.request))
        return PropertyFilterWithoutTenant if not get_user_setting('filter_by_tenants', request=self.request)['value'] else PropertyFilter


class PropertyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Property
    form_class = PropertyForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = get_property_image(form.instance)
        return super().form_valid(form)


class PropertyEditView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Property
    success_message = 'Changes saved successfully'
    form_class = PropertyForm

    def get_object(self, *args):
        obj = super().get_object()
        obj.estimated_value = get_estimated_value(obj)
        obj.save()
        return obj

    def form_valid(self, form):
        form.instance.image_url = get_property_image(form.instance)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user

# LOANS

class LoanEditView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Loan
    form_class = LoanForm
    success_message = 'Changes saved successfully'

    def test_func(self):
        return self.request.user == self.get_object().property.user


class LoanListView(LoginRequiredMixin, FilterView):
    model = Loan
    context_object_name = 'tenants'
    template_name = 'app/loan_list.html'
    filterset_fields = ['name', 'rent_payment']


class LoanCreateView(LoginRequiredMixin, CreateView):
    model = Loan
    form_class = LoanForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.monthly_payment = get_mortgage(instance)

        return super().form_valid(instance)

# TENANTS

class TenantListView(LoginRequiredMixin, FilterView):
    model = Tenant
    context_object_name = 'tenants'
    template_name = 'app/tenant_list.html'
    filterset_fields = ['name', 'rent_payment']


class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm


class TenantEditView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
    success_message = "Tenant has been registered successfully"

    def get_success_url(self):
        prop = self.get_object().rental_property
        return prop.get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().rental_property.user
    
# SETTINGS

class SettingsView(MultiFormView, LoginRequiredMixin):
    template_name = 'app/settings.html'
    form_classes = {
        'property_filter_setting':PropertyFilterSetting,
        'credit_score_setting':CreditScoreSetting,
    }
    success_url = '/settings/'

    def get_initial(self):
        initial = {
            'property_filter_setting': {
            'filter_by_loans':get_user_setting('filter_by_loans', request=self.request)['value'],
            'filter_by_tenants':get_user_setting('filter_by_tenants', request=self.request)['value'],
        }, 
            'credit_score_setting': {
                'credit_score':get_user_setting('credit_score', request=self.request)['value']
        }}
        return initial
    
    def forms_valid(self, forms):
        #print(forms['property_filter_setting'].cleaned_data)
        for key, value in forms.items():
            for k, v in value.cleaned_data.items():
                try:
                    set_user_setting(k, v, request=self.request)
                except IntegrityError:
                    pass
        messages.success(self.request, "Changes saved successfully")
        return super().forms_valid(forms)


"""
@login_required
def SettingsView(request):
    forms = []
    if request.method == 'POST':
        forms += PropertyFilterSetting(request.POST)
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                set_user_setting(k, v, request=request)
        
    else:
        initial = {
            'filter_by_loans':bool(get_user_setting('filter_by_loans', request=request)['value']),
            'filter_by_tenants':bool(get_user_setting('filter_by_tenants', request=request)['value']),
        }

        forms += PropertyFilterSetting(initial=initial)

    return render(request, 'app/settings.html', {'forms' : forms})
 """