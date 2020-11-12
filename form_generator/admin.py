from django.contrib import admin

from .models import Form, Field

admin.site.register([Form, Field])
# Register your models here.
