from django.contrib import admin

from .models import Customer, Bus, PassType, Pass

admin.site.register(Customer)
admin.site.register(Bus)
admin.site.register(PassType)
admin.site.register(Pass)