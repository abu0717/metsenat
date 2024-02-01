from django.core.exceptions import ValidationError


def validate_phone_number(value):
    if not (str(value).startswith('+998') and len(str(value)) == 13):
        raise ValidationError('The Phone Number form is not correct')