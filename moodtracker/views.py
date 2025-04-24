import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .spotify_auth import get_song_link_based_on_mood
from django.utils.crypto import get_random_string
from .models import Mood
from django.views.decorators.csrf import csrf_exempt
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"

from transformers import pipeline

# Initialize the Hugging Face emotion detection pipeline
emotion_classifier = pipeline("text-classification", 
                              model="j-hartmann/emotion-english-distilroberta-base",
                              top_k=1)

MOOD_RECOMMENDATIONS = {
    "joy": {
        "advice": "Keep doing what makes you happy!",
        "activities": ["Go for a walk", "Share your joy with someone"],
        "music": ["Happy – Pharrell Williams", "Walking on Sunshine – Katrina & The Waves"]
    },
    "sadness": {
        "advice": "Try taking a walk or talking to a friend.",
        "activities": ["Journal your feelings", "Watch a comforting movie"],
        "music": ["Fix You – Coldplay", "Someone Like You – Adele"]
    },
    "anger": {
        "advice": "Take a deep breath. Maybe write it out or do something to cool off.",
        "activities": ["Boxing workout", "Go for a run"],
        "music": ["Lose Yourself – Eminem", "Numb – Linkin Park"]
    },
    "fear": {
        "advice": "You're not alone. Try slowly taking deep breaths.",
        "activities": ["Meditate for 5 minutes", "Do a grounding exercise"],
        "music": ["Weightless – Marconi Union", "Breathe Me – Sia"]
    },
    "surprise": {
        "advice": "Stay curious and open to what's ahead!",
        "activities": ["Capture the moment in a journal", "Talk about it with someone"],
        "music": ["Surprise Yourself – Jack Garratt", "Life is Beautiful – Sixx:A.M."]
    },
    "neutral": {
        "advice": "A great moment to relax or try something new.",
        "activities": ["Read a book", "Try a new recipe"],
        "music": ["Lo-Fi Chill Playlist – YouTube", "Better Together – Jack Johnson"]
    }
}

def detect_emotion_from_text(text):
    try:
        result = emotion_classifier(text, top_k=1)
        if isinstance(result, list) and isinstance(result[0], list):
            result = result[0]
        return result [0]['label'].lower()
    except Exception as e:
        print("Emotion detection error:", e)
        return "neutral"

def index(request):
    # Assign a cookie ID if it doesn't exist
    if not request.COOKIES.get('anonymous_id'):
        anonymous_id = get_random_string(32)
        response = redirect('index')
        response.set_cookie('anonymous_id', anonymous_id, max_age=60*60*24*30)  # Cookie valid for 30 days
        return response
    
    anonymous_id = request.COOKIES.get('anonymous_id')

    advice = ""
    activities = []
    music = []

    if request.method == "POST":
        notes = request.POST.get('notes', '')
        if notes:
            emotion = detect_emotion_from_text(notes) if notes else "Neutral"
            emotion_data = MOOD_RECOMMENDATIONS.get(emotion, {})
            advice = emotion_data.get("advice", "Take care of yourself.")
            activities = emotion_data.get("activities", [])
            music = emotion_data.get("music", [])

            Mood.objects.create(
                user=request.user if request.user.is_authenticated else None,
                anonymous_id=anonymous_id,
                notes=notes,
                emotion=emotion,
                advice=advice,
            )

            return redirect('index')

    if request.user.is_authenticated:
        moods = Mood.objects.filter(user=request.user).order_by('timestamp')
    else:
        moods = Mood.objects.filter(anonymous_id=anonymous_id).order_by('timestamp')
        
    labels = [m.timestamp.strftime('%Y-%m-%d') for m in moods]
    mood_values = [
        {
            'joy': 5,
            'sadness': 2,
            'anger': 3,
            'fear': 4,
            'neutral': 1
        }.get(m.emotion.lower(), 0)
        for m in moods
    ]

    context = {
        'labels': json.dumps(labels),  # Pass labels as JSON
        'mood_values': json.dumps(mood_values),  # Pass mood values as JSO
        'moods': moods,
        'mood_data': [(m, m.emotion) for m in moods],
        'latest_advice': advice if 'advice' in locals() else "",
        'latest_activities': activities if 'activities' in locals() else [],
        'latest_music': music if 'music' in locals() else [],
    }

    return render(request, 'moodtracker/index.html', context)

# User registration view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    """Handles logout with GET request and redirects to login."""
    logout(request)
    return redirect('login')  # Redirect to login page

