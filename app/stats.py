from djmoney.money import Money


class UserStats:
    def __init__(self, user):
        self.user = user
        self.user_properties = user.property_set.all()

    @property
    def monthly_net_income(self):

        res = Money(0, 'USD')

        for p in self.user_properties:
            if hasattr(p, 'loan'):
                res -= p.loan.monthly_payment
            if hasattr(p, 'tenant'):
                res += p.tenant.rent_payment
            if hasattr(p, 'property_taxes'):
                res -= p.property_taxes
            if hasattr(p, 'insurance'):
                res -= p.insurance

        return res

    @property
    def gross_worth(self):

        res = 0

        for p in self.user_properties:
            if hasattr(p, 'loan'):
                res += p.loan.get_total_equity()
            else:
                res += p.bought_for.amount

        return res

    @property
    def total_taxes(self):
        return sum((p.property_taxes for p in self.user_properties))

    @property
    def total_home_insurance(self):
        return sum((p.insurance for p in self.user_properties))

    @property
    def total_mortgage(self):
        return sum((p.loan.monthly_payment for p in self.user_properties))

    @property
    def total_rent(self):
        return sum((p.tenant.rent_payment for p in self.user_properties))
