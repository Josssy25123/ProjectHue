import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings

# Set up the authentication scope
scope = "user-library-read playlist-read-private"

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope=scope
    ))
    return sp

def get_song_link_based_on_mood(mood):
    sp = authenticate_spotify()
    query = f"{mood} song"
    results = sp.search(q=query, limit=5, type='track', market='US')

    music_links = []
    for track in results['tracks']['items']:
        music_links.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'url':track['external_urls']['wpotify'],
            'album':track['album']['name'],
            'cover_image': track['album']['images'][0]['url']
        })
    return music_links