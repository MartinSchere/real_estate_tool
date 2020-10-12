from decimal import Decimal

from mortgage import Loan as LoanCalc

from django.db import models
from django.conf import settings

from djmoney.models.fields import MoneyField
from django_google_maps import fields as map_fields

from django.contrib.auth.models import User

from django.urls import reverse

from .utils import percentage_validator, term_validator, get_property_image
from .zillow import get_estimated_value

PROPERTY_CHOICES = (
    ('Re', 'Residential'),
    ('In', 'Industrial'),
    ('Mi', 'Mixed'),
    ('Rt', 'Retail'),
    ('Co', 'Commercial'),
)


class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = map_fields.AddressField(max_length=200, unique=True)
    geolocation = map_fields.GeoLocationField(max_length=100)
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=2)
    bought_for = MoneyField(max_digits=20, decimal_places=2,
                            default_currency='USD', null=True, blank=True, help_text="Total value of the property at the moment of purchse")
    estimated_value = MoneyField(max_digits=20, decimal_places=2,
                                 default_currency='USD', null=True, blank=True)
    image_url = models.URLField(null=True)
    owned_since = models.DateField()
    zpid = models.IntegerField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.estimated_value = get_estimated_value(self)

        self.image_url = get_property_image(self)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("property_edit", kwargs={"pk": self.pk})

    def get_net_cashflow(self):
        return self.tenant.rent_payment - self.loan.monthly_payment

    class Meta:
        verbose_name_plural = 'properties'
        ordering = ['id']

    def __str__(self):
        return str(self.address)


class Loan(models.Model):
    rental_property = models.OneToOneField(Property, on_delete=models.CASCADE)
    down_payment = MoneyField(max_digits=20, decimal_places=2,
                              default_currency='USD', help_text="This will be substracted from your initial buying price.")
    term = models.IntegerField(null=True, validators=[term_validator])
    interest_rate = models.FloatField(validators=[
                                      percentage_validator], help_text="Fixed interest rate. ARM support coming soon!")

    monthly_payment = MoneyField(max_digits=20, decimal_places=2,
                                 default_currency='USD')

    def get_loaned_amount(self):
        return self.rental_property.bought_for - self.down_payment

    def save(self, *args, **kwargs):
        principal = self.get_loaned_amount().amount
        loan_obj = LoanCalc(principal=principal,
                            interest=(self.interest_rate/100), term=self.term)
        self.monthly_payment = loan_obj.monthly_payment
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("loan_edit", kwargs={"pk": self.pk})

    def __str__(self):
        return f'loan for {self.rental_property}'


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
