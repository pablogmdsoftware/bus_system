from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime, date

from .forms import TicketForm
from .models import Customer, Bus, Travel, Ticket, Pass, PassType

class TicketFormTests(TestCase):
    def test_seat_number_greater_than_bus_seats_or_zero(self):
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
            "customer": test_customer,
            "travel": test_travel,
            "seat_number": 100,
            "price": 0,
        })
        zero_seat_ticket = TicketForm(data = {
            "customer": test_customer,
            "travel": test_travel,
            "seat_number": 0,
            "price": 0,
        })  
        self.assertIs(big_seat_ticket.is_valid(),False)
        self.assertIs(zero_seat_ticket.is_valid(),False)

class CustomerModelTests(TestCase):
    def test_not_null_fields(self):
        test_customer = Customer()
        try:
            test_customer.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        self.assertIs(bool(error_raised.get("first_name")),True)
        self.assertIs(bool(error_raised.get("last_name")),True)
        self.assertIs(bool(error_raised.get("birth_date")),True)
        self.assertIs(bool(error_raised.get("gmail")),True)

class BusModelTests(TestCase):
    def test_not_null_fields(self):
        test_bus = Bus()
        try:
            test_bus.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        self.assertIs(bool(error_raised.get("bus_id")),True)
        self.assertIs(bool(error_raised.get("seats")),True)
        self.assertIs(bool(error_raised.get("seats_first_row")),True)
        self.assertIs(bool(error_raised.get("seats_reduced_mobility")),True)
    
class PassTypeModelTests(TestCase):
    def test_not_null_fields(self):
        test_pass_type = PassType()
        try:
            test_pass_type.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        self.assertIs(bool(error_raised.get("name")),True)
        self.assertIs(bool(error_raised.get("price")),True)

class PassModelTests(TestCase):
    def test_not_null_fields(self):
        test_pass = Pass()
        test_pass.num_travels_done = None
        test_pass.num_travels_uncompleted = None
        try:
            test_pass.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        self.assertIs(bool(error_raised.get("customer")),True)
        self.assertIs(bool(error_raised.get("pass_type")),True)
        self.assertIs(bool(error_raised.get("num_travels_done")),True)
        self.assertIs(bool(error_raised.get("num_travels_uncompleted")),True)

class TravelModelTests(TestCase):
    def test_not_null_fields(self):
        test_travel = Travel()
        try:
            test_travel.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        self.assertIs(bool(error_raised.get("schedule")),True)
        self.assertIs(bool(error_raised.get("origin")),True)
        self.assertIs(bool(error_raised.get("destination")),True)
        self.assertIs(bool(error_raised.get("bus")),True)

class TicketModelTests(TestCase):
    def test_not_null_fields(self):
        test_ticket = Ticket()
        try:
            test_ticket.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        self.assertIs(bool(error_raised.get("customer")),True)
        self.assertIs(bool(error_raised.get("travel")),True)
        self.assertIs(bool(error_raised.get("seat_number")),True)