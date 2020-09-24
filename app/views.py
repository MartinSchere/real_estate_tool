from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from django.views.generic import ListView
from django_filters.views import FilterView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Property, Loan
from .forms import UserRegisterForm, LoanEditForm, PropertyCreateForm, TenantCreateForm

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


class PropertyListView(FilterView):
    template_name = 'app/property_list.html'
    context_object_name = 'properties'
    model = Property
    filterset_fields = ['property_type',
                        'estimated_value', 'address', 'owned_since']


@login_required
def PropertyCreateView(request):
    if request.method == 'POST':
        form = PropertyCreateForm(request.POST)

        if form.is_valid():
            new_property = form.save(commit=False)
            new_property.user = request.user
            new_property.image_url = get_property_image(new_property)
            new_property.save()

            return redirect(new_property)

    else:
        form = PropertyCreateForm()
    return render(request, 'app/property_form.html', {'form': form})


class PropertyEditView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Property
    success_message = 'Changes saved successfully'
    form_class = PropertyCreateForm

    def get_object(self, *args):
        obj = super().get_object()
        obj.estimated_value = get_estimated_value(obj)
        obj.save()
        return obj

    def test_func(self):
        return self.request.user == self.get_object().user

# LOANS


class LoanEditView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    template_name = 'app/loan_edit.html'
    model = Loan
    form_class = LoanEditForm
    success_message = 'Changes saved successfully'

    def test_func(self):
        return self.request.user == self.get_object().property.user


# TENANTS
@login_required
def TenantCreateView(request):
    if request.method == 'POST':
        form = TenantCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(new_property)

    else:
        form = TenantCreateForm()
    return render(request, 'app/tenant_form.html', {'form': form})
