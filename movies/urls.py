from django.urls import path
from .views import (
    trending_view, discover_view, search_view,
    genres_view, details_view, wizard_recommend_view
)

urlpatterns = [
    path('trending/', trending_view, name='trending'),
    path('discover/', discover_view, name='discover'),
    path('search/', search_view, name='search'),
    path('genres/', genres_view, name='genres'),
    path('details/<str:media_type>/<int:media_id>/', details_view, name='details'),
    path('wizard/recommend/', wizard_recommend_view, name='wizard-recommend'),
]