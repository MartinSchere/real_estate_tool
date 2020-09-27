from django.db import models


class SubscribedUser(models.Model):
    email = models.EmailField(max_length=254)
    subscribed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
