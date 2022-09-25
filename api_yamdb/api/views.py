from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (IsAdminOrReadOnlyPermission, IsAdminPermission,
                             ReviewOrCommentPermission)
from api.serializers import (CategorySerializer, CommentsSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer)
from api.utils import gen_confirmation_code, send_confirmation_code
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        users = User.objects.filter(email=email, username=username)
        if users.exists():
            confirmation_code = users.first().confirmation_code
            send_confirmation_code(email, confirmation_code)
            return Response(
                {
                    'email': email,
                    'username': username
                }
            )
        confirmation_code = gen_confirmation_code()
        data = {
            'email': email,
            'confirmation_code': confirmation_code,
            'username': username
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        send_confirmation_code(email, confirmation_code)
        return Response(
            {
                'email': email,
                'username': username
            }
        )


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        confirmation_code = request.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        refresh = RefreshToken.for_user(user)
        if user.confirmation_code != confirmation_code:
            return Response(
                {
                    'confirmation_code': 'Неверный код подтверждения!',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'token': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission, permissions.IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(detail=False,
            url_path=r'(?P<username>[\w.@+-]+)',
            methods=['get', 'patch', 'delete'])
    def get_users(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(user, many=False)
        if request.method == 'PATCH':
            data = request.data
            serializer = self.get_serializer(
                instance=user, data=data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.data)

    @action(methods=['get', 'patch'],
            detail=False, url_path='me',
            permission_classes=(permissions.IsAuthenticated,))
    def get_self_info(self, request):
        user = request.user
        serializer = self.get_serializer(user, many=False)
        if request.method == 'PATCH':
            data = request.data
            serializer = self.get_serializer(
                instance=user, data=data, partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewOrCommentPermission, )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        if serializer.is_valid:
            serializer.save(
                title=self.get_title(),
                author=self.request.user
            )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (ReviewOrCommentPermission, )

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.get_title())

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(),
            author=self.request.user,
        )


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    serializer_class = TitleWriteSerializer
    permission_classes = (IsAdminOrReadOnlyPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
