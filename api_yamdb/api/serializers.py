from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone

from reviews.models import (
    User, ROLES, Review, Comments,
    Title, Genre, Category
)


class UserSerializer(serializers.ModelSerializer):

    role = serializers.ChoiceField(choices=ROLES, default='user')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
            'confirmation_code',
        )
        extra_kwargs = {
            'confirmation_code': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                'Такое имя пользователя недопустимо!'
            )
        if 'role' in attrs != 'user' and 'request' in self.context:
            if self.context.get('request').user.role == 'user':
                del attrs['role']
                return attrs
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'confirmation_code',
            'username'
        )
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='pk'
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date'
        )

    def validate(self, attrs):
        if attrs.get('score'):
            if attrs.get('score') < 1 or attrs.get('score') > 10:
                raise serializers.ValidationError(
                    'Параметр "score" должен быть в пределах от 1 до 10!'
                )
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if (Review.objects.filter(
                title=get_object_or_404(Title, pk=title_id),
                author=author
        )
                and self.context['request'].method == 'POST'):
            raise serializers.ValidationError(
                'Объект с такими параметрами уже существует!'
            )
        return attrs


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='pk'
    )
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comments
        fields = (
            'id',
            'review',
            'text',
            'author',
            'pub_date'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        model = Title

    def validate_year(value):
        if value > timezone.now().year:
            raise ValidationError(
                ('Год %(value)s больше текущего!'),
                params={'value': value},
            )


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

    def to_representation(self, instance):
        serializer = TitleReadSerializer(instance)
        return serializer.data
