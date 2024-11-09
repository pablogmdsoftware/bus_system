from django.core.exceptions import ValidationError

def validate_seats_first_row(value):
    if value < 1 or value > 4:
        raise ValidationError("Must be between 1 and 4")

def validate_seats(value):
    if value < 8:
        raise ValidationError("Too little for a bus, right?")
    if value > 68:
        raise ValidationError("I don't know buses that big!")

def validate_rm_seats(value):
    if value < 0 or value > 2:
        raise ValidationError("The maximum amount of rm seats is 2")