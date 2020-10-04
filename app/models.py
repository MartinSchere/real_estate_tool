from django.db import models
from django.conf import settings

from djmoney.models.fields import MoneyField
from django_google_maps import fields as map_fields

from django.contrib.auth.models import User

from django.urls import reverse

from .utils import percentage_validator

PROPERTY_CHOICES = (
    ('Re', 'Residential'),
    ('In', 'Industrial'),
    ('Mi', 'Mixed'),
    ('Rt', 'Retail'),
    ('Co', 'Commercial'),
)


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)
    zws_id = models.CharField(max_length=len(settings.ZWS_ID), null=True)
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=2)
    bought_for = MoneyField(max_digits=20, decimal_places=2,
                            default_currency='USD', null=True, blank=True)
    estimated_value = MoneyField(max_digits=20, decimal_places=2,
                                 default_currency='USD', null=True, blank=True)
    image_url = models.URLField(null=True)
    owned_since = models.DateField()

    def get_absolute_url(self):
        return reverse("property_edit", kwargs={"pk": self.pk})

    class Meta:
        verbose_name_plural = 'properties'

    def __str__(self):
        return str(self.address)


class Loan(models.Model):
    rental_property = models.OneToOneField(Property, on_delete=models.CASCADE)
    down_payment = MoneyField(max_digits=20, decimal_places=2,
                              default_currency='USD')
    total_price = MoneyField(max_digits=20, decimal_places=2,
                             default_currency='USD')
    interest_rate = models.FloatField(validators=[percentage_validator])

    program = models.CharField(max_length=30, choices=(
        ('30F', '30-year-fixed'),
        ('15F', '15-year-fixed'),
        ('51A', '5/1 ARM')
    ))
    monthly_payment = MoneyField(max_digits=20, decimal_places=2,
                              default_currency='USD')

    def get_absolute_url(self):
        return reverse("loan_edit", kwargs={"pk": self.pk})

    def __str__(self):
        return f'loan for {self.amount}'


class Tenant(models.Model):
    rental_property = models.OneToOneField(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    rent_payment = MoneyField(max_digits=20, decimal_places=2,
                              default_currency='USD')

    def get_absolute_url(self):
        return reverse("tenant_edit", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Renovation(models.Model):
    property_renovated = models.ForeignKey(Property, on_delete=models.CASCADE)
    cost = MoneyField(max_digits=20, decimal_places=2,
                      default_currency='USD')

    def __str__(self):
        return f'{self.cost} renovation for {self.property_renovated}'


class Setting(models.Model):
    user = models.ManyToManyField(User, related_name="settings")
    name = models.CharField(max_length=50)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
