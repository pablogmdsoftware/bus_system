from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from datetime import date, timedelta

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

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        if birth_date:
            today = date.today()
            if date(year=today.year-10,month=today.month,day=today.day) < birth_date:
                raise ValidationError("That birth date was weird, wasn't it?")
        return birth_date

class PasswordForm(forms.Form):
    """
    Form to change passwords.
    """
    old_password = forms.CharField()
    new_password = forms.CharField()
    repeat_password = forms.CharField()

    def clean_new_password(self):
        password = self.cleaned_data["new_password"]
        weak_password_message = """
        Weak passwords are not allowed. It must contain at least 8 characters
        using letters and numbers. 
        """
        if len(password) < 8:
            raise ValidationError(weak_password_message)
        weak = {
            "has_letter": False,
            "has_digit": False,
        }
        for character in password:
            if character.islower() or character.isupper():
                weak["has_letter"] = True
                break
        for character in password:
            if character.isdigit():
                weak["has_digit"] = True
                break
        if weak["has_letter"] and weak["has_digit"]:
            return password
        else:
            raise ValidationError(weak_password_message)

    def clean(self):
        passwords = self.cleaned_data
        if passwords.get("new_password") != passwords.get("repeat_password"):
            raise ValidationError("The passwords do not match")

class SignupForm(PasswordForm):
    """
    Form to create new user accounts. It inherits the fields *new_password* and
    *repeat_password* from PasswordForm, along with the password validation.
    """
    username = forms.CharField()
    email = forms.EmailField()
    old_password = None

    def clean_username(self):
        users = User.objects.all()
        for user in users:
            if user.username == self.cleaned_data["username"]:
                raise ValidationError("That username is already in use, please choose another.")
        return self.cleaned_data["username"]

    def clean(self):
        super().clean()