from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.views.generic import ListView
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .models import Property, Loan, Tenant
from .forms import UserRegisterForm, LoanForm, PropertyForm, TenantForm

from .stats import UserStats
from .utils import get_property_image, get_estimated_value


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
    model = Property
    filterset_fields = ['property_type',
                        'estimated_value', 'address', 'owned_since']


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

# TENANTS


class TenantListView(LoginRequiredMixin, FilterView):
    model = Tenant
    context_object_name = 'tenants'
    template_name = 'app/tenant_list.html'
    filterset_fields = ['name', 'rent_payment']


class TenantCreateView(LoginRequiredMixin, CreateView):
    model = Tenant
    form_class = TenantForm


class TenantEditView(LoginRequiredMixin, UpdateView):
    model = Tenant
    form_class = TenantForm
