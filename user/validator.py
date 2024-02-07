from django.core.exceptions import ValidationError
import phonenumbers


# def validate_phone_number(value):
#     if not (str(value).startswith('+998') and len(str(value)) == 13):
#         raise ValidationError('The Phone Number form is not correct')

def validate_phone_number(value):
    try:
        phone_number = phonenumbers.parse(value, None)  # Assuming no region code
        if not phonenumbers.is_valid_number(phone_number):
            raise ValidationError('The Phone Number format is not correct')
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError('The Phone Number format is not correct')
