from django.test import TestCase
from datetime import datetime, date

from .forms import TicketForm
from .models import Customer, Bus, Travel, Ticket

class TicketFormTests(TestCase):
    def test_seat_number_greater_than_bus_seats(self):
        test_customer = Customer(
            first_name = "Name",
            last_name = "LastName",
            birth_date = date(year=1990,month=2,day=13),
            gmail = "testemail@gmail.com",
            has_large_family = False,
            has_reduced_mobility = False,
        )
        test_customer.save()
        test_bus = Bus(bus_id="AA00",seats=64,seats_first_row=4,seats_reduced_mobility=0)
        test_bus.save()
        test_travel = Travel(schedule=datetime.now(),origin="M",destination="B",bus=test_bus)
        test_travel.save()
        big_seat_ticket = TicketForm(data = {
            "customer":test_customer,
            "travel":test_travel,
            "seat_number":100,
            "price":0,
        }) 
        self.assertIs(big_seat_ticket.is_valid(),False)