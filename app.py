from flask import Flask, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import requests
import os
import urllib.parse
import base64
import json
import time
from dotenv import load_dotenv
import eventlet

eventlet.monkey_patch()

# ----------------------
# Load environment variables from .env
# ----------------------
load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

print("CLIENT_ID loaded:", "Yes" if CLIENT_ID else "No")
print("CLIENT_SECRET loaded:", "Yes" if CLIENT_SECRET else "No")

REDIRECT_URI = 'https://safetymusiczone-production.up.railway.app/callback'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_URL = 'https://api.spotify.com/v1'
SCOPES = 'user-read-private user-read-email'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///church_party.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# Add this for session security
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# ----------------------
# Database Models
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    
    # Relationships
    requests = db.relationship('Request', backref='user', lazy=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(200), nullable=False)
    album = db.Column(db.String(200))
    explicit = db.Column(db.Boolean, nullable=False)
    duration_ms = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    
    # Relationships
    requests = db.relationship('Request', backref='song', lazy=True)
    lyrics_check = db.relationship('LyricsCheck', backref='song', lazy=True, uselist=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    
    # Relationships
    votes = db.relationship('Vote', backref='request', lazy=True)

class LyricsCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    lyrics = db.Column(db.Text)
    is_clean = db.Column(db.Boolean, nullable=False)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class SongLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    guest_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# ----------------------
# Lyrics Cache System
# ----------------------
LYRICS_CACHE_FILE = 'lyrics_cache.json'

def load_lyrics_cache():
    """Load lyrics cache from file"""
    try:
        with open(LYRICS_CACHE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_lyrics_cache(cache):
    """Save lyrics cache to file"""
    with open(LYRICS_CACHE_FILE, 'w') as f:
        json.dump(cache, f)

def get_cached_lyrics(artist, title):
    """Get lyrics from cache if available"""
    cache = load_lyrics_cache()
    cache_key = f"{artist.lower()}_{title.lower()}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        # Check if cache is not too old (30 days)
        if time.time() - cached_data.get('timestamp', 0) < 30 * 24 * 60 * 60:
            return cached_data.get('lyrics')
    return None

def cache_lyrics(artist, title, lyrics, api_used=None):
    """Cache lyrics for future use"""
    if not lyrics:
        return
        
    cache = load_lyrics_cache()
    cache_key = f"{artist.lower()}_{title.lower()}"
    cache[cache_key] = {
        'lyrics': lyrics,
        'timestamp': time.time(),
        'api_used': api_used
    }
    save_lyrics_cache(cache)

# ----------------------
# Lyrics API Testing & Selection
# ----------------------
def test_lyrics_apis(artist, title):
    """Test all available lyrics APIs and return working ones"""
    print(f"🔍 Testing lyrics APIs for: '{artist}' - '{title}'")
    
    clean_artist = urllib.parse.quote(artist.lower().strip())
    clean_title = urllib.parse.quote(title.lower().strip())
    
    apis_to_test = [
        # Most reliable APIs (tested)
        {
            'name': 'Lyrics.ovh',
            'url': f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', ''),
            'method': 'GET'
        },
        {
            'name': 'LRCLIB',
            'url': f"https://lrclib.net/api/get?artist_name={clean_artist}&track_name={clean_title}",
            'parser': lambda data: data.get('plainLyrics', ''),
            'method': 'GET'
        },
        {
            'name': 'Vanilla API',
            'url': f"https://vanilla.works.gd/api/lyrics?artist={clean_artist}&song={clean_title}",
            'parser': lambda data: data.get('lyrics', ''),
            'method': 'GET'
        },
        {
            'name': 'Some Random API',
            'url': f"https://some-random-api.com/lyrics?title={clean_title}",
            'parser': lambda data: data.get('lyrics', ''),
            'method': 'GET'
        },
        # Fallback APIs
        {
            'name': 'Lyrist (Vercel)',
            'url': f"https://lyrist.vercel.app/api/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', ''),
            'method': 'GET'
        },
        {
            'name': 'Genius Proxy',
            'url': f"https://genius.com/api/search/song?q={clean_artist}%20{clean_title}",
            'parser': lambda data: parse_genius_search(data, artist, title),
            'method': 'GET'
        }
    ]
    
    working_apis = []
    
    for api in apis_to_test:
        try:
            print(f"🧪 Testing {api['name']}...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            if api['method'] == 'GET':
                response = requests.get(api['url'], timeout=8, headers=headers)
            else:
                response = requests.post(api['url'], timeout=8, headers=headers)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                # Try to parse as JSON
                try:
                    data = response.json()
                    lyrics = api['parser'](data)
                    
                    if lyrics and len(lyrics.strip()) > 50:
                        print(f"   ✅ SUCCESS: Got {len(lyrics)} characters")
                        working_apis.append({
                            'name': api['name'],
                            'url': api['url'],
                            'parser': api['parser'],
                            'response_time': response.elapsed.total_seconds(),
                            'sample': lyrics[:100] + '...' if len(lyrics) > 100 else lyrics
                        })
                    else:
                        print(f"   ⚠️  No lyrics found")
                        
                except ValueError as e:
                    print(f"   ❌ JSON Parse Error: {e}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection Error")
        except Exception as e:
            print(f"   💥 Unexpected error: {str(e)}")
    
    # Sort by response time (fastest first)
    working_apis.sort(key=lambda x: x.get('response_time', 10))
    return working_apis

def parse_genius_search(data, artist, title):
    """Parse Genius API search results and try to get lyrics"""
    try:
        if data.get('response') and data['response'].get('sections'):
            for section in data['response']['sections']:
                if section.get('hits'):
                    for hit in section['hits']:
                        if hit.get('result'):
                            result = hit['result']
                            # Check if it's the right song
                            if (result.get('artist_names', '').lower() == artist.lower() or 
                                result.get('title', '').lower() == title.lower()):
                                # For Genius, we'd need to scrape the actual lyrics page
                                # This is a simplified version
                                return "Lyrics available on Genius (full implementation needed)"
        return ""
    except:
        return ""

# ----------------------
# Main Lyrics Function with Smart API Selection
# ----------------------

def get_lyrics(artist, title):
    """Main lyrics function using the working fetcher"""
    return get_lyrics_working(artist, title)
    print(f"🎵 Getting lyrics for: {artist} - {title}")
    
    # Try cache first
    cached_lyrics = get_cached_lyrics(artist, title)
    if cached_lyrics:
        print(f"📦 Using cached lyrics")
        return cached_lyrics
    
    clean_artist = urllib.parse.quote(artist.lower().strip())
    clean_title = urllib.parse.quote(title.lower().strip())
    
    # Updated API priority list with working endpoints
    apis_priority = [
        # Most reliable - Lyrics.ovh
        {
            'name': 'Lyrics.ovh',
            'url': f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', ''),
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        },
        # Second option - LRCLIB
        {
            'name': 'LRCLIB', 
            'url': f"https://lrclib.net/api/get?artist_name={clean_artist}&track_name={clean_title}",
            'parser': lambda data: data.get('plainLyrics', ''),
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        },
        # Third option - AZLyrics scraper (fallback)
        {
            'name': 'AZLyrics Proxy',
            'url': f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', ''),
            'headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        }
    ]
    
    best_lyrics = None
    best_api = None
    
    for api in apis_priority:
        try:
            print(f"🔍 Trying {api['name']}...")
            response = requests.get(api['url'], timeout=10, headers=api.get('headers', {}))
            
            if response.status_code == 200:
                data = response.json()
                lyrics = api['parser'](data)
                
                # Better validation for lyrics
                if lyrics and len(lyrics.strip()) > 100:  # Require at least 100 characters
                    print(f"✅ Success with {api['name']} - {len(lyrics)} characters")
                    best_lyrics = lyrics
                    best_api = api['name']
                    break
                else:
                    print(f"⚠️  {api['name']} returned insufficient lyrics: {len(lyrics) if lyrics else 0} chars")
            else:
                print(f"❌ {api['name']} returned {response.status_code}")
                
        except Exception as e:
            print(f"💥 {api['name']} failed: {str(e)}")
            continue
    
    # Cache the result
    cache_lyrics(artist, title, best_lyrics, best_api)
    
    if best_lyrics:
        print(f"🎯 Returning lyrics from {best_api}")
        return best_lyrics
    else:
        print("😞 No lyrics found from any API")
        # Return a helpful message instead of None
        return f"Lyrics for '{title}' by {artist} are not available in our database.\n\nThis could be because:\n• The song is very new\n• It's a regional song not in international databases\n• The lyrics APIs are temporarily unavailable\n\nYou can manually check lyrics on music services or approve based on Spotify's explicit flag."
    
# ----------------------
# Content Checking
# ----------------------
def check_lyrics_content(lyrics):
    """Check lyrics for inappropriate content"""
    if not lyrics:
        return True  # If we can't get lyrics, assume clean
    
    # Convert to lowercase for case-insensitive matching
    lyrics_lower = lyrics.lower()
    
    # List of inappropriate words/phrases
    inappropriate_words = [
        # Profanity
        'fuck', 'shit', 'bitch', 'asshole', 'damn', 'hell',
        # Sexual content
        'sex', 'naked', 'fucking', 'dick', 'pussy', 'whore',
        # Violence
        'kill', 'murder', 'gun', 'shoot', 'stab',
        # Drugs/alcohol
        'drugs', 'cocaine', 'weed', 'alcohol', 'drunk'
    ]
    
    # Check for any inappropriate words
    for word in inappropriate_words:
        if word in lyrics_lower:
            print(f"🚫 Found inappropriate word: {word}")
            return False
    
    return True

# ----------------------
# Spotify API Integration
# ----------------------
def search_spotify(query):
    token = session.get('spotify_token')
    if not token:
        return {'error': 'Not authenticated with Spotify'}, 401

    url = f'{SPOTIFY_API_URL}/search'
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": query, "type": "track", "limit": 5}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_track_details(track_id):
    """Get detailed track information from Spotify"""
    token = session.get('spotify_token')
    if not token:
        return None

    url = f'{SPOTIFY_API_URL}/tracks/{track_id}'
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# ----------------------
# Routes
# ----------------------
@app.route('/')
def home():
    return "Welcome to Safety Music Zone! Use /login to authenticate with Spotify."

# @app.route("/guest")
# def guest_page():
#     return render_template("guest.html")

@app.route('/test-form')
def test_form():
    """Serve the test form"""
    try:
        with open('test.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "test.html file not found. Please create the file in your project folder.", 404

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

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    token_info = response.json()

    if 'access_token' in token_info:
        session['spotify_token'] = token_info['access_token']
        return 'Spotify authentication successful! You can now use the app.'
    else:
        return jsonify(token_info), 400

@app.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    data = search_spotify(query)
    
    if 'tracks' in data:
        simplified_tracks = []
        for track in data['tracks']['items']:
            simplified_tracks.append({
                'spotify_id': track['id'],
                'title': track['name'],
                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                'album': track['album']['name'],
                'explicit': track['explicit'],
                'duration_ms': track['duration_ms'],
                'preview_url': track['preview_url'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
        return jsonify({'tracks': simplified_tracks})
    
    return jsonify(data)

@app.route('/request-song', methods=['POST'])
def request_song():
    """Submit a song request"""
    try:
        token = session.get('spotify_token')
        if not token:
            return jsonify({"error": "Not authenticated with Spotify. Please visit /login first."}), 401

        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        spotify_id = data.get('spotify_id')
        
        if not spotify_id:
            return jsonify({"error": "Spotify ID is required"}), 400

        # Check if song exists in our database
        song = Song.query.filter_by(spotify_id=spotify_id).first()
        
        if not song:
            # Fetch song details from Spotify
            track_data = get_track_details(spotify_id)
            if not track_data:
                return jsonify({"error": "Could not fetch song details from Spotify"}), 400
            
            # Create new song record
            song = Song(
                spotify_id=track_data['id'],
                title=track_data['name'],
                artist=track_data['artists'][0]['name'] if track_data['artists'] else 'Unknown',
                album=track_data['album']['name'],
                explicit=track_data['explicit'],
                duration_ms=track_data['duration_ms'],
                image_url=track_data['album']['images'][0]['url'] if track_data['album']['images'] else None
            )
            db.session.add(song)
            db.session.commit()

            # Check lyrics asynchronously
            def check_lyrics_async(song_id, artist, title):
                with app.app_context():
                    try:
                        lyrics = get_lyrics(artist, title)
                        is_clean = check_lyrics_content(lyrics) if lyrics else True
                        
                        # Update lyrics check
                        lyrics_check = LyricsCheck.query.filter_by(song_id=song_id).first()
                        if lyrics_check:
                            lyrics_check.lyrics = lyrics[:1000] if lyrics else None
                            lyrics_check.is_clean = is_clean
                        else:
                            lyrics_check = LyricsCheck(
                                song_id=song_id,
                                lyrics=lyrics[:1000] if lyrics else None,
                                is_clean=is_clean
                            )
                            db.session.add(lyrics_check)
                        
                        db.session.commit()
                        
                        # If lyrics are bad, auto-reject
                        if not is_clean:
                            request_obj = Request.query.filter_by(song_id=song_id, status='Pending').first()
                            if request_obj:
                                request_obj.status = 'Rejected'
                                db.session.commit()
                                socketio.emit('request_rejected', {
                                    'request_id': request_obj.id,
                                    'song_title': request_obj.song.title,
                                    'reason': 'Inappropriate lyrics detected'
                                })
                    
                    except Exception as e:
                        print(f"DEBUG: Async lyrics check failed: {str(e)}")

            # Start async lyrics check
            import threading
            thread = threading.Thread(target=check_lyrics_async, args=(song.id, song.artist, song.title))
            thread.daemon = True
            thread.start()

        # Use a default user
        temp_user = User.query.filter_by(username='guest').first()
        if not temp_user:
            temp_user = User(username='guest', password_hash='temp', role='guest')
            db.session.add(temp_user)
            db.session.commit()

        # Check if this song is already pending
        existing_request = Request.query.filter_by(
            user_id=temp_user.id, 
            song_id=song.id, 
            status='Pending'
        ).first()
        
        if existing_request:
            return jsonify({"error": "You already have a pending request for this song"}), 400

        # Check if song should be auto-rejected based on explicit flag
        if song.explicit:
            new_request = Request(
                user_id=temp_user.id, 
                song_id=song.id, 
                status='Rejected'
            )
            db.session.add(new_request)
            db.session.commit()
            
            return jsonify({
                "error": "Song automatically rejected due to explicit content",
                "reasons": ["Explicit content flagged by Spotify"]
            }), 400

        # Create request record
        new_request = Request(
            user_id=temp_user.id, 
            song_id=song.id, 
            status='Pending'
        )
        db.session.add(new_request)
        db.session.commit()

        socketio.emit('new_request', {
            'request_id': new_request.id,
            'song_title': song.title,
            'artist': song.artist,
            'explicit': song.explicit
        })

        return jsonify({
            "message": "Song request submitted successfully!",
            "request_id": new_request.id,
            "song_title": song.title,
            "artist": song.artist,
            "explicit": song.explicit,
            "lyrics_checked": False  # Will be checked async
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to submit request: {str(e)}"}), 500

# ----------------------
# New Lyrics Testing Routes
# ----------------------
@app.route('/test-lyrics-apis')
def test_lyrics_apis_route():
    """Test all lyrics APIs with popular songs"""
    test_songs = [
        {"artist": "Ed Sheeran", "title": "Shape of You"},
        {"artist": "The Weeknd", "title": "Blinding Lights"},
        {"artist": "Queen", "title": "Bohemian Rhapsody"},
        {"artist": "Adele", "title": "Hello"},
        {"artist": "Taylor Swift", "title": "Shake It Off"}
    ]
    
    results = {}
    
    for song in test_songs:
        artist = song["artist"]
        title = song["title"]
        print(f"\n🎵 Testing: {artist} - {title}")
        print("=" * 50)
        
        working_apis = test_lyrics_apis(artist, title)
        
        # Convert to JSON-serializable format
        serializable_apis = []
        for api in working_apis:
            serializable_apis.append({
                'name': api['name'],
                'url': api['url'],
                'response_time': api.get('response_time', 0),
                'sample': api.get('sample', '')[:100] + '...' if api.get('sample') and len(api.get('sample', '')) > 100 else api.get('sample', '')
            })
        
        results[f"{artist} - {title}"] = {
            'working_apis': serializable_apis,
            'working_count': len(working_apis)
        }
    
    return jsonify(results)

def get_lyrics(artist, title):
    """Smart lyrics fetching with caching and multiple fallbacks"""
    print(f"🎵 Getting lyrics for: {artist} - {title}")
    
    # Try cache first
    cached_lyrics = get_cached_lyrics(artist, title)
    if cached_lyrics:
        print(f"📦 Using cached lyrics")
        return cached_lyrics
    
    clean_artist = urllib.parse.quote(artist.lower().strip())
    clean_title = urllib.parse.quote(title.lower().strip())
    
    # Updated priority list based on test results
    apis_priority = [
        # Most reliable based on testing
        {
            'name': 'Lyrics.ovh',
            'url': f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', '')
        },
        {
            'name': 'LRCLIB',
            'url': f"https://lrclib.net/api/get?artist_name={clean_artist}&track_name={clean_title}",
            'parser': lambda data: data.get('plainLyrics', '')
        },
        # Fallback - Genius provides limited lyrics but works consistently
        {
            'name': 'Genius Proxy',
            'url': f"https://genius.com/api/search/song?q={clean_artist}%20{clean_title}",
            'parser': lambda data: parse_genius_lyrics(data, artist, title)
        }
    ]
    
    best_lyrics = None
    best_api = None
    
    for api in apis_priority:
        try:
            print(f"🔍 Trying {api['name']}...")
            response = requests.get(api['url'], timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200:
                data = response.json()
                lyrics = api['parser'](data)
                
                if lyrics and len(lyrics.strip()) > 50:
                    print(f"✅ Success with {api['name']} - {len(lyrics)} characters")
                    best_lyrics = lyrics
                    best_api = api['name']
                    break  # Stop at first successful API
                else:
                    print(f"⚠️  {api['name']} returned insufficient lyrics")
            else:
                print(f"❌ {api['name']} returned {response.status_code}")
                
        except Exception as e:
            print(f"💥 {api['name']} failed: {str(e)}")
            continue
    
    # Cache the result
    cache_lyrics(artist, title, best_lyrics, best_api)
    
    if best_lyrics:
        print(f"🎯 Returning lyrics from {best_api}")
    else:
        print("😞 No lyrics found from any API")
    
    return best_lyrics

@app.route('/dj/manual-lyrics/<int:song_id>', methods=['POST'])
def manual_lyrics_input(song_id):
    """Allow DJ to manually input lyrics when APIs fail"""
    try:
        data = request.json
        lyrics_text = data.get('lyrics', '')
        
        if not lyrics_text:
            return jsonify({"error": "No lyrics provided"}), 400
        
        # Update or create lyrics check
        lyrics_check = LyricsCheck.query.filter_by(song_id=song_id).first()
        if lyrics_check:
            lyrics_check.lyrics = lyrics_text[:2000]  # Limit length
            lyrics_check.is_clean = check_lyrics_content(lyrics_text)
        else:
            lyrics_check = LyricsCheck(
                song_id=song_id,
                lyrics=lyrics_text[:2000],
                is_clean=check_lyrics_content(lyrics_text)
            )
            db.session.add(lyrics_check)
        
        db.session.commit()
        
        return jsonify({
            "message": "Lyrics manually added successfully",
            "is_clean": lyrics_check.is_clean
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add lyrics: {str(e)}"}), 500

def parse_genius_lyrics(data, artist, title):
    """Better Genius lyrics parser"""
    try:
        if data.get('response') and data['response'].get('sections'):
            for section in data['response']['sections']:
                if section.get('hits'):
                    for hit in section['hits']:
                        if hit.get('result'):
                            result = hit['result']
                            # Check if it's the right song
                            match_score = 0
                            if result.get('artist_names', '').lower() == artist.lower():
                                match_score += 2
                            if result.get('title', '').lower() == title.lower():
                                match_score += 1
                            
                            if match_score >= 1:  # At least partial match
                                # For now, return a message since we can't easily get full lyrics
                                return f"Lyrics available on Genius for '{result.get('title', '')}' by {result.get('artist_names', '')}"
        return ""
    except:
        return ""

@app.route('/lyrics-cache-info')
def lyrics_cache_info():
    """Get info about cached lyrics"""
    cache = load_lyrics_cache()
    return jsonify({
        "cached_songs_count": len(cache),
        "cached_songs": list(cache.keys())[:10]  # First 10
    })

@app.route('/lyrics-summary')
def lyrics_summary():
    """Show which APIs are working best"""
    return jsonify({
        "reliable_apis": [
            {
                "name": "Lyrics.ovh",
                "status": "✅ Working",
                "description": "Most reliable, good coverage"
            },
            {
                "name": "LRCLIB", 
                "status": "✅ Working (some songs)",
                "description": "Good when available"
            },
            {
                "name": "Genius Proxy",
                "status": "✅ Working (limited)",
                "description": "Always works but limited lyrics"
            }
        ],
        "unreliable_apis": [
            "Vanilla API - Connection issues",
            "Some Random API - 403 Forbidden", 
            "Lyrist (Vercel) - Rate limited"
        ],
        "recommendation": "Use Lyrics.ovh as primary, LRCLIB as fallback"
    })

@app.route('/quick-test/<artist>/<title>')
def quick_test(artist, title):
    """Quick test of lyrics for a specific song"""
    lyrics = get_lyrics(artist, title)
    
    return jsonify({
        "artist": artist,
        "title": title,
        "lyrics_found": lyrics is not None,
        "lyrics_length": len(lyrics) if lyrics else 0,
        "preview": lyrics[:200] + "..." if lyrics and len(lyrics) > 200 else lyrics
    })

# ----------------------
# Working Lyrics Scraper
# ----------------------
def scrape_lyrics_direct(artist, title):
    """Direct lyrics scraping as fallback"""
    try:
        # Clean the artist and title for URL
        clean_artist = artist.lower().replace(' ', '-').replace('&', 'and')
        clean_title = title.lower().replace(' ', '-')
        
        # Try AZLyrics style URL
        url = f"https://www.azlyrics.com/lyrics/{clean_artist}/{clean_title}.html"
        
        print(f"🔍 Trying direct scrape from: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Simple HTML parsing to extract lyrics
            import re
            # Look for lyrics between specific div tags (AZLyrics structure)
            lyrics_match = re.search(r'<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement\. Sorry\. -->(.*?)</div>', response.text, re.DOTALL)
            
            if lyrics_match:
                lyrics = lyrics_match.group(1).strip()
                # Clean up the lyrics
                lyrics = re.sub(r'<br>', '\n', lyrics)
                lyrics = re.sub(r'<.*?>', '', lyrics)
                lyrics = re.sub(r'\n\s*\n', '\n\n', lyrics)  # Remove extra blank lines
                
                if len(lyrics) > 100:
                    print(f"✅ Successfully scraped {len(lyrics)} characters")
                    return lyrics
        
        return None
    except Exception as e:
        print(f"❌ Direct scrape failed: {e}")
        return None

def get_lyrics_working(artist, title):
    """Working lyrics fetcher with multiple fallbacks"""
    print(f"🎵 Getting lyrics for: {artist} - {title}")
    
    # Try cache first
    cached_lyrics = get_cached_lyrics(artist, title)
    if cached_lyrics and len(cached_lyrics.strip()) > 100:
        print(f"📦 Using cached lyrics")
        return cached_lyrics
    
    # Priority 1: Lyrics.ovh (most reliable)
    try:
        clean_artist = urllib.parse.quote(artist)
        clean_title = urllib.parse.quote(title)
        url = f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}"
        
        print(f"🔍 Trying Lyrics.ovh...")
        response = requests.get(url, timeout=8, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get('lyrics', '')
            if lyrics and len(lyrics.strip()) > 100:
                print(f"✅ Lyrics.ovh success: {len(lyrics)} characters")
                cache_lyrics(artist, title, lyrics, 'Lyrics.ovh')
                return lyrics
    except Exception as e:
        print(f"❌ Lyrics.ovh failed: {e}")
    
    # Priority 2: LRCLIB
    try:
        url = f"https://lrclib.net/api/get?artist_name={urllib.parse.quote(artist)}&track_name={urllib.parse.quote(title)}"
        print(f"🔍 Trying LRCLIB...")
        response = requests.get(url, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            lyrics = data.get('plainLyrics', '')
            if lyrics and len(lyrics.strip()) > 100:
                print(f"✅ LRCLIB success: {len(lyrics)} characters")
                cache_lyrics(artist, title, lyrics, 'LRCLIB')
                return lyrics
    except Exception as e:
        print(f"❌ LRCLIB failed: {e}")
    
    # Priority 3: Direct scraping as last resort
    print(f"🔍 Trying direct scraping...")
    lyrics = scrape_lyrics_direct(artist, title)
    if lyrics:
        cache_lyrics(artist, title, lyrics, 'Direct Scrape')
        return lyrics
    
    # Final fallback - return a helpful message
    fallback_msg = f"""We couldn't find lyrics for "{title}" by {artist} in our databases.
                        This is common for:
                        • Newly released songs
                        • Lesser-known artists  
                        • Regional or non-English songs
                        • Songs with limited online presence

                        What you can do:
                        1. Check Spotify or YouTube Music for lyrics
                        2. Search manually on lyrics websites
                        3. Use your judgment based on the artist and song title
                        4. The Spotify explicit flag is still reliable for content filtering

                        If you believe this song should have lyrics available, try the "Refresh Lyrics" button to search again."""
    
    cache_lyrics(artist, title, fallback_msg, 'Not Found')
    return fallback_msg

# ----------------------
# Existing Routes (Updated)
# ----------------------
@app.route('/approved-songs')
def approved_songs():
    """Get all approved songs with like counts - NO DUPLICATES"""
    try:
        # Get unique approved songs (group by song, not by request)
        approved_songs = db.session.query(
            Song
        ).join(
            Request, Song.id == Request.song_id
        ).filter(
            Request.status == 'Approved'
        ).group_by(
            Song.id
        ).all()
        
        songs_data = []
        for song in approved_songs:
            # Count likes for this song
            like_count = SongLike.query.filter_by(song_id=song.id).count()
            
            # Count how many times this song was requested (popularity)
            request_count = Request.query.filter_by(song_id=song.id, status='Approved').count()
            
            # Check if current user liked this song
            guest_id = request.args.get('guest_id')
            user_liked = False
            if guest_id:
                user_like = SongLike.query.filter_by(song_id=song.id, guest_id=guest_id).first()
                user_liked = user_like is not None
            
            songs_data.append({
                'song_id': song.id,
                'title': song.title,
                'artist': song.artist,
                'image_url': song.image_url,
                'like_count': like_count,
                'request_count': request_count,
                'user_liked': user_liked
            })
        
        # Sort by like count (most liked first)
        songs_data.sort(key=lambda x: x['like_count'], reverse=True)
        
        return jsonify(songs_data)
    
    except Exception as e:
        print(f"DEBUG: Error in approved-songs: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/toggle-like', methods=['POST'])
def toggle_like():
    """Toggle like on a song"""
    try:
        data = request.json
        song_id = data.get('song_id')
        guest_id = data.get('guest_id')
        
        if not song_id or not guest_id:
            return jsonify({"error": "Song ID and Guest ID required"}), 400
        
        # Check if like exists
        existing_like = SongLike.query.filter_by(song_id=song_id, guest_id=guest_id).first()
        
        if existing_like:
            # Remove like
            db.session.delete(existing_like)
            message = "Like removed"
        else:
            # Add like
            new_like = SongLike(song_id=song_id, guest_id=guest_id)
            db.session.add(new_like)
            message = "Like added"
        
        db.session.commit()
        
        # Emit socket event for real-time updates
        socketio.emit('like_updated', {
            'song_id': song_id,
            'guest_id': guest_id,
            'action': 'removed' if existing_like else 'added'
        })
        
        return jsonify({"message": message})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/dj/requests')
def dj_requests():
    """DJ view of all pending requests - FIXED with images"""
    try:
        pending_requests = db.session.query(
            Request, Song, User, LyricsCheck
        ).join(
            Song, Request.song_id == Song.id
        ).join(
            User, Request.user_id == User.id
        ).outerjoin(
            LyricsCheck, Song.id == LyricsCheck.song_id
        ).filter(
            Request.status == 'Pending'
        ).all()
        
        requests_data = []
        for req, song, user, lyrics_check in pending_requests:
            requests_data.append({
                'request_id': req.id,
                'song_id': song.id,
                'song_title': song.title,
                'artist': song.artist,
                'explicit': song.explicit,
                'album': song.album,
                'duration_ms': song.duration_ms,
                'image_url': song.image_url,  # Make sure this is included
                'requested_by': user.username,
                'lyrics_checked': lyrics_check is not None,
                'lyrics_clean': lyrics_check.is_clean if lyrics_check else True,
                'has_lyrics': lyrics_check.lyrics is not None if lyrics_check else False
            })
        
        return jsonify(requests_data)
    
    except Exception as e:
        return jsonify({"error": f"Failed to fetch requests: {str(e)}"}), 500

@app.route('/dj/approve/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    """Approve a song request"""
    try:
        request_obj = Request.query.get_or_404(request_id)
        request_obj.status = 'Approved'
        db.session.commit()

        socketio.emit('request_approved', {
            'request_id': request_obj.id,
            'song_title': request_obj.song.title
        })

        return jsonify({"message": "Request approved successfully!"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to approve request: {str(e)}"}), 500

@app.route('/dj/reject/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    """Reject a song request"""
    try:
        request_obj = Request.query.get_or_404(request_id)
        request_obj.status = 'Rejected'
        db.session.commit()

        socketio.emit('request_rejected', {
            'request_id': request_obj.id,
            'song_title': request_obj.song.title
        })

        return jsonify({"message": "Request rejected successfully!"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to reject request: {str(e)}"}), 500

# ----------------------
# DJ Lyrics Routes (Add these to your app.py)
# ----------------------

@app.route('/dj/lyrics/<int:song_id>')
def get_lyrics_for_song(song_id):
    """Get lyrics for a specific song"""
    try:
        lyrics_check = LyricsCheck.query.filter_by(song_id=song_id).first()
        song = Song.query.get(song_id)
        
        if not song:
            return jsonify({
                "error": "Song not found",
                "song_id": song_id
            }), 404
        
        response_data = {
            "song_id": song_id,
            "song_title": song.title,
            "artist": song.artist,
            "explicit": song.explicit,
            "lyrics_available": False,
            "lyrics": None,
            "is_clean": True
        }
        
        if lyrics_check:
            response_data.update({
                "lyrics_available": lyrics_check.lyrics is not None,
                "lyrics": lyrics_check.lyrics,
                "is_clean": lyrics_check.is_clean
            })
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"DEBUG: Error in get_lyrics_for_song: {str(e)}")
        return jsonify({
            "error": f"Failed to fetch lyrics: {str(e)}",
            "song_id": song_id
        }), 500

@app.route('/dj/refresh-lyrics/<int:song_id>', methods=['POST'])
def refresh_lyrics(song_id):
    """Manually refresh lyrics for a song"""
    try:
        song = Song.query.get(song_id)
        if not song:
            return jsonify({"error": "Song not found"}), 404
        
        print(f"DEBUG: Manually refreshing lyrics for {song.title}")
        lyrics = get_lyrics(song.artist, song.title)
        is_clean = check_lyrics_content(lyrics) if lyrics else True
        
        # Update or create lyrics check
        lyrics_check = LyricsCheck.query.filter_by(song_id=song_id).first()
        if lyrics_check:
            lyrics_check.lyrics = lyrics[:1000] if lyrics else None
            lyrics_check.is_clean = is_clean
        else:
            lyrics_check = LyricsCheck(
                song_id=song_id,
                lyrics=lyrics[:1000] if lyrics else None,
                is_clean=is_clean
            )
            db.session.add(lyrics_check)
        
        db.session.commit()
        
        return jsonify({
            "message": "Lyrics refreshed successfully",
            "lyrics_available": lyrics is not None,
            "is_clean": is_clean,
            "song_title": song.title
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to refresh lyrics: {str(e)}"}), 500

@app.route('/dj/override/<int:request_id>', methods=['POST'])
def override_lyrics_check(request_id):
    """Allow DJ to manually override lyrics check and approve song"""
    try:
        request_obj = Request.query.get_or_404(request_id)
        
        # Only allow override if song was rejected due to lyrics
        if request_obj.status != 'Rejected':
            return jsonify({"error": "Can only override rejected requests"}), 400
        
        # Update status to approved
        request_obj.status = 'Approved'
        db.session.commit()

        socketio.emit('request_approved', {
            'request_id': request_obj.id,
            'song_title': request_obj.song.title,
            'overridden': True
        })

        return jsonify({
            "message": "Request manually approved despite lyrics check!",
            "request_id": request_obj.id,
            "song_title": request_obj.song.title
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to override request: {str(e)}"}), 500

@app.route('/guest-stats')
def guest_stats():
    """Get guest statistics"""
    try:
        total_requests = Request.query.count()
        pending_requests = Request.query.filter_by(status='Pending').count()
        unique_guests = db.session.query(Request.user_id).distinct().count()
        
        return jsonify({
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'unique_guests': unique_guests
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/popular-songs')
def popular_songs():
    """Get most requested songs"""
    try:
        popular = db.session.query(
            Song.title,
            Song.artist,
            db.func.count(Request.id).label('request_count')
        ).join(
            Request, Song.id == Request.song_id
        ).group_by(
            Song.id
        ).order_by(
            db.desc('request_count')
        ).limit(10).all()
        
        return jsonify([{
            'title': song.title,
            'artist': song.artist,
            'request_count': song.request_count
        } for song in popular])
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/guest')
def guest_interface():
    """Serve the mobile-friendly guest interface"""
    try:
        with open('guest.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "guest.html file not found", 404

@app.route('/debug-auth')
def debug_auth():
    """Debug authentication status"""
    return jsonify({
        "client_id_loaded": bool(os.getenv('SPOTIFY_CLIENT_ID')),
        "session_token": 'spotify_token' in session,
        "token_exists": bool(session.get('spotify_token'))
    })

@app.route('/debug-lyrics/<artist>/<title>')
def debug_lyrics(artist, title):
    """Debug lyrics fetching for a specific song"""
    print(f"🔍 Debugging lyrics for: {artist} - {title}")
    
    # Test the improved lyrics function
    lyrics = get_lyrics(artist, title)
    
    return jsonify({
        "artist": artist,
        "title": title,
        "lyrics_found": lyrics is not None,
        "lyrics_length": len(lyrics) if lyrics else 0,
        "lyrics_preview": lyrics[:500] + "..." if lyrics and len(lyrics) > 500 else lyrics,
        "cache_info": "Check server logs for detailed API testing"
    })

# Create all tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)