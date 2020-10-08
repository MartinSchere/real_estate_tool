import requests

from django.test import SimpleTestCase, Client
from django.urls import reverse
from django.conf import settings

from app.models import Property, Tenant, Loan, Tenant
from app.zillow import API_URLS

import google_streetview.api


class TestApis(SimpleTestCase):

    def setUp(self):
        self.mock_citystatezip = 'Los Angeles, CA'
        self.mock_addresses = (
            '1262 S Longwood Ave',
            '1000 S Westgate Ave',
            '1051 S Sherbourne Dr #1',
            '10900 Wilshire Blvd #1600',
            '10425 Tabor St'
        )

    def test_zillow(self):
        for address in self.mock_addresses:
            res = requests.get(API_URLS['GetZestimate'], params={
                'access_token': settings.ZILLOW_ACCESS_TOKEN, 'address': address
            })
            print(res.text)
            self.assertEquals(res.json()['success'], True)

    def test_google_maps_streetview(self):
        base_url = 'https://maps.googleapis.com/maps/api/streetview'
        res = google_streetview.api.results([{'size': '600x300',
                                              'location': '37.7656048,-122.46229511',
                                              'heading': '0',
                                              'pitch': '0',
                                              'key': settings.GOOGLE_MAPS_API_KEY}])
        metadata = res.metadata[0]
        self.assertEquals(metadata['status'], 'OK')
