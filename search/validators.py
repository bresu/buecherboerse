from django.core.exceptions import ValidationError


def validate_isbn_numeric(value):
    if not value.isdigit():
        raise ValidationError("ISBN must consist of digits only!")
