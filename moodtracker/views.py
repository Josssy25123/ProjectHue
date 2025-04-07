import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import Mood
from transformers import pipeline

# Initialize the Hugging Face emotion detection pipeline
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def index(request):
    # Assign a cookie ID if it doesn't exist
    if not request.COOKIES.get('anonymous_id'):
        anonymous_id = get_random_string(32)
        response = redirect('index')
        response.set_cookie('anonymous_id', anonymous_id, max_age=60*60*24*30)  # Cookie valid for 30 days
        return response
    
    anonymous_id = request.COOKIES.get('anonymous_id')

    if request.method == "POST":
        # Get the mood and notes from the form
        mood = request.POST['mood']
        notes = request.POST.get('notes', '')

        detected_emotion = detect_emotion_from_text(notes) if notes else "Neutral"

        # Save the mood entry to the database & associate with the logged-in user
        if request.user.is_authenticated:
            new_mood = Mood(user=request.user, mood=mood, notes=notes)
        else:
            new_mood = Mood(mood=mood, notes=notes, anonymous_id=anonymous_id)  # Anonymous user
        
        new_mood.notes += f"\n[Detected Emotion: {detected_emotion}]"
        new_mood.save()

        request.session['detected_emotion'] = detected_emotion

        return redirect('index')
    
    # Fetch mood data for the chart
    if request.user.is_authenticated:
        moods = Mood.objects.filter(user=request.user).order_by('timestamp')  # For authenticated users
    else:
        moods = Mood.objects.filter(anonymous_id=anonymous_id).order_by('timestamp')  # For anonymous users

    labels = []
    mood_values = []
    detected_emotions = []

    # Create data for the chart
    for mood in moods:
        labels.append(mood.timestamp.strftime('%Y-%m-%d'))  # Format date for x-axis
        mood_values.append({
            'happy': 5,
            'sad': 2,
            'angry': 3,
            'anxious': 4,
            'neutral': 1
        }.get(mood.mood, 0))  # Assign numeric values for mood types
    
        # Extract detected emotions from notes
        if '[Detected Emotion:' in mood.notes:
            detected_emotion = mood.notes.split('[Detected Emotion: ')[-1].replace(']', '')
        else:
            detected_emotion = "N/A"

        detected_emotions.append(detected_emotion)
        
    context = {
        'labels': json.dumps(labels),  # Pass labels as JSON
        'mood_values': json.dumps(mood_values),  # Pass mood values as JSON
        'detected_emotions': detected_emotions,
        'mood_data': zip(moods, detected_emotions)
    }
    
    return render(request, 'moodtracker/index.html', context)

def detect_emotion_from_text(text):
    # Use the Hugging Face model to detect emotion from text
    result = emotion_classifier(text)
    # Extract the predicted emotion with the highest score
    emotion = result[0]['label']
    return emotion

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