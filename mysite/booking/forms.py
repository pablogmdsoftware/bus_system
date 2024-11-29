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
        fields = ["user","travel","seat_number","price"]
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

    def clean_date(self):
        travel_date = self.cleaned_data["date"]
        if travel_date < date.today():
            raise ValidationError("Past dates are not allowed")
        return travel_date

    def clean(self):
        if self.cleaned_data.get("origin") == self.cleaned_data.get("destination"):
            raise ValidationError("Cities must be different")


class PurchaseTicketForm(SearchTravelForm):
    """
    Inherits from SearchTravelForm. Apart from base field it has time and seat in order
    to allow a customer to search a specific travel and choose an unique seat.
    """
    time = forms.TimeField()
    seat = forms.IntegerField()

class ProfileForm(forms.Form):
    """
    Profile form to validate personal information of an user.
    """
    username = forms.CharField()
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    birth_date = forms.DateField(required=False)
    email = forms.EmailField()
    has_large_family = forms.BooleanField(required=False)
    has_reduced_mobility = forms.BooleanField(required=False)

class PasswordForm(forms.Form):
    """
    Form to change passwords
    """
    old_password = forms.CharField()
    new_password = forms.CharField()
    repeat_password = forms.CharField()

    def clean(self):
        passwords = self.cleaned_data
        if passwords.get("new_password") != passwords.get("repeat_password"):
            raise ValidationError("The passwords do not match")

class SingupForm(forms.Form):
    """
    Form to create new user accounts
    """
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    repeat_password = forms.CharField()

    def clean_username(self):
        usernames = User.objects.all().username
        for username in usernames:
            if username == self.cleaned_data["username"]:
                raise ValidationError("That username is already been used, please choose another")

    def clean(self):
        passwords = self.cleaned_data
        if passwords.get("password") != passwords.get("repeat_password"):
            raise ValidationError("The passwords do not match")