from rest_framework.validators import UniqueValidator, ValidationError
from .models import Student, Book

def no_numbers(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("This field cannot contain numbers.")
    return value


def email_validator(value):
    if not value.endswith('@gmail.com'):
        raise ValidationError("Email domain must be 'gmail.com'.")
    return value
        