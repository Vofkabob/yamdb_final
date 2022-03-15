from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели категорий.
    """
    class Meta:
        exclude = ('id',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели жанров.
    """
    class Meta:
        exclude = ('id',)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели произведений.
    Предназначен для операций записи.
    """
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerGet(serializers.ModelSerializer):
    """
    Сериализатор модели жанров.
    Предназначен для операций чтения.
    """
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели отзывов.
    """
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    title = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        data_kwargs = self.context['request'].parser_context['kwargs']

        if 'pk' in data_kwargs:
            return data

        title_id = data_kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        if self.context['request'].user.reviews.filter(title=title).exists():
            raise serializers.ValidationError(
                detail='Ваш отзыв уже существует!',
                code=status.HTTP_400_BAD_REQUEST)
        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели комментариев.
    """
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    review = serializers.SlugRelatedField(
        slug_field='id', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
