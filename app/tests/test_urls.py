from django.test import SimpleTestCase
from django.urls import reverse, resolve

from app.views import (SignUpView, index, PropertyListView, PropertyCreateView, PropertyEditView,
                       LoanEditView, LoanListView, LoanCreateView, TenantListView, SettingsView)


class TestUrls(SimpleTestCase):
    """
    Test whether all the naming is correct
    """

    def test_index_url(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_properties_urls(self):
        list_url = reverse('property_list')
        create_url = reverse('property_create')
        detail_url = reverse('property_edit', args=[1])

        self.assertEquals(resolve(list_url).func.view_class, PropertyListView)
        self.assertEquals(resolve(create_url).func.view_class,
                          PropertyCreateView)
        self.assertEquals(
            resolve(detail_url).func.view_class, PropertyEditView)

    def test_loans_urls(self):
        list_url = reverse('loan_list')
        create_url = reverse('loan_create')
        detail_url = reverse('loan_edit', args=[1])

        self.assertEquals(resolve(list_url).func.view_class, LoanListView)
        self.assertEquals(resolve(create_url).func.view_class,
                          LoanCreateView)
        self.assertEquals(
            resolve(detail_url).func.view_class, LoanEditView)

    def test_tenants_urls(self):
        list_url = reverse('tenant_list')
        create_url = reverse('property_create')
        detail_url = reverse('property_edit', args=[1])

        self.assertEquals(resolve(list_url).func.view_class, TenantListView)
        """
        self.assertEquals(resolve(create_url).func.view_class,
                          PropertyCreateView)
        self.assertEquals(
            resolve(detail_url).func.view_class, PropertyEditView)
        """

    def test_settings_urls(self):
        url = reverse('settings')
        self.assertEquals(resolve(url).func.view_class, SettingsView)
