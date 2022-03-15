from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя.
    Для операций создания и редактирования пользователя.
    """
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role')
        model = User


class EmailSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя.
    Для операций запроса проверочного кода при авторизации.
    """
    class Meta:
        fields = ['email', 'username']
        model = User
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }


class AccessTokenSerializer(serializers.Serializer):
    """
    Сериализатор для получения токена.
    """
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
