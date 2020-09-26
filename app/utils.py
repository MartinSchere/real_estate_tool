import os
import requests

from django.conf import settings

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import google_streetview.api

import reverse_geocoder as rg


PROPERTY_IMAGE_PARAMS = {
    'size': '600x300',
    'heading': '0',
    'pitch': '0',
    'key': settings.GOOGLE_MAPS_API_KEY
}


def percentage_validator(value):
    if not (value > 0 and value < 100):
        raise ValidationError(
            _('%(value)s must be between 0 and 100'),
            params={'value': value},
        )


def reverse_geocode(coords):
    return rg.search((coords.lat, coords.lon))


def get_property_image(prop, **params):
    PROPERTY_IMAGE_PARAMS['location'] = str(prop.geolocation)

    for k, v in params:
        assert k in PROPERTY_IMAGE_PARAMS.keys()
        PROPERTY_IMAGE_PARAMS[k] = v

    res = google_streetview.api.results([PROPERTY_IMAGE_PARAMS])
    base_url = 'https://maps.googleapis.com/maps/api/streetview'
    try:
        res = requests.get(base_url, params=PROPERTY_IMAGE_PARAMS)
        return res.url
    except:
        return


def get_estimated_value(obj):
    property_location = obj.geolocation
    address = obj.address.split(",")[0]
    url = 'http://www.zillow.com/webservice/GetSearchResults.htm'
    rev_geocoded = reverse_geocode(property_location)[0]
    citystatezip = rev_geocoded['admin1']
    """
    res = requests.get(url, params={'zws-id': settings.ZWS_ID,
                                    'address': address,
                                    'citystatezip': citystatezip})
    print(res.text, res.url)
    """
