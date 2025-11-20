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

print("CLIENT_ID loaded:", "Yes" if CLIENT_ID else "No")
print("CLIENT_SECRET loaded:", "Yes" if CLIENT_SECRET else "No")

REDIRECT_URI = 'http://127.0.0.1:5000/callback'
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
# Database Models - FIXED WITH RELATIONSHIPS
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
# Lyrics API Integration
# ----------------------

def get_lyrics(artist, title):
    """Fetch lyrics from multiple APIs with better error handling"""
    # Clean the artist and title
    clean_artist = urllib.parse.quote(artist.lower().strip())
    clean_title = urllib.parse.quote(title.lower().strip())
    
    print(f"DEBUG: Searching lyrics for '{artist}' - '{title}'")
    
    # Try multiple lyrics APIs as fallback
    apis_to_try = [
        {
            'name': 'Lyrics.ovh',
            'url': f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', '')
        },
        {
            'name': 'Lyrist.vercel.app',
            'url': f"https://lyrist.vercel.app/api/{clean_artist}/{clean_title}",
            'parser': lambda data: data.get('lyrics', '')
        }
    ]
    
    for api in apis_to_try:
        try:
            print(f"DEBUG: Trying {api['name']}...")
            response = requests.get(api['url'], timeout=8, headers={
                'User-Agent': 'SafetyMusicZone/1.0'
            })
            
            # Check if response is JSON
            content_type = response.headers.get('content-type', '')
            if 'application/json' not in content_type:
                print(f"DEBUG: {api['name']} returned non-JSON: {content_type}")
                continue
                
            if response.status_code == 200:
                data = response.json()
                lyrics = api['parser'](data)
                if lyrics and len(lyrics.strip()) > 10:  # Basic validation
                    print(f"DEBUG: Successfully got lyrics from {api['name']}")
                    return lyrics
                else:
                    print(f"DEBUG: {api['name']} returned empty lyrics")
            else:
                print(f"DEBUG: {api['name']} returned {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"DEBUG: {api['name']} timeout")
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: {api['name']} request error: {str(e)}")
        except ValueError as e:  # JSON decode error
            print(f"DEBUG: {api['name']} JSON error: {str(e)}")
        except Exception as e:
            print(f"DEBUG: {api['name']} unexpected error: {str(e)}")
    
    print("DEBUG: All lyrics APIs failed")
    return None

def check_lyrics_content(lyrics):
    """Check lyrics for inappropriate content"""
    if not lyrics:
        return True  # If we can't get lyrics, assume clean
    
    # Convert to lowercase for case-insensitive matching
    lyrics_lower = lyrics.lower()
    
    # List of inappropriate words/phrases (you can expand this)
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
            print(f"DEBUG: Found inappropriate word: {word}")
            return False
    
    return True

# Add this to your app.py

CUSTOM_INAPPROPRIATE_WORDS = [
    # Add church-specific inappropriate words
    'hell', 'damn', 'ass',  # These might be too strict for some churches
    # Add any other words specific to your church's guidelines
]

def check_lyrics_content(lyrics):
    """Check lyrics for inappropriate content with custom words"""
    if not lyrics:
        return True  # If we can't get lyrics, assume clean
    
    # Convert to lowercase for case-insensitive matching
    lyrics_lower = lyrics.lower()
    
    # Combined word list
    inappropriate_words = [
        # Profanity
        'fuck', 'shit', 'bitch', 'asshole', 'damn', 'hell',
        # Sexual content
        'sex', 'naked', 'fucking', 'dick', 'pussy', 'whore',
        # Violence
        'kill', 'murder', 'gun', 'shoot', 'stab',
        # Drugs/alcohol
        'drugs', 'cocaine', 'weed', 'alcohol', 'drunk'
    ] + CUSTOM_INAPPROPRIATE_WORDS
    
    # Check for any inappropriate words
    for word in inappropriate_words:
        if word in lyrics_lower:
            print(f"DEBUG: Found inappropriate word: {word}")
            return False
    
    return True

@app.route('/')
def home():
    return "Welcome to Safety Music Zone! Use /login to authenticate with Spotify."

@app.route('/test-form')
def test_form():
    """Serve the test form"""
    try:
        # Specify UTF-8 encoding to avoid charset issues
        with open('test.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "test.html file not found. Please create the file in your project folder.", 404
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open('test.html', 'r', encoding='latin-1') as file:
            return file.read()

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

    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)

    print("DEBUG: Token exchange status code:", response.status_code)
    token_info = response.json()

    if 'access_token' in token_info:
        session['spotify_token'] = token_info['access_token']
        return 'Spotify authentication successful! You can now use the app.'
    else:
        return jsonify(token_info), 400

# ----------------------
# User Routes
# ----------------------

@app.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    data = search_spotify(query)
    
    # Format the response for easier frontend use
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
        print("DEBUG: request-song called")
        
        # Check authentication first
        token = session.get('spotify_token')
        if not token:
            return jsonify({"error": "Not authenticated with Spotify. Please visit /login first."}), 401

        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        spotify_id = data.get('spotify_id')
        
        if not spotify_id:
            return jsonify({"error": "Spotify ID is required"}), 400

        print(f"DEBUG: Processing spotify_id: {spotify_id}")

        # Check if song exists in our database
        song = Song.query.filter_by(spotify_id=spotify_id).first()
        
        if not song:
            print("DEBUG: Song not in DB, fetching from Spotify...")
            # Fetch song details from Spotify
            track_data = get_track_details(spotify_id)
            if not track_data:
                return jsonify({"error": "Could not fetch song details from Spotify"}), 400

            print(f"DEBUG: Fetched track: {track_data['name']}")
            
            # Create new song record
            song = Song(
                spotify_id=track_data['id'],
                title=track_data['name'],
                artist=track_data['artists'][0]['name'] if track_data['artists'] else 'Unknown',
                album=track_data['album']['name'],
                explicit=track_data['explicit'],
                duration_ms=track_data['duration_ms']
            )
            db.session.add(song)
            db.session.commit()
            print(f"DEBUG: Saved new song: {song.title}")

            # ✅ NEW: Check lyrics after saving song
            print("DEBUG: Checking lyrics...")
            lyrics = get_lyrics(song.artist, song.title)
            is_lyrics_clean = check_lyrics_content(lyrics)
            
            # Save lyrics check result
            lyrics_check = LyricsCheck(
                song_id=song.id,
                lyrics=lyrics[:1000] if lyrics else None,  # Store first 1000 chars
                is_clean=is_lyrics_clean
            )
            db.session.add(lyrics_check)
            db.session.commit()
            print(f"DEBUG: Lyrics check completed - Clean: {is_lyrics_clean}")

        # For now, use a default user
        temp_user = User.query.filter_by(username='guest').first()
        if not temp_user:
            print("DEBUG: Creating guest user")
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

        # ✅ NEW: Check if song should be auto-rejected
        lyrics_check = LyricsCheck.query.filter_by(song_id=song.id).first()
        auto_reject_reasons = []
        
        if song.explicit:
            auto_reject_reasons.append("Explicit content flagged by Spotify")
        
        if lyrics_check and not lyrics_check.is_clean:
            auto_reject_reasons.append("Inappropriate lyrics detected")
        
        if auto_reject_reasons:
            # Auto-reject the song
            new_request = Request(
                user_id=temp_user.id, 
                song_id=song.id, 
                status='Rejected'
            )
            db.session.add(new_request)
            db.session.commit()
            
            return jsonify({
                "error": "Song automatically rejected due to content",
                "reasons": auto_reject_reasons
            }), 400

        # Create request record
        print("DEBUG: Creating new request")
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
            'explicit': song.explicit,
            'lyrics_clean': lyrics_check.is_clean if lyrics_check else True
        })

        print("DEBUG: Request completed successfully")
        return jsonify({
            "message": "Song request submitted successfully!",
            "request_id": new_request.id,
            "song_title": song.title,
            "artist": song.artist,
            "explicit": song.explicit,
            "lyrics_checked": lyrics_check is not None,
            "lyrics_clean": lyrics_check.is_clean if lyrics_check else True
        })

    except Exception as e:
        db.session.rollback()
        print(f"DEBUG: Error in request-song: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return jsonify({"error": f"Failed to submit request: {str(e)}"}), 500

@app.route('/guest')
def guest_interface():
    """Serve the mobile-friendly guest interface"""
    try:
        with open('guest.html', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "guest.html file not found", 404
    
# ----------------------
# DJ Routes
# ----------------------

@app.route('/dj/requests')
def dj_requests():
    """DJ view of all pending requests - WITH LYRICS CHECK"""
    try:
        # Use join to get song and user data in one query
        pending_requests = db.session.query(
            Request, Song, User, LyricsCheck
        ).join(
            Song, Request.song_id == Song.id
        ).join(
            User, Request.user_id == User.id
        ).outerjoin(  # Use outerjoin for optional lyrics check
            LyricsCheck, Song.id == LyricsCheck.song_id
        ).filter(
            Request.status == 'Pending'
        ).all()
        
        requests_data = []
        for req, song, user, lyrics_check in pending_requests:
            requests_data.append({
                'request_id': req.id,
                'song_title': song.title,
                'artist': song.artist,
                'explicit': song.explicit,
                'album': song.album,
                'duration_ms': song.duration_ms,
                'requested_by': user.username,
                # ✅ NEW: Lyrics check info
                'lyrics_checked': lyrics_check is not None,
                'lyrics_clean': lyrics_check.is_clean if lyrics_check else True,
                'has_lyrics': lyrics_check.lyrics is not None if lyrics_check else False
            })
        
        return jsonify(requests_data)
    
    except Exception as e:
        print(f"DEBUG: Error in dj_requests: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
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

@app.route('/dj/lyrics/<int:song_id>')
def get_lyrics_for_song(song_id):
    """Get lyrics for a specific song with robust error handling"""
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

#----------------------
# Debugging Routes
# ----------------------

@app.route('/test-db')
def test_db():
    """Test database connection - FIXED VERSION"""
    try:
        db.create_all()
        user_count = User.query.count()
        song_count = Song.query.count()
        request_count = Request.query.count()
        
        return jsonify({
            "status": "Database working!",
            "users": user_count,
            "songs": song_count,
            "requests": request_count
        })
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/debug-request', methods=['POST'])
def debug_request():
    """Debug endpoint to see what's happening with requests"""
    print("DEBUG: Headers:", dict(request.headers))
    print("DEBUG: JSON data:", request.json)
    print("DEBUG: Form data:", request.form)
    print("DEBUG: Session token exists:", 'spotify_token' in session)
    
    token = session.get('spotify_token')
    if token:
        print("DEBUG: Token (first 20 chars):", token[:20])
    
    return jsonify({
        "headers": dict(request.headers),
        "json_data": request.json,
        "session_has_token": 'spotify_token' in session
    })

@app.before_request
def before_request():
    print(f"DEBUG: {request.method} {request.path} - Session: {dict(session)}")

@app.route('/stats')
def get_stats():
    """Get statistics about songs and lyrics checks"""
    try:
        total_songs = Song.query.count()
        explicit_songs = Song.query.filter_by(explicit=True).count()
        songs_with_lyrics = LyricsCheck.query.filter(LyricsCheck.lyrics.isnot(None)).count()
        unclean_lyrics = LyricsCheck.query.filter_by(is_clean=False).count()
        
        return jsonify({
            "total_songs": total_songs,
            "explicit_songs": explicit_songs,
            "songs_with_lyrics": songs_with_lyrics,
            "unclean_lyrics": unclean_lyrics,
            "safety_effectiveness": f"{(explicit_songs + unclean_lyrics) / total_songs * 100:.1f}%" if total_songs > 0 else "0%"
        })
    
    except Exception as e:
        return jsonify({"error": f"Failed to get stats: {str(e)}"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)