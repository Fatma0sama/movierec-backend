from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Favorite, Watchlist, Watched, Rating

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'media_id', 'media_type', 'created_at']
        read_only_fields = ['id', 'created_at']

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ['id', 'media_id', 'media_type', 'created_at']
        read_only_fields = ['id', 'created_at']

class WatchedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watched
        fields = ['id', 'media_id', 'media_type', 'watched_at']
        read_only_fields = ['id', 'watched_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'media_id', 'media_type', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError("Rating must be between 1 and 10")
        return value