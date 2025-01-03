# WORKING CODE
# from flask import Flask, session, url_for, request, redirect

# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy.cache_handler import FlaskSessionCacheHandler

# from dotenv import load_dotenv
# import os

# load_dotenv()

# app = Flask(__name__)

# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# client_id = os.getenv('CLIENT_ID')
# client_secret = os.getenv('CLIENT_SECRET')
# redirect_uri = os.getenv('REDIRECT_URI')
# scope = 'playlist-read-private'

# cache_handler = FlaskSessionCacheHandler(session)
# sp_oauth = SpotifyOAuth(
#     client_id=client_id,
#     client_secret=client_secret,
#     redirect_uri=redirect_uri,
#     scope=scope,
#     cache_handler=cache_handler,
#     show_dialog=True
# )
# sp = Spotify(auth_manager=sp_oauth)

# def check_auth():
#     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
#         auth_url = sp_oauth.get_authorize_url()
#         return redirect(auth_url)

# @app.route('/')
# def home():
#     auth_check = check_auth()
#     if auth_check:
#         return auth_check
#     return redirect(url_for('get_private_playlists'))

# @app.route('/callback')
# def callback():
#     sp_oauth.get_access_token(request.args['code'])
#     return redirect(url_for('get_private_playlists'))

# @app.route('/private_playlists')
# def get_private_playlists():
#     auth_check = check_auth()
#     if auth_check:
#         return auth_check

#     playlists = sp.current_user_playlists()
#     playlists_info = [(pl['name'], pl['id'], pl['external_urls']['spotify']) for pl in playlists['items']]
#     playlists_html = '<br>'.join([f'{name}: {id} | {url}' for name, id, url in playlists_info])

#     return playlists_html

# @app.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('home'))

# @app.errorhandler(Exception)
# def handle_exception(e):
#     return {"error": str(e)}, 500

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, redirect, url_for, session
import os
import authorizationCode  # Importing the logged-in functionality
import clientCredentials  # Importing the non-logged-in functionality

from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Enable CORS for all routes
CORS(app, origins=["http://localhost:4200", ["https://spotify-insights-ten.vercel.app"]])

@app.route('/')
def home():
    return 'yes'

@app.route('/callback')
def callback():
    return authorizationCode.callback()

@app.route('/private_playlists')
def private_playlists():
    # Fetch playlists only for logged-in users
    return authorizationCode.get_playlists()

@app.route('/playlist_info/<playlist_id>')
def playlist_info(playlist_id):
    # Fetch playlists only for logged-in users
    return clientCredentials.get_playlist_info(playlist_id)

@app.route('/logout')
def logout():
    # Clear session to log out
    session.clear()
    return redirect(url_for('home'))

@app.errorhandler(Exception)
def handle_exception(e):
    return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)