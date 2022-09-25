from datetime import datetime

from rest_framework.serializers import ValidationError


def correct_year(value):
    if value > datetime.now().year:
        raise ValidationError(f'{value} год больше текущего!')
