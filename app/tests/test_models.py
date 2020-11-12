from datetime import date

from djmoney.money import Money

from django.test import Client, TestCase
from django.contrib.auth.models import User

from app.models import Property, Loan, Tenant


class TestModels(TestCase):
    def setUp(self):
        mock_user = User.objects.create(username="test", password="test")
        self.mock_properties = (
            Property.objects.create(user=mock_user, address="", bought_for=Money(280_000, 'USD'), property_type='Co', owned_since=date(
                2003, 12, 12), estimated_value=Money(300_000, 'USD'), property_taxes=Money(300, 'USD'), insurance=Money(150, 'USD')),
            Property.objects.create(user=mock_user, address="1", bought_for=Money(350_000, 'USD'), property_type='In', owned_since=date(
                2010, 10, 10), estimated_value=Money(400_000, 'USD'), property_taxes=Money(400, 'USD'), insurance=Money(135, 'USD')),
            Property.objects.create(user=mock_user, address="2", bought_for=Money(375_000, 'USD'), property_type='Re', owned_since=date(
                2003, 5, 5), estimated_value=Money(500_000, 'USD'), property_taxes=Money(500, 'USD'), insurance=Money(160, 'USD')),
            Property.objects.create(user=mock_user, address="3", bought_for=Money(100_000, 'USD'), property_type='Rt', owned_since=date(
                2009, 10, 12), estimated_value=Money(240_000, 'USD'), property_taxes=Money(240, 'USD'), insurance=Money(175, 'USD')),
            Property.objects.create(user=mock_user, address="4", bought_for=Money(600_000, 'USD'), property_type='Co', owned_since=date(
                2018, 12, 12), estimated_value=Money(840_000, 'USD'), property_taxes=Money(800, 'USD'), insurance=Money(150, 'USD')),
        )
        self.mock_loans = (
            Loan.objects.create(rental_property=self.mock_properties[0], term=30, down_payment=Money(
                28_000, 'USD'), interest_rate=4.00),
            Loan.objects.create(rental_property=self.mock_properties[1], term=15, down_payment=Money(
                35_000, 'USD'), interest_rate=3.75),
            Loan.objects.create(rental_property=self.mock_properties[2], term=15, down_payment=Money(
                40_000, 'USD'), interest_rate=4.25),
            Loan.objects.create(rental_property=self.mock_properties[3], term=20, down_payment=Money(
                10_000, 'USD'), interest_rate=3.375),
            Loan.objects.create(rental_property=self.mock_properties[4], term=30, down_payment=Money(
                90_000, 'USD'), interest_rate=5.00)
        )
        self.mock_tenants = (
            Tenant.objects.create(
                rental_property=self.mock_properties[0], name="James", email="james@gmail.com", rent_payment=Money(2000, 'USD')),
            Tenant.objects.create(
                rental_property=self.mock_properties[1], name="John", email="john@gmail.com", rent_payment=Money(2200, 'USD')),
            Tenant.objects.create(
                rental_property=self.mock_properties[2], name="Juliet", email="juliet@gmail.com", rent_payment=Money(2400, 'USD')),
            Tenant.objects.create(
                rental_property=self.mock_properties[3], name="Peter", email="peter@gmail.com", rent_payment=Money(1800, 'USD')),
            Tenant.objects.create(
                rental_property=self.mock_properties[4], name="Marie", email="marie@gmail.com", rent_payment=Money(3950, 'USD')),
        )

    def test_property_cashflow(self):
        self.assertAlmostEqual(self.mock_properties[0].get_net_cashflow(), Money(
            347, 'USD'), msg="Net cashflow yields wrong result.", delta=Money(20, 'USD'))
        self.assertAlmostEqual(self.mock_properties[1].get_net_cashflow(
        ), Money(-625.75, 'USD'), msg="Net cashflow yields wrong result.", delta=Money(20, 'USD'))
        self.assertAlmostEqual(self.mock_properties[2].get_net_cashflow(
        ), Money(-780, 'USD'), msg="Net cashflow yields wrong result.", delta=Money(20, 'USD'))
        self.assertAlmostEqual(self.mock_properties[3].get_net_cashflow(), Money(
            869, 'USD'), msg="Net cashflow yields wrong result.", delta=Money(20, 'USD'))
        self.assertAlmostEqual(self.mock_properties[4].get_net_cashflow(), Money(
            263, 'USD'), msg="Net cashflow yields wrong result.", delta=Money(20, 'USD'))

    def test_property_equity(self):
        self.assertAlmostEqual(self.mock_loans[0].get_total_equity(), Money(
            152_412.94, 'USD'), delta=Money(1000, 'USD'))
        self.assertAlmostEqual(self.mock_loans[1].get_total_equity(), Money(
            274_849.16, 'USD'), delta=Money(2000, 'USD'))
