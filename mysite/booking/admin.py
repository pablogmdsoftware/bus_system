from django.contrib import admin

from .models import Customer, Bus, PassType, Pass, Travel, Ticket
from .forms import TicketForm, PassForm

admin.site.register(Customer)
admin.site.register(Bus)
admin.site.register(PassType)
admin.site.register(Travel)

class TicketAdmin(admin.ModelAdmin):
    form = TicketForm

admin.site.register(Ticket,TicketAdmin)

class PassAdmin(admin.ModelAdmin):
    form = PassForm

admin.site.register(Pass,PassAdmin)