from django.db import models

class Customer(models.Model):
    """Customers and their necessary information to buy tickets."""
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
    be XXYY where X are letters and Y are numbers. Seats number have into account 
    the reduced mobility seats."""
    bus_id = models.CharField(max_length=4)
    seats = models.PositiveSmallIntegerField()
    seats_first_row = models.PositiveSmallIntegerField()
    seats_reduced_mobility = models.PositiveSmallIntegerField()

    def __str__(self):
        total_seats = self.seats + self.seats_reduced_mobility
        return f"ID: {self.bus_id}. Total Seats: {total_seats} ({self.seats_reduced_mobility}rm)."

pass_type_names = {
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
    name = models.CharField(max_length=50,choices=pass_type_names,unique=True)
    max_uses = models.PositiveSmallIntegerField(null=True)
    price = models.PositiveIntegerField(db_comment="Stored in cts")     
    is_multi_route = models.BooleanField(db_default=False)

    def __str__(self):
        return f"{self.name}"