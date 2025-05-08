from django.db import models
from django.contrib.auth.models import User

# Define a model to store mood data
class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_id = models.CharField(max_length=64, null=True, blank=True)

    # Removed unused mood_choices, since emotion detection is dynamic
    emotion = models.CharField(max_length=50, default="unknown")
    notes = models.TextField()
    advice = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Spotify resources
    song_link = models.URLField(null=True, blank=True)
    podcast_link = models.URLField(null=True, blank=True)

    def __str__(self):
        user_display = self.user.username if self.user else f"Anonymous ({self.anonymous_id})"
        return f"{user_display} - {self.emotion} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
