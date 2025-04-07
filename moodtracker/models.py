from django.db import models
from django.contrib.auth.models import User

# Define a model to store mood data
class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add user relation
    anonymous_id = models.CharField(max_length=32, null=True, blank=True)

    mood_choices = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('anxious', 'Anxious'),
        ('neutral', 'Neutral'),
    ]
    
    mood = models.CharField(max_length=10, choices=mood_choices)
    notes = models.TextField(null=True, blank=True)  # Optional notes for extra info
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically adds the timestamp

    def __str__(self):
        user_display = self.user.username if self.user else f"Anonymous ({self.anonymous_id})"
        return f"{user_display} - {self.mood} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
