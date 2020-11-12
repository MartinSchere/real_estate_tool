from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django import forms

from django.views.generic import ListView, View
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User

from multi_form_view import MultiFormView, MultiModelFormView

from .models import Property, Loan, Tenant
from .forms import UserRegisterForm, LoanCreateForm, LoanEditForm, PropertyForm, TenantForm
from .user_settings import PropertyFilterSetting, CreditScoreSetting
from .filters import PropertyFilter, PropertyFilterWithoutTenant

from .stats import UserStats
from .utils import get_property_image
from .zillow import get_estimated_value

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


@login_required
def chart_data_api(request, chart):
    ctx = {
        'labels': [],
        'data': []
    }
    user_properties = Property.objects.filter(user=request.user)
    if chart == "income-chart":
        for p in user_properties:
            ctx['labels'] += p.address.split(",")[0],
            # appending because of TypeError
            ctx['data'].append(p.get_net_cashflow().amount)

    if chart == "total-expense-chart":
        ctx['labels'] += ['Property taxes', 'Mortgage', 'Insurance']
        ctx['data'] += [sum((p.property_taxes for p in user_properties)).amount,
                        sum((p.loan.monthly_payment for p in user_properties)).amount,
                        sum((p.insurance for p in user_properties)).amount]

    if chart == "property-expenses-chart":
        for p in user_properties:
            ctx['labels'] += p.address.split(",")[0],
            ctx['data'].append(p.get_total_expenses().amount)

    return JsonResponse(ctx)


# PROPERTIES


class PropertyListView(LoginRequiredMixin, FilterView):
    template_name = 'app/property_list.html'
    context_object_name = 'properties'
    paginate_by = 5

    def get_queryset(self):
        return Property.objects.filter(user=self.request.user)

    def get_filterset_class(self):
        return PropertyFilterWithoutTenant if not get_user_setting('filter_by_tenants', request=self.request)['value'] else PropertyFilter


class PropertyCreateView(LoginRequiredMixin, SuccessMessageMixin, MultiModelFormView):
    form_classes = {'property_form': PropertyForm,
                    'loan_form': LoanCreateForm,
                    'tenant_form': TenantForm}
    template_name = 'app/property_create.html'
    success_message = "Property added successfully"

    def forms_valid(self, forms):
        prop = forms['property_form'].instance
        prop.user = self.request.user
        prop.image_url = get_property_image(prop)

        loan = forms['loan_form'].instance
        loan.rental_property = prop

        forms['tenant_form'].instance.rental_property = prop
        saved_prop = forms['property_form'].save()

        self.success_url = reverse(
            'property_edit', kwargs={'pk': saved_prop.id})
        return super().forms_valid(forms)


class PropertyEditView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Property
    success_message = 'Changes saved successfully'
    form_class = PropertyForm
    template_name = "app/property_edit.html"

    def form_valid(self, form):
        form.instance.image_url = get_property_image(form.instance)
        return super().form_valid(form)

    def test_func(self):
        return self.request.user == self.get_object().user


class PropertyDeleteView(DeleteView, UserPassesTestMixin):
    model = Property
    success_url = reverse_lazy('property_list')

    def test_func(self):
        return self.request.user == self.get_object().user

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


# LOANS


class LoanEditView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Loan
    form_class = LoanEditForm
    success_message = 'Changes saved successfully'

    def test_func(self):
        return self.request.user == self.get_object().rental_property.user


class LoanListView(LoginRequiredMixin, FilterView):
    model = Loan
    context_object_name = 'tenants'
    template_name = 'app/loan_list.html'
    filterset_fields = ['name', 'rent_payment']


class LoanCreateView(LoginRequiredMixin, CreateView):
    model = Loan
    form_class = LoanCreateForm

    def form_valid(self, form):
        instance = form.save(commit=False)

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

# EXPENSE TABLE


class ExpenseTableView(View):
    def get(self, request):
        user_properties = Property.objects.filter(user=request.user)
        mortgage_sum = sum(
            (p.loan.monthly_payment for p in user_properties)
        )
        other_sum = sum(
            (p.property_taxes + p.insurance for p in user_properties)
        )
        ctx = {
            'properties': user_properties,
            'total': mortgage_sum + other_sum
        }
        return render(request, 'app/expense_table.html', ctx)

# SETTINGS


class SettingsView(MultiFormView, LoginRequiredMixin):
    template_name = 'app/settings.html'
    form_classes = {
        'property_filter_setting': PropertyFilterSetting,
        'credit_score_setting': CreditScoreSetting,
    }
    success_url = '/settings/'

    def get_initial(self):
        initial = {
            'property_filter_setting': {
                'filter_by_loans': get_user_setting('filter_by_loans', request=self.request)['value'],
                'filter_by_tenants': get_user_setting('filter_by_tenants', request=self.request)['value'],
            },
            'credit_score_setting': {
                'credit_score': get_user_setting('credit_score', request=self.request)['value']
            }}
        return initial

    def forms_valid(self, forms):
        # print(forms['property_filter_setting'].cleaned_data)
        for key, value in forms.items():
            for k, v in value.cleaned_data.items():
                try:
                    set_user_setting(k, v, request=self.request)
                except IntegrityError:
                    pass
        messages.success(self.request, "Changes saved successfully")
        return super().forms_valid(forms)
