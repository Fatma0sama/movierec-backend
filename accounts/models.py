from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    media_id = models.IntegerField()  # TMDb ID
    media_type = models.CharField(max_length=10, choices=[('movie', 'Movie'), ('tv', 'TV Show')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'media_id', 'media_type')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.media_type} {self.media_id}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=10, choices=[('movie', 'Movie'), ('tv', 'TV Show')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'media_id', 'media_type')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.media_type} {self.media_id}"


class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watched')
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=10, choices=[('movie', 'Movie'), ('tv', 'TV Show')])
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'media_id', 'media_type')
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user.username} - {self.media_type} {self.media_id}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=10, choices=[('movie', 'Movie'), ('tv', 'TV Show')])
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'media_id', 'media_type')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.media_type} {self.media_id} - {self.rating}/10"