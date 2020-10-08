import requests

from .utils import reverse_geocode
from django.conf import settings

BASE_URL = 'http://www.zillow.com/webservice/'
API_URLS = {
    'GetZestimate': 'https://api.bridgedataoutput.com/api/v2/zestimates'
}


def get_estimated_value(prop):
    property_location = prop.geolocation
    address = prop.address.split(",")[0]
    rev_geocoded = reverse_geocode(property_location)[0]
    citystatezip = rev_geocoded['admin1']
    res = requests.get(API_URLS['GetZestimate'], params={
        'access_token': settings.ZILLOW_ACCESS_TOKEN,
        'address': address, })
    return 0.0
