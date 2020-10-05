import requests

from .utils import reverse_geocode
from django.conf import settings

BASE_URL = 'http://www.zillow.com/webservice/'
API_URLS = {
    'GetSearchResults': BASE_URL + 'GetSearchResults.htm',
    # 'GetMortgageRates': 'https://mortgageapi.zillow.com/getRates'
}


def get_search_results(prop):
    property_location = prop.geolocation
    address = prop.address.split(",")[0]
    rev_geocoded = reverse_geocode(property_location)[0]
    citystatezip = rev_geocoded['admin1']
    res = requests.get(API_URLS['GetSearchResults'], params={
        'zws-id': settings.ZWS_ID,
        'address': address,
        'citystatezip': citystatezip})
    return res.text


def get_estimated_value(prop):
    res = get_search_results(prop)
    print(res)


def get_mortgage(prop):
    res = requests.get(API_URLS['GetMortgageRates'], params={
        'partnerId': settings.ZILLOW_PARTNER_ID
    })
    print(res.json())
