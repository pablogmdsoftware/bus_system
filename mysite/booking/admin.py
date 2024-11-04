from django.contrib import admin

from .models import Customer, Bus, PassType, Pass, Travel, Ticket

admin.site.register(Customer)
admin.site.register(Bus)
admin.site.register(PassType)
admin.site.register(Pass)
admin.site.register(Travel)
admin.site.register(Ticket)