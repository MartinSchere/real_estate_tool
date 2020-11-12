from django.urls import reverse

from django.contrib.auth.models import User
from django.db import models

import uuid


class Form(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def get_absolute_url(self):
        return reverse("form_edit", kwargs={"pk": self.pk})
    
class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    # field_type = models.

class Submission(models.Model):
   pass 