class UserStats:
    def __init__(self, user):
        self.user = user
        self.user_properties = user.property_set.all()

    @property
    def monthly_net_income(self):
        res = 0.0
        for p in self.user_properties:
            print(p)
            # res -= p.loan.
            if p.tenant:
                res += p.tenant.rent_payment
        return res
