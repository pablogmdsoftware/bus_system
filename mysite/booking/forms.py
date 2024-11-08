from django.forms import ModelForm
from django.core.exceptions import ValidationError

from .models import Ticket, Travel

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = []
    def clean(self):
        super().clean()
        travel = self.cleaned_data.get("travel_id")
        seat = self.cleaned_data.get("seat_number")
        max_seats = travel.bus_id.seats
        if seat > max_seats or seat == 0:
            raise ValidationError("Choose a valid seat.")


