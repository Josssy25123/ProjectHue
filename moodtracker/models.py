from django.db import models
from django.contrib.auth.models import User

# Define a model to store mood data
class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add user relation
    anonymous_id = models.CharField(max_length=64, null=True, blank=True)

    mood_choices = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('anxious', 'Anxious'),
        ('neutral', 'Neutral'),
    ]

    emotion = models.CharField(max_length=50, default="unknown")
    notes = models.TextField()  # Optional notes for extra info
    advice = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds the timestamp

    def __str__(self):
        user_display = self.user.username if self.user else f"Anonymous ({self.anonymous_id})"
        return f"{user_display} - {self.mood} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
