from flask import Flask, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import requests
import os
import urllib.parse
import base64
from dotenv import load_dotenv

# ----------------------
# Load environment variables from .env
# ----------------------
load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Debug prints
print("CLIENT_ID loaded:", "Yes" if CLIENT_ID else "No")
print("CLIENT_SECRET loaded:", "Yes" if CLIENT_SECRET else "No")

REDIRECT_URI = 'http://127.0.0.1:5000/callback'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SCOPES = 'user-read-private user-read-email'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church_party.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ----------------------
# Database Models (Keep your existing models)
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    album = db.Column(db.String(200))
    explicit = db.Column(db.Boolean, nullable=False)
    duration_ms = db.Column(db.Integer)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')

class LyricsCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    lyrics = db.Column(db.Text)
    is_clean = db.Column(db.Boolean, nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def home():
    return "Welcome to Safety Music Zone! Use /login to authenticate with Spotify."

# ----------------------
# OAuth Routes
# ----------------------
@app.route('/login')
def login():
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES
    }
    url = f"{SPOTIFY_AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Authorization failed', 400

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    # Use Basic Auth for client credentials
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    # Debug logging
    print("DEBUG: Token exchange status code:", response.status_code)
    print("DEBUG: Token exchange response:", response.text)

    token_info = response.json()

    if 'access_token' in token_info:
        session['spotify_token'] = token_info['access_token']
        return 'Spotify authentication successful! You can now use the app.'
    else:
        return jsonify(token_info), 400

# ----------------------
# Spotify API Integration using token from session
# ----------------------
def search_spotify(query):
    token = session.get('spotify_token')
    if not token:
        return {'error': 'Not authenticated with Spotify'}, 401

    url = 'https://api.spotify.com/v1/search'
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 5}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

@app.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    data = search_spotify(query)
    return jsonify(data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)