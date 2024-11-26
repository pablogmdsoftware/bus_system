from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from .validators import validate_seats_first_row, validate_seats, validate_rm_seats

class Customer(models.Model):
    """Users information to buy tickets."""
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birth_date = models.DateField(null=True,blank=True)
    has_large_family = models.BooleanField(default=False)
    has_reduced_mobility = models.BooleanField(default=False)

    def __str__(self):
        name = f"{self.user.first_name} {self.user.last_name}".title()
        return name

class Bus(models.Model):
    """
    Table to store bus entities owned by the business, the id in this country will
    be XXYY where X are letters and Y are numbers. Seats number does not have into
    account the reduced mobility seats.
    """
    bus_id = models.CharField(
        max_length=4,
        primary_key=True,
        validators=[RegexValidator("[A-Z]{2}[0-9]{2}","XXYY where X are letters and Y are numbers")],
        )
    seats = models.PositiveSmallIntegerField(validators=[validate_seats])
    seats_first_row = models.PositiveSmallIntegerField(validators=[validate_seats_first_row])
    seats_reduced_mobility = models.PositiveSmallIntegerField(validators=[validate_rm_seats])

    def __str__(self):
        return f"ID: {self.bus_id}. Total Seats: {self.seats} (+{self.seats_reduced_mobility}rm)."

PASS_TYPE_NAMES = {
    "ten_ticket_pass":"ten_ticket_pass",
    "ten_ticket_pass_multi_route":"ten_ticket_pass_multi_route",
    "monthly_pass":"monthly_pass",
    "monthly_pass_multi_route":"monthly_pass_multi_route",
    "three_month_pass":"three_month_pass",
    "three_month_pass":"three_month_pass",
    "four_month_pass":"four_month_pass",
    "four_month_pass":"four_month_pass",
    "year_pass":"year_pass",
    "year_pass":"year_pass",
}

class PassType(models.Model):
    """Available passes that the customers can buy."""
    name = models.CharField(max_length=50,choices=PASS_TYPE_NAMES,unique=True)
    max_uses = models.PositiveSmallIntegerField(null=True,blank=True)
    price = models.PositiveIntegerField(db_comment="Stored in cts")
    months_duration = models.PositiveSmallIntegerField(null=True,blank=True)
    is_multi_route = models.BooleanField(db_default=False)

    def __str__(self):
        return f"{self.name}"

CITIES = {
    "M":"Madrid",
    "B":"Barcelona",
    "TO":"Toledo",
    "BU":"Burgos",
    "SO":"Soria",
    "OV":"Oviedo",
    "PO":"Pontevedra",
}

class Pass(models.Model):
    """Personal passes."""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pass_type = models.ForeignKey(PassType,on_delete=models.PROTECT)
    num_travels_done = models.PositiveSmallIntegerField(default=0)
    num_travels_uncompleted = models.PositiveSmallIntegerField(default=0)
    purchased_datetime = models.DateTimeField(auto_now_add=True)
    validity_date = models.DateField(null=True,blank=True)
    first_city = models.CharField(max_length=2,choices=CITIES,null=True,blank=True)
    second_city = models.CharField(max_length=2,choices=CITIES,null=True,blank=True)

    def __str__(self):
        user_name = f"{self.user.first_name} {self.user.last_name}".title()
        return f"""{self.pass_type.name} puchased by {user_name}. Validity: {self.validity_date}. 
                Direction: {self.first_city}-{self.second_city}."""

class Travel(models.Model):
    """
    Travel itinerary to schedule the rides that the company offers. We assume that
    the buses can always be where they are needed. However, they can not be used
    two times in the same date.
    """
    schedule = models.DateTimeField()
    origin = models.CharField(max_length=2,choices=CITIES)
    destination = models.CharField(max_length=2,choices=CITIES)
    bus = models.ForeignKey(Bus,on_delete=models.PROTECT,unique_for_date="schedule")

    def __str__(self):
        return f"""{self.schedule.strftime("%d-%m-%Y (%H:%M %Z)")}. 
        Direction: {self.origin}-{self.destination}. Bus: {self.bus.bus_id}."""

class Ticket(models.Model):
    """Personal customer tickets."""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    travel = models.ForeignKey(Travel,on_delete=models.PROTECT)
    seat_number = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField(null=True,blank=True,db_comment="Stored in cts")
    purchase_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(name="unique_seat_per_travel",fields=["seat_number","travel_id"]),
        ]

    def __str__(self):
        origin = self.travel.origin
        destination = self.travel.destination
        schedule = self.travel.schedule
        user = f"{self.user.first_name} {self.user.last_name}".title()
        return f"""{schedule.strftime("%d-%m-%Y (%H:%M %Z)")}. Direction: {origin}-{destination}.
        Seat number: {self.seat_number}. Purchased by {user}."""