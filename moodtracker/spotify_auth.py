import random
import requests
import traceback
import base64
import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()

# Set up Spotify authentication scope
def create_spotify_client(access_token):
    """Initialize Spotify client with credentials from environment variables."""
    return spotipy.Spotify(auth=access_token)

# Songs
def get_song_link_based_on_mood(mood, access_token=None):
    """Return a song link based on the user's mood, with fallback."""
    if not access_token:
        print("Missing Spotify access token for song.")
        return "https://open.spotify.com/track/5qmq61DAAOUaW8AUo8xKhh"  # Fallback: popular song

    sp = spotipy.Spotify(auth=access_token)

    mood_query = {
        "joy": "happy upbeat songs",
        "sadness": "comforting music",
        "anger": "calm music",
        "fear": "relaxing songs",
        "surprise": "new hits",
        "neutral": "lofi chill beats"
    }.get(mood.lower(), mood)

    try:
        results = sp.search(q=mood_query, type='track', limit=10)
        tracks = results['tracks']['items']
        print("Track search results:", tracks)
        if tracks:
            return random.choice(tracks)['external_urls']['spotify']
        else:
            print("No tracks found. Returning fallback song.")
            return "https://open.spotify.com/track/5qmq61DAAOUaW8AUo8xKhh"  # Fallback song link
    except Exception as e:
        print(f"Error fetching song for mood '{mood}': {e}")
        traceback.print_exc()
        return "https://open.spotify.com/track/5qmq61DAAOUaW8AUo8xKhh"  # Fallback

# Podcasts
def get_podcast_link_based_on_mood(mood, access_token=None):
    """Return a podcast link based on the user's mood, with fallback."""
    if not access_token:
        print("Missing Spotify access token for podcast.")
        return "https://open.spotify.com/show/6kAsbP8pxwaU3bDWe0es5T"  # Fallback: popular podcast

    sp = spotipy.Spotify(auth=access_token)

    mood_query = {
        "sadness": "mental health",
        "fear": "overcoming fear",
        "anxiety": "calm anxiety",
        "joy": "positive mindset",
        "anger": "anger management",
        "surprise": "motivational podcasts",
        "neutral": "chill discussions"
    }.get(mood.lower(), mood)

    try:
        results = sp.search(q=mood_query, type='show', limit=10)
        shows = results['shows']['items']
        print("Podcast search results:", shows)
        if shows:
            return random.choice(shows)['external_urls']['spotify']
        else:
            print("No podcasts found. Returning fallback podcast.")
            return "https://open.spotify.com/show/6kAsbP8pxwaU3bDWe0es5T"  # Fallback podcast link
    except Exception as e:
        print(f"Error fetching podcast for mood '{mood}': {e}")
        traceback.print_exc()
        return "https://open.spotify.com/show/6kAsbP8pxwaU3bDWe0es5T"  # Fallback

# Refresh access token
def refresh_access_token(refresh_token):
    auth_header = base64.b64encode(f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to refresh Spotify access token:", response.json())
        return None
