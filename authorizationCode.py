from flask import session, redirect, url_for, request
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize SpotifyOAuth with session-based cache
cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    redirect_uri=os.getenv('REDIRECT_URI'),
    scope='playlist-read-private',
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

def check_auth():
    """Check if the user is authenticated"""
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return None

def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('private_playlists'))

def get_playlists():
    """Fetch and return playlists for logged-in user"""
    auth_check = check_auth()
    if auth_check:
        return auth_check
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['id'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}: {id} | {url}' for name, id, url in playlists_info])
    return playlists_html

# def get_playlist_info(playlist_id):
#     auth_check = check_auth()
#     if auth_check:
#         return auth_check
#     if not playlist_id:
#         return "No playlist ID provided"
#     playlist = sp.playlist(playlist_id)
#     return playlist