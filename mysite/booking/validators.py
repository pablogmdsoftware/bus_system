from django.core.exceptions import ValidationError

def validate_seats_first_row(value):
    if value < 1 or value > 4:
        raise ValidationError("Must be between 1 and 4")