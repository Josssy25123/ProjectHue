import json
import os
import requests
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import urllib.parse
from .models import Mood
from .emotion_detector import detect_emotion
from .spotify_auth import get_song_link_based_on_mood, get_podcast_link_based_on_mood

# Disable TensorFlow dependency in transformers
os.environ["TRANSFORMERS_NO_TF"] = "1"
from transformers import pipeline

# Hugging Face Emotion Detection
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# General mood advice
ADVICE = {
    "joy": "Keep doing what makes you happy!",
    "sadness": "Try taking a walk or talking to a friend.",
    "anger": "Take a deep breath. Maybe write it out or do something to cool off.",
    "fear": "You're not alone. Try slowly taking deep breaths.",
    "surprise": "Stay curious and open to what's ahead!",
    "neutral": "A great moment to relax or try something new."
}

def index(request):

    access_token = request.session.get('spotify_access_token', None)
    refresh_token = request.session.get('spotify_refresh_token', None)
 
    # Assign guest cookie if not authenticated
    if not request.COOKIES.get('anonymous_id'):
        anonymous_id = get_random_string(32)
        response = redirect('index')
        response.set_cookie('anonymous_id', anonymous_id, max_age=60*60*24*30)
        return response
    
    anonymous_id = request.COOKIES.get('anonymous_id')
    
    # Try refreshing if no valid token
    if not access_token and refresh_token:
        refreshed = refresh_access_token(refresh_token)
        if refreshed and 'access_token' in refreshed:
            access_token = refreshed['access_token']
            request.session['spotify_access_token'] = access_token
            print("✅ Refreshed Spotify access token:", access_token)
        else:
            print("❌ Failed to refresh Spotify token.")
            access_token = None

    emotion_label = None
    song_link = None
    podcast_link = None
    chat_response = None

    if request.method == "POST":
        notes = request.POST.get('notes', '')
        if notes:
            emotion_result = detect_emotion(notes)
            emotion_label = emotion_result.get('detected_emotion')
            advice = ADVICE.get(emotion_label, "Take care of yourself.")

            # Refresh Spotify token before using
            refresh_token = request.session.get('spotify_refresh_token')

            refreshed = refresh_access_token(refresh_token)
            print("Raw refresh response:", refreshed)

            access_token = None
            if refreshed and 'access_token' in refreshed:
                access_token = refreshed.get('access_token')
                request.session['spotify_access_token'] = access_token
                print("Refreshed Spotify access token:", access_token)
            else:
                print("No access token received. Refresh failed or missing token")


            if access_token:
                print("Access token being used:", access_token)

                song_link = get_song_link_based_on_mood(emotion_label, access_token)
                podcast_link = get_podcast_link_based_on_mood(emotion_label, access_token)

            print("Detected Emotion:", emotion_label)
            print("Advice:", advice)
            print("Song:", song_link)
            print("Podcast:", podcast_link)

            # Create response message
            chat_response = f"Huey: You seem to be feeling {emotion_label.capitalize()}.\n{advice}"
            if song_link:
                chat_response += f"\nHere's a song you might like: {song_link}"
            if podcast_link:
                chat_response += f"\nAnd a podcast that may help: {podcast_link}"


            Mood.objects.create(
                user=request.user if request.user.is_authenticated else None,
                anonymous_id=None if request.user.is_authenticated else anonymous_id,
                notes=notes,
                emotion=emotion_label,
                advice=advice,
                song_link=song_link,
                podcast_link=podcast_link
            )


            # Store chat response temporarily and redirect
            request.session['chat_response'] = chat_response
            return redirect('index')

    # Get mood entries
    if request.user.is_authenticated:
        moods = Mood.objects.filter(user=request.user).order_by('timestamp')
    else:
        moods = Mood.objects.filter(anonymous_id=anonymous_id).order_by('timestamp')

    mood_data = [(m, m.emotion, m.song_link, m.podcast_link) for m in moods]
    labels = [m.timestamp.strftime('%b %d %I:%M %p') for m in moods]
    mood_values = [
        {
            'joy': 5,
            'sadness': 2,
            'anger': 3,
            'fear': 4,
            'neutral': 1,
            'surprise': 3
        }.get(m.emotion.lower(), 0)
        for m in moods
    ]

    # Pull response from session if available
    chat_response = request.session.pop('chat_response', None)

    context = {
        'labels': json.dumps(labels),
        'mood_values': json.dumps(mood_values),
        'mood_data': mood_data,
        'show_greeting': len(moods) == 0,
        'chat_response': chat_response,
    }

    code = request.GET.get('code')
    if code:
        token_data = exchange_code_for_token(code)
        print("Code exchange result:", token_data)

        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')

        request.session['spotify_access_token'] = access_token
        request.session['spotify_refresh_token'] = refresh_token

        if access_token:
            # Place Spotify profile code here
            headers = {
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.get("https://api.spotify.com/v1/me", headers=headers)
            user_data = response.json()
            spotify_user_id = user_data.get("id")


        refresh_token = token_data.get('refresh_token')
        print("Access token:", access_token)

    return render(request, 'moodtracker/index.html', context)


def exchange_code_for_token(code):
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://127.0.0.1:8000/',  # must match app's settings in Spotify
    }
    auth = (settings.SPOTIPY_CLIENT_ID, settings.SPOTIPY_CLIENT_SECRET)
    response = requests.post(url, data=data, auth=auth)
    return response.json()

# User registration
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

# Logout view
def custom_logout(request):
    logout(request)
    return redirect('login')

def test_spotify_token(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def refresh_access_token(refresh_token):
    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    auth = (settings.SPOTIPY_CLIENT_ID, settings.SPOTIPY_CLIENT_SECRET)
    response = requests.post(url, data=data, auth=auth)
    return response.json()

def connect_spotify(request):
    query_params = {
        'client_id': settings.SPOTIPY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': 'http://127.0.0.1:8000/',
        'scope': 'user-read-private',
        'show_dialog': 'true'
    }
    url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)
    return redirect(url)


