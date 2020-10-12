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

        return res
