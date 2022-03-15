from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.permissions import (IsAdminOrReadOnly,
                               IsAuthorModeratorAdminOrReadOnly)
from .filters import TitleFilter
from .mixins import LCDMixin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerGet)


class CategoriesViewSet(LCDMixin):
    """
    Вьюсет модели категорий.
    Получение списка, создание, удаление.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, ]

    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    lookup_field = 'slug'


class GenresViewSet(LCDMixin):
    """
    Вьюсет модели жанров.
    Получение списка, создание, удаление.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly, ]

    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели произведений. CRUD.
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')

    permission_classes = [IsAdminOrReadOnly, ]

    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializer
        return TitleSerializerGet


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели отзывов. CRUD.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly, ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))

        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели комментариев. CRUD.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly, ]

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        comments = Comment.objects.filter(review=review)
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
