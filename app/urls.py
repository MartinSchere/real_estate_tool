from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('api/chart-data', views.chart_data_api),

    # Properties

    path('properties/', include([
        path('list', views.PropertyListView.as_view(), name="property_list"),
        path('detail/<int:pk>', views.PropertyEditView.as_view(),
             name="property_edit"),
        path('create/', views.PropertyCreateView.as_view(),
             name="property_create"),
        path('delete/<int:pk>', views.PropertyDeleteView.as_view(),
             name="property_delete"),
    ])),

    # Loans

    path('loans/', include([
        path('list/', views.LoanListView.as_view(), name="loan_list"),
        path('detail/<int:pk>', views.LoanEditView.as_view(), name="loan_edit"),
        path('create/', views.LoanCreateView.as_view(), name="loan_create"),
    ])),

    # Tenants

    path('tenants/', include([
         path('list', views.TenantListView.as_view(), name="tenant_list"),
         path('create/', views.TenantCreateView.as_view(), name="tenant_create"),
         path('detail/<int:pk>', views.TenantEditView.as_view(), name="tenant_edit"),
         path('detail/<int:pk>', views.TenantEditView.as_view(),
              name="tenant_edit_nested"),
         ])),

    # Expense table

    path('expense_table/', views.ExpenseTableView.as_view(), name="expense_table"),

    # Settings

    path('settings/', views.SettingsView.as_view(), name="settings")

]
