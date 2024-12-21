from django.contrib import admin

from .models import Customer, Bus, PassType, Pass, Travel, Ticket
from .models import CITIES
from .forms import TicketForm, PassForm

from datetime import datetime, timedelta, timezone

admin.site.register(Customer)
admin.site.register(PassType)
admin.site.register(Bus)

class TicketAdmin(admin.ModelAdmin):
    form = TicketForm

admin.site.register(Ticket,TicketAdmin)

class PassAdmin(admin.ModelAdmin):
    form = PassForm

admin.site.register(Pass,PassAdmin)

class TravelAdmin(admin.ModelAdmin):
    actions = ["add_travels"]
    def add_travels(self,request,queryset):
        now = datetime.now()
        schedules = (
            datetime(now.year,now.month,now.day+1,hour=12,minute=0,tzinfo=now.tzinfo),
            datetime(now.year,now.month,now.day+1,hour=15,minute=0,tzinfo=now.tzinfo),
            datetime(now.year,now.month,now.day+1,hour=18,minute=0,tzinfo=now.tzinfo),
        )
        for origin in CITIES.keys():
            n = 0
            for destination in CITIES.keys():
                if origin == destination:
                    pass
                else:
                    for schedule in schedules:
                        if len(origin) == 1 and len(str(n)) == 1:
                            bus_id = origin + origin + "0" + str(n)
                        elif len(origin) == 2 and len(str(n)) == 1:
                            bus_id = origin + "0" + str(n)
                        elif len(origin) == 1 and len(str(n)) == 2:
                            bus_id = origin + origin + str(n)
                        elif len(origin) == 2 and len(str(n)) == 2:
                            bus_id = origin + str(n)
                        n += 1
                        bus = Bus.objects.get(bus_id=bus_id)
                        travel = Travel(
                            origin = origin,
                            destination = destination,
                            bus = bus,
                            schedule = schedule,
                            )
                        travel.save()

admin.site.register(Travel,TravelAdmin)