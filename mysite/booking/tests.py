from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime, date, timezone

from .forms import TicketForm, SearchTravelForm, PasswordForm, SingupForm
from .models import Customer, Bus, Travel, Ticket, Pass, PassType

# class TicketFormTests(TestCase):
#     def test_seat_number_greater_than_bus_seats_or_zero(self):
#         test_customer = Customer(
#             first_name = "Name",
#             last_name = "LastName",
#             birth_date = date(year=1990,month=2,day=13),
#             gmail = "testemail@gmail.com",
#             has_large_family = False,
#             has_reduced_mobility = False,
#         )
#         test_customer.save()
#         test_bus = Bus(bus_id="AA00",seats=64,seats_first_row=4,seats_reduced_mobility=0)
#         test_bus.save()
#         test_travel = Travel(
#             schedule=datetime.now(timezone.utc),
#             origin="M",
#             destination="B",
#             bus=test_bus,
#         )
#         test_travel.save()
#         big_seat_ticket = TicketForm(data = {
#             "customer": test_customer,
#             "travel": test_travel,  
#             "seat_number": 100,
#             "price": 0,
#         })
#         zero_seat_ticket = TicketForm(data = {
#             "customer": test_customer,
#             "travel": test_travel,
#             "seat_number": 0,
#             "price": 0,
#         })  
#         self.assertIs(big_seat_ticket.is_valid(),False)
#         self.assertIs(zero_seat_ticket.is_valid(),False)

# class CustomerModelTests(TestCase):
#     def test_not_null_fields(self):
#         test_user = User()
#         try:
#             test_user.full_clean()
#         except ValidationError as err:
#             error_raised = dict(err)
#         else:
#             error_raised = {}      
#         self.assertIs(bool(error_raised.get("first_name")),True)
#         self.assertIs(bool(error_raised.get("last_name")),True)
#         self.assertIs(bool(error_raised.get("birth_date")),True)
#         self.assertIs(bool(error_raised.get("gmail")),True)

class BusModelTests(TestCase):
    def test_not_null_fields(self):
        test_bus = Bus()
        try:
            test_bus.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("bus_id")),True)
        self.assertIs(bool(error_raised.get("seats")),True)
        self.assertIs(bool(error_raised.get("seats_first_row")),True)
        self.assertIs(bool(error_raised.get("seats_reduced_mobility")),True)

    def test_bus_id_regex_validator(self):
        test_bus = Bus(bus_id="AAAA")
        try:
            test_bus.clean_fields(exclude=["seats","seats_first_row","seats_reduced_mobility"])
        except ValidationError as err:
            error_raised = dict(err)
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("bus_id")),True)

    def test_seats_validator(self):
        test_bus = Bus(seats=100)
        try:
            test_bus.clean_fields(exclude=["bus_id","seats_first_row","seats_reduced_mobility"])
        except ValidationError as err:
            error_raised = dict(err)
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("seats")),True)

    def test_seats_first_row_validator(self):
        test_bus = Bus(seats_first_row=5)
        try:
            test_bus.clean_fields(exclude=["bus_id","seats","seats_reduced_mobility"])
        except ValidationError as err:
            error_raised = dict(err)
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("seats_first_row")),True)

    def test_seats_reduced_mobility_validator(self):
        test_bus = Bus(seats_reduced_mobility=5)
        try:
            test_bus.clean_fields(exclude=["bus_id","seats","seats_first_row"])
        except ValidationError as err:
            error_raised = dict(err)
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("seats_reduced_mobility")),True)

    
class PassTypeModelTests(TestCase):
    def test_not_null_fields(self):
        test_pass_type = PassType()
        try:
            test_pass_type.full_clean()
        except ValidationError as err:
            error_raised = dict(err)
        else:
            error_raised = {}
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
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("user")),True)
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
        else:
            error_raised = {}
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
        else:
            error_raised = {}
        self.assertIs(bool(error_raised.get("user")),True)
        self.assertIs(bool(error_raised.get("travel")),True)
        self.assertIs(bool(error_raised.get("seat_number")),True)

class SearchTravelFormTests(TestCase):
    def test_clean_date_with_past_date(self):
        form = SearchTravelForm({"date":datetime(2000,1,1)})
        form.is_valid()
        self.assertIs(form.cleaned_data.get("date"),None)
    def test_clean_with_same_origin_than_destination(self):
        form = SearchTravelForm({"origin":"M","destination":"M"})
        form.is_valid()
        self.assertEqual(form.errors.get("__all__"),["Cities must be different"])

class PasswordFormTests(TestCase):
    def test_clean_with_mismatched_passwords(self):
        form = PasswordForm({
            "new_password": "test1234",
            "repeat_password": "test5687",
        })
        form.is_valid()
        self.assertEqual(form.errors.get("__all__"),["The passwords do not match"])
    def test_clean_new_password_with_short_password(self):
        form = PasswordForm({
            "new_password": "test",
            "repeat_password": "test",
        })
        form.is_valid()
        self.assertIs(bool(form.errors.get("new_password")),True)
    def test_clean_new_password_with_letters_only_password(self):
        form = PasswordForm({
            "new_password": "password",
            "repeat_password": "password",
        })
        form.is_valid()
        self.assertIs(bool(form.errors.get("new_password")),True)
    def test_clean_new_password_with_digits_only_password(self):
        form = PasswordForm({
            "new_password": "0123456879",
            "repeat_password": "0123456879",
        })
        form.is_valid()
        self.assertIs(bool(form.errors.get("new_password")),True)

class SingupFormTests(TestCase):
    def test_clean_username_with_stored_username(self):
        User.objects.create_user(username="test_username",password="testpassword1234")
        form = SingupForm({"username":"test_username"})
        form.is_valid()
        self.assertIs(bool(form.errors.get("username")),True)
    def test_email_field_validation(self):
        form = SingupForm({"email":"not_an_email_string"})
        form.is_valid()
        self.assertIs(bool(form.errors.get("email")),True)
    def test_singup_form_inherits_from_password_form(self):
        self.assertIs(issubclass(SingupForm,PasswordForm),True)