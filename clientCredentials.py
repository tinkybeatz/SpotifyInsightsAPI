from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

import os

from dotenv import load_dotenv

load_dotenv()

# Setup Spotify without requiring login
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    redirect_uri=os.getenv('REDIRECT_URI'),
    scope="playlist-read-public"  # You can use a different scope for public data
))

def get_playlist_info(playlist_id):
    if not playlist_id:
        return "No playlist ID provided"
    return f"Information for playlist with ID: {playlist_id}"