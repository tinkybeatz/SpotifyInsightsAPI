from flask import Flask, redirect, url_for, session
import os
import authorizationCode  # Importing the logged-in functionality
import clientCredentials  # Importing the non-logged-in functionality

from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Enable CORS for all routes
CORS(app, origins=["http://localhost:4200", "https://spotify-insights-ten.vercel.app"])

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
    # Fetch public playlists infos
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