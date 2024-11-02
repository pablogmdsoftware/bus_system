from django.contrib import admin

from .models import Customer, Bus, PassType

admin.site.register(Customer)
admin.site.register(Bus)
admin.site.register(PassType)
