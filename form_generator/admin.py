from django.contrib import admin

from .models import Form, Field, Submission

admin.site.register([Form, Field, Submission])
# Register your models here.
