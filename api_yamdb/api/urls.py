from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewsViewSet, TitlesViewSet)

app_name = 'api'

router_v1 = SimpleRouter()
router_v1.register(
    'categories',
    CategoriesViewSet,
    basename='categories')
router_v1.register(
    'genres',
    GenresViewSet,
    basename='genres')
router_v1.register(
    'titles',
    TitlesViewSet,
    basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
