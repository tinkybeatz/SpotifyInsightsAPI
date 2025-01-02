import os

from flask import Flask, session, url_for, request, redirect

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '13e6c218b5674f5ab0617df6fe43ec2d'
client_secret = 'c7472ba1952a4faf823ecd999ab77290'
redirect_uri = 'https://localhost:5000/callback'
scope = 'playlist-read-private'

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)
sp = Spotify(auth_manager=sp_oauth)

def check_auth():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

@app.route('/')
def home():
    auth_check = check_auth()
    if auth_check:
        return auth_check
    return redirect(url_for('get_private_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_private_playlists'))

@app.route('/private_playlists')
def get_private_playlists():
    auth_check = check_auth()
    if auth_check:
        return auth_check

    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['id'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_html = '<br>'.join([f'{name}: {id} | {url}' for name, id, url in playlists_info])

    return playlists_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)