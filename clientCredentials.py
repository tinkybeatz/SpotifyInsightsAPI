import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

import os

from dotenv import load_dotenv

load_dotenv()

auth_manager = SpotifyClientCredentials(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_playlist_info(playlist_id):
    if not playlist_id:
        return "No playlist ID provided"
    playlist = sp.playlist(playlist_id)
    return playlist