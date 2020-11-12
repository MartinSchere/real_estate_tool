from django.urls import reverse

from django.contrib.auth.models import User
from django.db import models

from django import forms
from .forms import CustomForm
import uuid


class Form(models.Model):
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def applicant_form(self):
        new_fields = {}
        for field in self.field_set.all():
            new_fields[field.question] = forms.CharField(max_length=60)
        form = type('form', (CustomForm,), new_fields)
        return form

    def get_absolute_url(self):
        return reverse("form_edit", kwargs={"pk": self.pk})

    def get_fill_url(self):
        return reverse("form_fill",  kwargs={"pk": self.pk})


class Field(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    question = models.CharField(max_length=40)
    # field_type = models.Charf


class Submission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()
