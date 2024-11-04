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
    be XXYY where X are letters and Y are numbers. Seats number has into account 
    the reduced mobility seats."""
    bus_id = models.CharField(max_length=4,primary_key=True)
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
    max_uses = models.PositiveSmallIntegerField(null=True,blank=True)
    price = models.PositiveIntegerField(db_comment="Stored in cts")
    is_multi_route = models.BooleanField(db_default=False)

    def __str__(self):
        return f"{self.name}"

cities = {
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
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    pass_type = models.ForeignKey(PassType,on_delete=models.CASCADE)
    num_travels_done = models.PositiveSmallIntegerField()
    num_travels_uncompleted = models.PositiveSmallIntegerField()
    purchased_datetime = models.DateTimeField(auto_now_add=True)
    validity_date = models.DateField()
    first_city = models.CharField(max_length=2,choices=cities)
    second_city = models.CharField(max_length=2,choices=cities)

    def __str__(self):
        customer_name = f"{self.customer.first_name} {self.customer.last_name}".title()
        return f"""{self.pass_type.name} puchased by {customer_name}. Validity: {self.validity_date}. 
                Direction: {self.first_city}-{self.second_city}."""

class Travel(models.Model):
    """Travel itinerary to schedule the rides that the company offers."""
    bus_id = models.ForeignKey(Bus,on_delete=models.PROTECT)
    origin = models.CharField(max_length=2,choices=cities)
    destination = models.CharField(max_length=2,choices=cities)
    schedule = models.DateTimeField()

    def __str__(self):
        return f"""Schedule: {self.schedule}. Direction: {self.origin}-{self.destination}. 
        Bus: {self.bus_id.bus_id}."""

class Ticket(models.Model):
    """Personal tickets of the customers."""
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE)
    travel_id = models.ForeignKey(Travel,on_delete=models.PROTECT)
    seat_number = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField(null=True,db_comment="Stored in cts")
    purchase_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        origin = self.travel_id.origin
        destination = self.travel_id.destination
        schedule = self.travel_id.schedule
        customer = f"{self.customer_id.first_name} {self.customer_id.last_name}".title()
        return f"""{origin}-{destination} ({schedule}). Seat number: {self.seat_number}. 
        Purchased by {customer}."""