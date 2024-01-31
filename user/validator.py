from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not value.startswith('+998') and len(value) == 13:
        raise ValidationError('The Phone Number form is not correct')
