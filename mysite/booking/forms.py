from django import forms
from django.core.exceptions import ValidationError

from datetime import date
from dateutil.relativedelta import relativedelta

from .models import Ticket, Travel, Pass
from .models import CITIES

class TicketForm(forms.ModelForm):
    """
    Ticket form created to add complex validators like prohibit to take a seat 
    that the bus does not have.
    """
    class Meta:
        model = Ticket
        fields = ["customer","travel","seat_number","price"]
    def clean(self):
        super().clean()
        travel = self.cleaned_data.get("travel")
        seat = self.cleaned_data.get("seat_number")
        max_seats = travel.bus.seats
        if seat > max_seats or seat == 0:
            raise ValidationError(f"Choose a valid seat ({max_seats} max)")

class PassForm(forms.ModelForm):
    """
    Pass form to prohibit selection of cities if the pass is multi route.
    """
    class Meta:
        model = Pass
        exclude = []
    def clean(self):
        super().clean()
        if self.cleaned_data.get("pass_type").is_multi_route == True:
            if self.cleaned_data.get("first_city") or self.cleaned_data.get("second_city"):
                raise ValidationError("The pass is multi route, do not add cities")

class SearchTravelForm(forms.Form):
    """
    Main travel search engine in the system. It is displayed in the main page, travel.
    A customer can use this form in order to search available tickets for a route and 
    a particular date.
    """
    origin = forms.ChoiceField(choices=CITIES)
    destination = forms.ChoiceField(choices=CITIES)  
    date = forms.DateField()

class BuyTicketForm(SearchTravelForm):
    """
    Inherits from SearchTravelForm. Apart from base field it has time and seat in order
    to allow a customer to search a specific travel and choose a unique seat.
    """
    time = forms.TimeField()
    seat = forms.IntegerField()