from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from datetime import date
from booking.models import Travel, Ticket
from mysite.settings import EMAIL_HOST_USER

class Command(BaseCommand):
    """
    This command deletes all past travels. As the tickets have proteccion against travel
    delection, it deletes past tickets too.
    """
    def handle(self, *args, **kwargs):
        Ticket.objects.filter(purchase_datetime__date__lt=date.today()).delete()
        Travel.objects.filter(schedule__date__lt=date.today()).delete()
        send_mail(
            "[Bus System] Travels have been deleted successfully",
            "",
            EMAIL_HOST_USER,
            ["pablogmdsoftware@gmail.com"],
            )