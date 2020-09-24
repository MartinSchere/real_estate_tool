from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name="index"),
    # Properties
    path('property_list', views.PropertyListView.as_view(), name="property_list"),
    path('property/<int:pk>', views.PropertyEditView.as_view(),
         name="property_edit"),
    path('property_create/', views.PropertyCreateView,
         name="property_create"),
    # Loans
    path('loan_edit/<int:pk>', views.LoanEditView.as_view(), name="loan_edit"),
    # Tenants
    path('loan_create/', views.TenantCreateView, name="tenant_create")

]
