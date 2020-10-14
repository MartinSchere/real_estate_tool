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
                res += p.property_taxes
            if hasattr(p, 'insurance'):
                res += p.insurance
        return res

    @property
    def gross_worth(self):

        res = Money(0, 'USD')

        for p in self.user_properties:
            if hasattr(p, 'estimated_value'):
                res += p.estimated_value
            else:
                res += p.bought_for

        return res
