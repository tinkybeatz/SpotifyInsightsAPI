from flask import Flask, redirect, url_for, session, jsonify
import os
import authorizationCode  # logged-in functionality
import clientCredentials  # non-logged-in functionality
from flask_cors import CORS

app = Flask(__name__)

# IMPORTANT: must be set in env vars; otherwise sessions & OAuth will break
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'unset-secret-key')

# Allow your frontend origins (add others as needed)
CORS(app, origins=[
    "http://localhost:4200",
    "https://spotify-insights-ten.vercel.app",
    "https://playlytix.tinky.cloud"
])

@app.route("/")
def home():
    return "yes"

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/callback")
def callback():
    return authorizationCode.callback()

@app.route("/private_playlists")
def private_playlists():
    return authorizationCode.get_playlists()

@app.route("/playlist_info/<playlist_id>")
def playlist_info(playlist_id):
    return clientCredentials.get_playlist_info(playlist_id)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.errorhandler(Exception)
def handle_exception(e):
    # Keep this simple & JSON
    return jsonify(error=str(e)), 500

# ---- Dev entrypoint only (local runs) ----
if __name__ == "__main__":
    # Bind to 0.0.0.0 so container/proxy can reach it
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)