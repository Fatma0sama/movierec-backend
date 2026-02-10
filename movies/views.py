from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tmdb_service import TMDbService

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def trending_view(request):
    """Get trending movies/TV shows"""
    media_type = request.GET.get('media_type', 'all')  # all, movie, tv
    time_window = request.GET.get('time_window', 'week')  # day, week
    page = request.GET.get('page', 1)
    
    data = TMDbService.get_trending(media_type, time_window, page)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def discover_view(request):
    """Discover movies/TV shows with filters"""
    media_type = request.GET.get('media_type', 'movie')
    
    # Build filter parameters
    filters = {}
    
    if request.GET.get('genre'):
        filters['with_genres'] = request.GET.get('genre')
    
    if request.GET.get('sort_by'):
        filters['sort_by'] = request.GET.get('sort_by')
    
    if request.GET.get('year'):
        if media_type == 'movie':
            filters['primary_release_year'] = request.GET.get('year')
        else:
            filters['first_air_date_year'] = request.GET.get('year')
    
    if request.GET.get('rating_gte'):
        filters['vote_average.gte'] = request.GET.get('rating_gte')
    
    if request.GET.get('rating_lte'):
        filters['vote_average.lte'] = request.GET.get('rating_lte')
    
    if request.GET.get('page'):
        filters['page'] = request.GET.get('page')
    
    data = TMDbService.discover(media_type, **filters)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_view(request):
    """Search for movies/TV shows"""
    query = request.GET.get('query', '')
    media_type = request.GET.get('media_type')  # movie, tv, or None for all
    page = request.GET.get('page', 1)
    
    if not query:
        return Response({'error': 'Query parameter is required'}, status=400)
    
    data = TMDbService.search(query, media_type, page)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genres_view(request):
    """Get list of genres"""
    media_type = request.GET.get('media_type', 'movie')
    data = TMDbService.get_genres(media_type)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def details_view(request, media_type, media_id):
    """Get details for a specific movie/TV show"""
    data = TMDbService.get_details(media_type, media_id)
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wizard_recommend_view(request):
    """Smart recommendation wizard based on user preferences"""
    media_type = request.GET.get('media_type', 'movie')
    
    # Build filters based on wizard choices
    filters = {
        'sort_by': 'popularity.desc',
        'page': 1
    }
    
    # Mood -> Genres
    mood = request.GET.get('mood')
    if mood and mood != 'dontcare':
        mood_genres = {
            'dramatic': '28,12,18,10752',  # Action, Adventure, Drama, War
            'intense': '27,53,80',  # Horror, Thriller, Crime
            'gentle': '35,10751,10749,16',  # Comedy, Family, Romance, Animation
            'curious': '9648,36,99',  # Mystery, History, Documentary
            'otherworldly': '14,878',  # Fantasy, Sci-Fi
            'realistic': '99,36'  # Documentary, Biography
        }
        if mood in mood_genres:
            filters['with_genres'] = mood_genres[mood]
    
    # Period -> Year range
    period = request.GET.get('period')
    if period and period != 'dontcare':
        period_map = {
            'fresh': (2023, 2025),
            'recent': (2020, 2025),
            'modern': (2015, 2025),
            'golden': (2000, 2015),
            'throwback': (1990, 2000),
            'retro': (1900, 1990)
        }
        if period in period_map:
            year_range = period_map[period]
            if media_type == 'movie':
                filters['primary_release_date.gte'] = f'{year_range[0]}-01-01'
                filters['primary_release_date.lte'] = f'{year_range[1]}-12-31'
            else:
                filters['first_air_date.gte'] = f'{year_range[0]}-01-01'
                filters['first_air_date.lte'] = f'{year_range[1]}-12-31'
    
    # Quality -> Rating
    quality = request.GET.get('quality')
    if quality and quality != 'dontcare':
        quality_map = {
            'masterpiece': 8.0,
            'high': 7.0,
            'average': 5.0
        }
        if quality in quality_map:
            filters['vote_average.gte'] = quality_map[quality]
    
    # Runtime
    runtime = request.GET.get('runtime')
    if runtime and runtime != 'dontcare':
        runtime_map = {
            'quick': (0, 90),
            'standard': (90, 150),
            'epic': (150, 500)
        }
        if runtime in runtime_map:
            filters['with_runtime.gte'] = runtime_map[runtime][0]
            filters['with_runtime.lte'] = runtime_map[runtime][1]
    
    # Popularity -> Vote count
    popularity_level = request.GET.get('popularity')
    if popularity_level and popularity_level != 'dontcare':
        popularity_map = {
            'famous': 50000,
            'known': 10000,
            'hidden': 0
        }
        if popularity_level in popularity_map:
            filters['vote_count.gte'] = popularity_map[popularity_level]
    
    data = TMDbService.discover(media_type, **filters)
    return Response(data)