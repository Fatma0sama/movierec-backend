from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView, login_view, user_profile,
    FavoriteViewSet, WatchlistViewSet, WatchedViewSet, RatingViewSet
)

router = DefaultRouter()
router.register('favorites', FavoriteViewSet, basename='favorite')
router.register('watchlist', WatchlistViewSet, basename='watchlist')
router.register('watched', WatchedViewSet, basename='watched')
router.register('ratings', RatingViewSet, basename='rating')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/', user_profile, name='profile'),
    path('', include(router.urls)),
]