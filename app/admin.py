from django.contrib import admin

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from .models import Property, Loan, Tenant
#from user_settings.models import UserSettings


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


admin.site.register([Loan, Tenant])
