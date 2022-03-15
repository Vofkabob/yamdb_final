from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AccessTokenView, EmailConfirmationView, UsersViewSet

app_name = 'users'

router_v1 = SimpleRouter()
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/',
         EmailConfirmationView.as_view({'post': 'create'}),
         name='signup'),
    path('v1/auth/token/', AccessTokenView.as_view(), name='token'),
]
