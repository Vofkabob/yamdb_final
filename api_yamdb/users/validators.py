from django.core.exceptions import ValidationError


def validate_me(value):
    if value == 'me':
        raise ValidationError('Неверное имя пользователя')
