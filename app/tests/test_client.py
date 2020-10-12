from datetime import date
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser, User
from app.models import Property


class TestClient(TestCase):
    def setUp(self):
        self.client = Client()
        self.mock_user = User.objects.create_user(
            username='jamesj1231',
            password='Mypass12!',
            first_name='James',
            email='jamesjohnson@gmail.com',
        )
        self.mock_property = {
            'address': '10425 Tabor St, Los Angeles, California',
            'geolocation': '37.7656048,-122.4622951',
            'bought_for': 400000.00,
            'property_type': 'In',
            'owned_since': date(2002, 12, 12),
            'image_url': 'xxx'
        }
        self.mock_tenant = {
            'name': 'John',
            'rent_payment': 2200.00
        }

    def test_auth(self):

        res = self.client.get('')
        self.assertEquals(res.status_code, 302)

        res = self.client.login(
            username='jamesj1231', password='Mypass12!')
        self.assertTrue(res)

    # def test_create_property(self):
    #     self.client.force_login(self.mock_user)
    #     res = self.client.post(
    #         '/properties/create/', (self.mock_property, self.mock_tenant))
    #     print(res)
    #     assert Property.objects.last() != None, "Property was not created"
    #     self.assertEqual(Property.objects.last().address,
    #                      "10425 Tabor St, Los Angeles, California")

    def test_edit_property(self):
        self.client.force_login(self.mock_user)

        prop = Property.objects.create(
            user=self.mock_user, **self.mock_property)

        new_prop = self.mock_property.copy()
        new_prop['address'] = '10422 Tabor St, Los Angeles, California'

        res = self.client.post(
            reverse('property_edit', kwargs={'pk': prop.pk}), new_prop)
        self.assertEquals(
            Property.objects.last().address, '10422 Tabor St, Los Angeles, California')

    def test_delete_property(self):
        self.client.force_login(self.mock_user)

        prop = Property.objects.create(
            user=self.mock_user, **self.mock_property)

        res = self.client.post(
            reverse('property_delete', kwargs={'pk': prop.pk}))

        self.assertEquals(res.status_code, 302)
