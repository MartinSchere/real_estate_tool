class UserStats:
    def __init__(self, user):
        self.user = user
        self.user_properties = user.property_set.all()

    @property
    def monthly_cashflow(self):
        res = 0.0
        for p in self.user_properties:
            if p.tenant:
                res += p.tenant.rent_payment
        return res
