from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


v1_router = SimpleRouter()

v1_router.register(
    'users',
    views.UsersViewSet,
    basename='users'
)

v1_router.register('categories', views.CategoriesViewSet)
v1_router.register('genres', views.GenresViewSet)
v1_router.register('titles', views.TitlesViewSet)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentsViewSet,
    basename='comments'
)

authpatterns = [
    path('auth/signup/', views.RegisterView.as_view(), name='register'),
    path('auth/token/', views.TokenView.as_view(), name='token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(authpatterns)),
]
