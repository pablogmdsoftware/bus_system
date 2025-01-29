from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, date, timedelta
from dateutil import tz
from booking.models import Travel, Bus, CITIES

class Command(BaseCommand):
    """
    This command is made for creating and adding a ton of travels into de database. It checks if
    there are enough travels created per day in the next 10 days. If not, it will create up to
    7 travels in all possible routes.
    """
    def handle(self, *args, **kwargs):
        tzinfo = tz.tzutc()
        for n in range(1,11):
            day = date.today() + timedelta(days=n)
            if len(Travel.objects.filter(schedule__date=day)) > 100:
                continue
            else:
                schedules = (
                    datetime(day.year,day.month,day.day,hour=9,minute=0,tzinfo=tzinfo),
                    datetime(day.year,day.month,day.day,hour=11,minute=0,tzinfo=tzinfo),
                    datetime(day.year,day.month,day.day,hour=13,minute=0,tzinfo=tzinfo),
                    datetime(day.year,day.month,day.day,hour=15,minute=0,tzinfo=tzinfo),
                    datetime(day.year,day.month,day.day,hour=17,minute=0,tzinfo=tzinfo),
                    datetime(day.year,day.month,day.day,hour=19,minute=0,tzinfo=tzinfo),
                )
                for origin in CITIES.keys():
                    n = 0
                    for destination in CITIES.keys():
                        if origin == destination:
                            continue
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