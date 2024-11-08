from django.contrib import admin

from .models import Customer, Bus, PassType, Pass, Travel, Ticket
from .forms import TicketForm

admin.site.register(Customer)
admin.site.register(Bus)
admin.site.register(PassType)
admin.site.register(Pass)
admin.site.register(Travel)

class TicketAdmin(admin.ModelAdmin):
    form = TicketForm

admin.site.register(Ticket,TicketAdmin)