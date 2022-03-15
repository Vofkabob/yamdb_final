from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdmin
from .serializers import AccessTokenSerializer, EmailSerializer, UserSerializer


class EmailConfirmationView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет пользователя для получения кода подтверждения.
    """
    permission_classes = [AllowAny, ]
    serializer_class = EmailSerializer

    def create(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        serializer.save(
            email=email,
            confirmation_code=User.generate_code())
        user = get_object_or_404(
            User,
            email=email)
        send_mail(
            subject='YaMDB Confirmation Code',
            message=f'Your code: {user.confirmation_code}',
            from_email=settings.NOREPLY_EMAIL,
            recipient_list=[email],
            fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccessTokenView(APIView):
    """
    Вьюсет получения токена авторизации.
    """
    permission_classes = [AllowAny, ]
    serializer_class = AccessTokenSerializer

    def post(self, request):
        serializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)

        confirmation_code = serializer.validated_data['confirmation_code']
        if user.confirmation_code != confirmation_code:
            return Response(
                {'confirmation_code': 'Неверный проверочный код'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.get_token(user), status=status.HTTP_200_OK)

    def get_token(user):
        return {
            'token': str(AccessToken.for_user(user))
        }


class UsersViewSet(viewsets.ModelViewSet):
    """
    Вьюсет пользователя для создания и редактирования. CRUD.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    lookup_field = 'username'

    permission_classes = [IsAdmin, ]

    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'PATCH':
            if request.data.get('role') and not request.user.is_admin:
                serializer = self.get_serializer(request.user)
                return Response(
                    serializer.data,
                    status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
