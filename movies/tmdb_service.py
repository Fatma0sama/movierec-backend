import requests
from django.conf import settings
from django.core.cache import cache

class TMDbService:
    BASE_URL = settings.TMDB_BASE_URL
    API_KEY = settings.TMDB_API_KEY

    @staticmethod
    def _make_request(endpoint, params=None):
        """Make request to TMDb API"""
        if params is None:
            params = {}
        params['api_key'] = TMDbService.API_KEY
        
        try:
            response = requests.get(f"{TMDbService.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"TMDb API Error: {e}")
            return None

    @staticmethod
    def get_trending(media_type='all', time_window='week', page=1):
        """Get trending movies/TV shows"""
        cache_key = f'trending_{media_type}_{time_window}_{page}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        data = TMDbService._make_request(f'trending/{media_type}/{time_window}', {'page': page})
        
        if data:
            cache.set(cache_key, data, 3600)  # Cache for 1 hour
        
        return data

    @staticmethod
    def discover(media_type='movie', **filters):
        """Discover movies/TV shows with filters"""
        endpoint = f'discover/{media_type}'
        data = TMDbService._make_request(endpoint, filters)
        return data

    @staticmethod
    def search(query, media_type=None, page=1):
        """Search for movies/TV shows"""
        if media_type:
            endpoint = f'search/{media_type}'
        else:
            endpoint = 'search/multi'
        
        params = {'query': query, 'page': page}
        return TMDbService._make_request(endpoint, params)

    @staticmethod
    def get_genres(media_type='movie'):
        """Get list of genres"""
        cache_key = f'genres_{media_type}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        data = TMDbService._make_request(f'genre/{media_type}/list')
        
        if data:
            cache.set(cache_key, data, 86400)  # Cache for 24 hours
        
        return data

    @staticmethod
    def get_details(media_type, media_id):
        """Get details for a specific movie/TV show"""
        cache_key = f'details_{media_type}_{media_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        data = TMDbService._make_request(f'{media_type}/{media_id}')
        
        if data:
            cache.set(cache_key, data, 3600)  # Cache for 1 hour
        
        return data