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


def term_validator(value):
    if not (value > 0 and value <= 30):
        raise ValidationError(
            _('%(value)s must be between 0 and 30'),
            params={'value': value},
        )


def credit_score_validator(value):
    if not (value >= 300 and value <= 850):
        raise ValidationError(
            _('Credit score must be between 300 and 850'),
            params={'value': value},
        )


def reverse_geocode(coords):
    return rg.search((coords.lat, coords.lon))


def is_image_available():
    base_url = 'https://maps.googleapis.com/maps/api/streetview/metadata'
    res = requests.get(base_url, params=PROPERTY_IMAGE_PARAMS)
    return res.json()['status'] != 'ZERO_RESULTS'


def get_property_image(prop, **params):
    PROPERTY_IMAGE_PARAMS['location'] = str(prop.geolocation)

    for k, v in params:
        assert k in PROPERTY_IMAGE_PARAMS.keys()
        PROPERTY_IMAGE_PARAMS[k] = v

    if is_image_available():

        base_url = 'https://maps.googleapis.com/maps/api/streetview'
        try:
            res = requests.get(base_url, params=PROPERTY_IMAGE_PARAMS)
            return res.url
        except:
            return
