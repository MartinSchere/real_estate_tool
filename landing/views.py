from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django import forms

from .models import SubscribedUser
from .forms import RegisterUserForm


class Index(SuccessMessageMixin, CreateView):
    form_class = RegisterUserForm
    template_name = "landing/index.html"
    success_url = "#"
    success_message = "_"
