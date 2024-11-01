from django.db import models

class Customer(models.Model):
    """Customers and their necessary information to buy tickets"""
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=50)
    birt_date = models.DateField()
    gmail = models.EmailField()
    registration_datetime = models.DateTimeField(auto_now_add=True)
    has_large_family = models.BooleanField(default=False)
    has_reduced_mobility = models.BooleanField(default=False)

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".title()
        return name

class Bus(models.Model):
    """Table to store bus entities owned by the business, the id in this country will 
    be XXYY where X are letters and Y are numbers. Sears number does not have into
    account the other types of seats."""
    bus_id = models.CharField(max_length=7)
    seats = models.PositiveSmallIntegerField()
    seats_first_row = models.PositiveSmallIntegerField()
    seats_reduced_mobility = models.PositiveSmallIntegerField()