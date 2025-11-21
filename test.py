# First, let me create the complete reorganized project structure with multi-language support

import os
import json
from pathlib import Path

# Create the complete project structure
def create_project_structure():
    project_structure = {
        "backend": {
            "app.py": "",
            "config.py": "",
            "requirements.txt": "",
            "models": {
                "__init__.py": "",
                "database.py": ""
            },
            "routes": {
                "__init__.py": "",
                "auth.py": "",
                "songs.py": "",
                "dj.py": "",
                "lyrics.py": "",
                "language.py": ""
            },
            "services": {
                "__init__.py": "",
                "spotify_service.py": "",
                "lyrics_service.py": "",
                "content_filter.py": ""
            },
            "utils": {
                "__init__.py": "",
                "cache.py": "",
                "helpers.py": ""
            }
        },
        "frontend": {
            "dj-dashboard.html": "",
            "guest-interface.html": "",
            "static": {
                "css": {
                    "styles.css": "",
                    "dj.css": "",
                    "guest.css": ""
                },
                "js": {
                    "app.js": "",
                    "dj.js": "",
                    "guest.js": "",
                    "language.js": ""
                },
                "images": {}
            }
        },
        "docs": {
            "architecture.md": "",
            "api.md": "",
            "setup.md": "",
            "workflow.md": ""
        },
        "data": {
            "lyrics_cache.json": "",
            "database": {}
        },
        "tests": {
            "test_routes.py": "",
            "test_services.py": "",
            "test_content_filter.py": ""
        },
        ".env.example": "",
        ".gitignore": "",
        "README.md": "",
        "requirements.txt": ""
    }
    
    return project_structure

# Create language translations
def create_language_files():
    languages = {
        "en": {
            "app_title": "Safety Music Zone",
            "subtitle": "Request songs for the party! 🎉",
            "total_requests": "Total Requests",
            "active_guests": "Active Guests",
            "approved_songs": "Approved Songs",
            "search_placeholder": "Try \"Happy\"...",
            "search_songs": "Search Songs",
            "request_queue": "Request Queue",
            "most_requested": "Most Requested",
            "no_approved_songs": "No approved songs yet",
            "dj_approval_pending": "DJ will approve songs soon!",
            "no_songs_found": "No songs found. Try a different search.",
            "search_failed": "Search failed. Please try again.",
            "submitting_request": "Submitting your request...",
            "request_success": "Success! \"{song}\" requested!",
            "request_submitted": "Your request for \"{song}\" was submitted!",
            "no_requests": "No requests yet",
            "be_first": "Be the first to request a song!",
            "your_request": "Your Request",
            "approved": "APPROVED",
            "explicit": "EXPLICIT",
            "like": "Like",
            "liked": "Liked",
            "requests": "requests",
            "send_feedback": "💡 Send Feedback & Suggestions",
            "built_with_love": "Built with ❤️ for better church parties",
            "language": "Language",
            "portuguese": "Portuguese",
            "spanish": "Spanish", 
            "english": "English",
            "french": "French"
        },
        "pt": {
            "app_title": "Zona de Música Segura",
            "subtitle": "Solicite músicas para a festa! 🎉",
            "total_requests": "Total de Pedidos",
            "active_guests": "Convidados Ativos",
            "approved_songs": "Músicas Aprovadas",
            "search_placeholder": "Tente \"Feliz\"...",
            "search_songs": "Buscar Músicas",
            "request_queue": "Fila de Pedidos",
            "most_requested": "Mais Pedidas",
            "no_approved_songs": "Nenhuma música aprovada ainda",
            "dj_approval_pending": "O DJ aprovará as músicas em breve!",
            "no_songs_found": "Nenhuma música encontrada. Tente uma busca diferente.",
            "search_failed": "Falha na busca. Por favor, tente novamente.",
            "submitting_request": "Enviando seu pedido...",
            "request_success": "Sucesso! \"{song}\" solicitada!",
            "request_submitted": "Seu pedido para \"{song}\" foi enviado!",
            "no_requests": "Nenhum pedido ainda",
            "be_first": "Seja o primeiro a pedir uma música!",
            "your_request": "Seu Pedido",
            "approved": "APROVADA",
            "explicit": "EXPLÍCITA",
            "like": "Curtir",
            "liked": "Curtiu",
            "requests": "pedidos",
            "send_feedback": "💡 Enviar Feedback & Sugestões",
            "built_with_love": "Feito com ❤️ para festas da igreja melhores",
            "language": "Idioma",
            "portuguese": "Português",
            "spanish": "Espanhol",
            "english": "Inglês",
            "french": "Francês"
        },
        "es": {
            "app_title": "Zona de Música Segura",
            "subtitle": "¡Solicita canciones para la fiesta! 🎉",
            "total_requests": "Solicitudes Totales",
            "active_guests": "Invitados Activos",
            "approved_songs": "Canciones Aprobadas",
            "search_placeholder": "Prueba \"Feliz\"...",
            "search_songs": "Buscar Canciones",
            "request_queue": "Cola de Solicitudes",
            "most_requested": "Más Solicitadas",
            "no_approved_songs": "Todavía no hay canciones aprobadas",
            "dj_approval_pending": "¡El DJ aprobará canciones pronto!",
            "no_songs_found": "No se encontraron canciones. Intenta con una búsqueda diferente.",
            "search_failed": "Error en la búsqueda. Por favor, inténtalo de nuevo.",
            "submitting_request": "Enviando tu solicitud...",
            "request_success": "¡Éxito! \"{song}\" solicitada!",
            "request_submitted": "¡Tu solicitud para \"{song}\" fue enviada!",
            "no_requests": "Todavía no hay solicitudes",
            "be_first": "¡Sé el primero en solicitar una canción!",
            "your_request": "Tu Solicitud",
            "approved": "APROBADA",
            "explicit": "EXPLÍCITA",
            "like": "Me gusta",
            "liked": "Me gusta",
            "requests": "solicitudes",
            "send_feedback": "💡 Enviar Comentarios y Sugerencias",
            "built_with_love": "Hecho con ❤️ para mejores fiestas de iglesia",
            "language": "Idioma",
            "portuguese": "Portugués",
            "spanish": "Español",
            "english": "Inglés", 
            "french": "Francés"
        },
        "fr": {
            "app_title": "Zone de Musique Sécurisée",
            "subtitle": "Demandez des chansons pour la fête ! 🎉",
            "total_requests": "Demandes Totales",
            "active_guests": "Invités Actifs",
            "approved_songs": "Chansons Approuvées",
            "search_placeholder": "Essayez \"Heureux\"...",
            "search_songs": "Rechercher des Chansons",
            "request_queue": "File d'Attente",
            "most_requested": "Plus Demandées",
            "no_approved_songs": "Aucune chanson approuvée pour le moment",
            "dj_approval_pending": "Le DJ approuvera les chansons bientôt !",
            "no_songs_found": "Aucune chanson trouvée. Essayez une recherche différente.",
            "search_failed": "Échec de la recherche. Veuillez réessayer.",
            "submitting_request": "Envoi de votre demande...",
            "request_success": "Succès ! \"{song}\" demandée !",
            "request_submitted": "Votre demande pour \"{song}\" a été envoyée !",
            "no_requests": "Aucune demande pour le moment",
            "be_first": "Soyez le premier à demander une chanson !",
            "your_request": "Votre Demande",
            "approved": "APPROUVÉE",
            "explicit": "EXPLICITE",
            "like": "J'aime",
            "liked": "J'aime",
            "requests": "demandes",
            "send_feedback": "💡 Envoyer des Commentaires et Suggestions",
            "built_with_love": "Fait avec ❤️ pour de meilleures fêtes d'église",
            "language": "Langue",
            "portuguese": "Portugais",
            "spanish": "Espagnol",
            "english": "Anglais",
            "french": "Français"
        }
    }
    
    return languages

# Now let me create all the files with the actual content
def create_backend_files():
    files_content = {}
    
    # Backend app.py
    files_content["backend/app.py"] = '''from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import requests
import os
import urllib.parse
import base64
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/database/church_party.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import models
from models.database import User, Song, Request, LyricsCheck, Vote, SongLike

# Import routes
from routes.songs import songs_bp
from routes.dj import dj_bp
from routes.lyrics import lyrics_bp
from routes.language import language_bp

# Register blueprints
app.register_blueprint(songs_bp)
app.register_blueprint(dj_bp)
app.register_blueprint(lyrics_bp)
app.register_blueprint(language_bp)

# Create all tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
'''

    # Backend models/database.py
    files_content["backend/models/database.py"] = '''from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    requests = db.relationship('Request', backref='song', lazy=True)
    lyrics_check = db.relationship('LyricsCheck', backref='song', lazy=True, uselist=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    votes = db.relationship('Vote', backref='request', lazy=True)

class LyricsCheck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    lyrics = db.Column(db.Text)
    is_clean = db.Column(db.Boolean, nullable=False)
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)

class SongLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)
    guest_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
'''

    # Backend routes/songs.py
    files_content["backend/routes/songs.py"] = '''from flask import Blueprint, request, jsonify, session
from models.database import db, User, Song, Request, LyricsCheck
from services.spotify_service import SpotifyService
from services.lyrics_service import LyricsService
import threading

songs_bp = Blueprint('songs', __name__)
spotify_service = SpotifyService()
lyrics_service = LyricsService()

@songs_bp.route('/search', methods=['GET'])
def search_song():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    data = spotify_service.search_spotify(query)
    
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

@songs_bp.route('/request-song', methods=['POST'])
def request_song():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        spotify_id = data.get('spotify_id')
        guest_id = data.get('guest_id')
        
        if not spotify_id:
            return jsonify({"error": "Spotify ID is required"}), 400

        # Check if song exists in our database
        song = Song.query.filter_by(spotify_id=spotify_id).first()
        
        if not song:
            # Fetch song details from Spotify
            track_data = spotify_service.get_track_details(spotify_id)
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
                with songs_bp.app_context():
                    try:
                        lyrics = lyrics_service.get_lyrics(artist, title)
                        is_clean = lyrics_service.check_lyrics_content(lyrics) if lyrics else True
                        
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
                        
                    except Exception as e:
                        print(f"Async lyrics check failed: {str(e)}")

            thread = threading.Thread(target=check_lyrics_async, args=(song.id, song.artist, song.title))
            thread.daemon = True
            thread.start()

        # Use a default user for guests
        temp_user = User.query.filter_by(username='guest').first()
        if not temp_user:
            temp_user = User(username='guest', password_hash='temp', role='guest')
            db.session.add(temp_user)
            db.session.commit()

        # Check if this song is already pending for this guest
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

        from flask_socketio import emit
        emit('new_request', {
            'request_id': new_request.id,
            'song_title': song.title,
            'artist': song.artist,
            'explicit': song.explicit
        }, broadcast=True)

        return jsonify({
            "message": "Song request submitted successfully!",
            "request_id": new_request.id,
            "song_title": song.title,
            "artist": song.artist,
            "explicit": song.explicit,
            "lyrics_checked": False
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to submit request: {str(e)}"}), 500

@songs_bp.route('/approved-songs')
def approved_songs():
    try:
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
            like_count = SongLike.query.filter_by(song_id=song.id).count()
            request_count = Request.query.filter_by(song_id=song.id, status='Approved').count()
            
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
        
        songs_data.sort(key=lambda x: x['like_count'], reverse=True)
        return jsonify(songs_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@songs_bp.route('/toggle-like', methods=['POST'])
def toggle_like():
    try:
        data = request.json
        song_id = data.get('song_id')
        guest_id = data.get('guest_id')
        
        if not song_id or not guest_id:
            return jsonify({"error": "Song ID and Guest ID required"}), 400
        
        existing_like = SongLike.query.filter_by(song_id=song_id, guest_id=guest_id).first()
        
        if existing_like:
            db.session.delete(existing_like)
            message = "Like removed"
        else:
            new_like = SongLike(song_id=song_id, guest_id=guest_id)
            db.session.add(new_like)
            message = "Like added"
        
        db.session.commit()
        
        from flask_socketio import emit
        emit('like_updated', {
            'song_id': song_id,
            'guest_id': guest_id,
            'action': 'removed' if existing_like else 'added'
        }, broadcast=True)
        
        return jsonify({"message": message})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@songs_bp.route('/popular-songs')
def popular_songs():
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

@songs_bp.route('/guest-stats')
def guest_stats():
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
'''

    # Backend routes/dj.py
    files_content["backend/routes/dj.py"] = '''from flask import Blueprint, request, jsonify
from models.database import db, Request, Song, User, LyricsCheck
from flask_socketio import emit

dj_bp = Blueprint('dj', __name__)

@dj_bp.route('/dj/requests')
def dj_requests():
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
                'image_url': song.image_url,
                'requested_by': user.username,
                'lyrics_checked': lyrics_check is not None,
                'lyrics_clean': lyrics_check.is_clean if lyrics_check else True,
                'has_lyrics': lyrics_check.lyrics is not None if lyrics_check else False
            })
        
        return jsonify(requests_data)
    
    except Exception as e:
        return jsonify({"error": f"Failed to fetch requests: {str(e)}"}), 500

@dj_bp.route('/dj/approve/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    try:
        request_obj = Request.query.get_or_404(request_id)
        request_obj.status = 'Approved'
        db.session.commit()

        emit('request_approved', {
            'request_id': request_obj.id,
            'song_title': request_obj.song.title
        }, broadcast=True)

        return jsonify({"message": "Request approved successfully!"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to approve request: {str(e)}"}), 500

@dj_bp.route('/dj/reject/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    try:
        request_obj = Request.query.get_or_404(request_id)
        request_obj.status = 'Rejected'
        db.session.commit()

        emit('request_rejected', {
            'request_id': request_obj.id,
            'song_title': request_obj.song.title
        }, broadcast=True)

        return jsonify({"message": "Request rejected successfully!"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to reject request: {str(e)}"}), 500
'''

    # Backend routes/lyrics.py
    files_content["backend/routes/lyrics.py"] = '''from flask import Blueprint, request, jsonify
from models.database import db, Song, LyricsCheck
from services.lyrics_service import LyricsService

lyrics_bp = Blueprint('lyrics', __name__)
lyrics_service = LyricsService()

@lyrics_bp.route('/dj/lyrics/<int:song_id>')
def get_lyrics_for_song(song_id):
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
        return jsonify({
            "error": f"Failed to fetch lyrics: {str(e)}",
            "song_id": song_id
        }), 500

@lyrics_bp.route('/dj/refresh-lyrics/<int:song_id>', methods=['POST'])
def refresh_lyrics(song_id):
    try:
        song = Song.query.get(song_id)
        if not song:
            return jsonify({"error": "Song not found"}), 404
        
        lyrics = lyrics_service.get_lyrics(song.artist, song.title)
        is_clean = lyrics_service.check_lyrics_content(lyrics) if lyrics else True
        
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

@lyrics_bp.route('/dj/manual-lyrics/<int:song_id>', methods=['POST'])
def manual_lyrics_input(song_id):
    try:
        data = request.json
        lyrics_text = data.get('lyrics', '')
        
        if not lyrics_text:
            return jsonify({"error": "No lyrics provided"}), 400
        
        lyrics_check = LyricsCheck.query.filter_by(song_id=song_id).first()
        if lyrics_check:
            lyrics_check.lyrics = lyrics_text[:2000]
            lyrics_check.is_clean = lyrics_service.check_lyrics_content(lyrics_text)
        else:
            lyrics_check = LyricsCheck(
                song_id=song_id,
                lyrics=lyrics_text[:2000],
                is_clean=lyrics_service.check_lyrics_content(lyrics_text)
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
'''

    # Backend routes/language.py
    files_content["backend/routes/language.py"] = '''from flask import Blueprint, jsonify
import json
import os

language_bp = Blueprint('language', __name__)

@language_bp.route('/api/languages')
def get_languages():
    """Return available languages"""
    languages_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'languages.json')
    
    try:
        with open(languages_path, 'r', encoding='utf-8') as f:
            languages = json.load(f)
        return jsonify(languages)
    except FileNotFoundError:
        # Return default languages if file doesn't exist
        default_languages = {
            "en": {
                "app_title": "Safety Music Zone",
                "subtitle": "Request songs for the party! 🎉",
                "total_requests": "Total Requests",
                "active_guests": "Active Guests",
                "approved_songs": "Approved Songs",
                "search_placeholder": "Try \"Happy\"...",
                "search_songs": "Search Songs",
                "request_queue": "Request Queue",
                "most_requested": "Most Requested",
                "no_approved_songs": "No approved songs yet",
                "dj_approval_pending": "DJ will approve songs soon!",
                "no_songs_found": "No songs found. Try a different search.",
                "search_failed": "Search failed. Please try again.",
                "submitting_request": "Submitting your request...",
                "request_success": "Success! \"{song}\" requested!",
                "request_submitted": "Your request for \"{song}\" was submitted!",
                "no_requests": "No requests yet",
                "be_first": "Be the first to request a song!",
                "your_request": "Your Request",
                "approved": "APPROVED",
                "explicit": "EXPLICIT",
                "like": "Like",
                "liked": "Liked",
                "requests": "requests",
                "send_feedback": "💡 Send Feedback & Suggestions",
                "built_with_love": "Built with ❤️ for better church parties",
                "language": "Language",
                "portuguese": "Portuguese",
                "spanish": "Spanish", 
                "english": "English",
                "french": "French"
            }
        }
        return jsonify(default_languages)
'''

    # Backend services/spotify_service.py
    files_content["backend/services/spotify_service.py"] = '''import requests
import base64
import urllib.parse
from flask import session
import os

class SpotifyService:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = 'http://127.0.0.1:5000/callback'
        self.api_url = 'https://api.spotify.com/v1'
    
    def get_auth_token(self):
        return session.get('spotify_token')
    
    def search_spotify(self, query):
        token = self.get_auth_token()
        if not token:
            return {'error': 'Not authenticated with Spotify'}

        url = f'{self.api_url}/search'
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": query, "type": "track", "limit": 5}
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    
    def get_track_details(self, track_id):
        token = self.get_auth_token()
        if not token:
            return None

        url = f'{self.api_url}/tracks/{track_id}'
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        return None
'''

    # Backend services/lyrics_service.py
    files_content["backend/services/lyrics_service.py"] = '''import requests
import urllib.parse
import json
import time
import os

class LyricsService:
    def __init__(self):
        self.cache_file = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'lyrics_cache.json')
    
    def load_lyrics_cache(self):
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_lyrics_cache(self, cache):
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    
    def get_cached_lyrics(self, artist, title):
        cache = self.load_lyrics_cache()
        cache_key = f"{artist.lower()}_{title.lower()}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            if time.time() - cached_data.get('timestamp', 0) < 30 * 24 * 60 * 60:
                return cached_data.get('lyrics')
        return None
    
    def cache_lyrics(self, artist, title, lyrics, api_used=None):
        if not lyrics:
            return
            
        cache = self.load_lyrics_cache()
        cache_key = f"{artist.lower()}_{title.lower()}"
        cache[cache_key] = {
            'lyrics': lyrics,
            'timestamp': time.time(),
            'api_used': api_used
        }
        self.save_lyrics_cache(cache)
    
    def get_lyrics(self, artist, title):
        cached_lyrics = self.get_cached_lyrics(artist, title)
        if cached_lyrics:
            return cached_lyrics
        
        clean_artist = urllib.parse.quote(artist)
        clean_title = urllib.parse.quote(title)
        
        apis_priority = [
            {
                'name': 'Lyrics.ovh',
                'url': f"https://api.lyrics.ovh/v1/{clean_artist}/{clean_title}",
                'parser': lambda data: data.get('lyrics', '')
            },
            {
                'name': 'LRCLIB',
                'url': f"https://lrclib.net/api/get?artist_name={clean_artist}&track_name={clean_title}",
                'parser': lambda data: data.get('plainLyrics', '')
            }
        ]
        
        best_lyrics = None
        best_api = None
        
        for api in apis_priority:
            try:
                response = requests.get(api['url'], timeout=8, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200:
                    data = response.json()
                    lyrics = api['parser'](data)
                    
                    if lyrics and len(lyrics.strip()) > 100:
                        best_lyrics = lyrics
                        best_api = api['name']
                        break
                        
            except Exception:
                continue
        
        self.cache_lyrics(artist, title, best_lyrics, best_api)
        return best_lyrics
    
    def check_lyrics_content(self, lyrics):
        if not lyrics:
            return True
        
        lyrics_lower = lyrics.lower()
        
        inappropriate_words = [
            'fuck', 'shit', 'bitch', 'asshole', 'damn', 'hell',
            'sex', 'naked', 'fucking', 'dick', 'pussy', 'whore',
            'kill', 'murder', 'gun', 'shoot', 'stab',
            'drugs', 'cocaine', 'weed', 'alcohol', 'drunk'
        ]
        
        for word in inappropriate_words:
            if word in lyrics_lower:
                return False
        
        return True
'''

    # Backend config.py
    files_content["backend/config.py"] = '''import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///../data/database/church_party.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
'''

    # Backend requirements.txt
    files_content["backend/requirements.txt"] = '''Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-SocketIO==5.3.6
python-dotenv==1.0.0
requests==2.31.0
'''

    return files_content

# Create frontend files with multi-language support
def create_frontend_files():
    files_content = {}
    
    # Frontend guest-interface.html with multi-language support
    files_content["frontend/guest-interface.html"] = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-i18n="app_title">Safety Music Zone - Request Songs</title>
    <link rel="stylesheet" href="static/css/guest.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <i class="fas fa-headphones"></i>
            </div>
            <h1 data-i18n="app_title">Safety Music Zone</h1>
            <p data-i18n="subtitle">Request songs for the party! 🎉</p>
            
            <!-- Language Selector -->
            <div class="language-selector">
                <select id="languageSelect" onchange="changeLanguage(this.value)">
                    <option value="en" data-i18n="english">English</option>
                    <option value="pt" data-i18n="portuguese">Portuguese</option>
                    <option value="es" data-i18n="spanish">Spanish</option>
                    <option value="fr" data-i18n="french">French</option>
                </select>
            </div>
        </div>

        <!-- Party Statistics -->
        <div class="party-stats">
            <div class="stat">
                <div class="stat-number" id="totalRequests">0</div>
                <div class="stat-label" data-i18n="total_requests">Total Requests</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="activeGuests">0</div>
                <div class="stat-label" data-i18n="active_guests">Active Guests</div>
            </div>
        </div>

        <!-- Approved Songs Section -->
        <div class="card">
            <h3 style="margin-bottom: 1rem; text-align: center;">
                <i class="fas fa-check-circle" style="color: var(--success);"></i>
                <span data-i18n="approved_songs">Approved Songs</span>
            </h3>
            <div id="approvedSongs" class="song-list"></div>
        </div>

        <!-- Main Card -->
        <div class="card">
            <!-- Tabs -->
            <div class="tabs">
                <div class="tab active" onclick="switchTab('search')">
                    <i class="fas fa-search"></i> <span data-i18n="search_songs">Search</span>
                </div>
                <div class="tab" onclick="switchTab('queue')">
                    <i class="fas fa-list"></i> <span data-i18n="request_queue">Queue</span>
                </div>
                <div class="tab" onclick="switchTab('popular')">
                    <i class="fas fa-chart-bar"></i> <span data-i18n="most_requested">Popular</span>
                </div>
            </div>

            <!-- Search Tab -->
            <div id="search-tab">
                <div class="search-container">
                    <i class="fas fa-search search-icon"></i>
                    <input type="text" class="search-input" id="searchInput" 
                           data-i18n-placeholder="search_placeholder" placeholder="Try &quot;Happy&quot;..." 
                           onkeypress="handleSearchKeypress(event)">
                </div>
                
                <button class="btn btn-primary btn-full" onclick="searchSongs()" id="searchBtn">
                    <i class="fas fa-search"></i> <span data-i18n="search_songs">Search Songs</span>
                </button>

                <!-- Search Results -->
                <div id="searchResults" class="song-list" style="margin-top: 1rem;"></div>
            </div>

            <!-- Queue Tab -->
            <div id="queue-tab" style="display: none;">
                <h3 style="margin-bottom: 1rem; text-align: center;" data-i18n="request_queue">Request Queue</h3>
                <div id="queueList" class="song-list"></div>
            </div>

            <!-- Popular Tab -->
            <div id="popular-tab" style="display: none;">
                <h3 style="margin-bottom: 1rem; text-align: center;" data-i18n="most_requested">Most Requested</h3>
                <div id="popularList" class="song-list"></div>
            </div>
        </div>

        <!-- Request Status -->
        <div id="requestStatus"></div>

        <!-- Footer -->
        <div class="footer">
            <div style="margin-bottom: 1rem;">
                <p>in development by: <strong>Thales Vaz Sousa</strong></p>
                <div style="margin-top: 0.5rem; display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                    <button onclick="openFeedbackModal()" class="feedback-btn">
                        <i class="fas fa-comment-dots"></i>
                        <span data-i18n="send_feedback">💡 Send Feedback & Suggestions</span>
                    </button>
                </div>
            </div>
            <p style="font-size: 0.8rem; color: var(--gray); margin-top: 1rem;">
                <i class="fas fa-code"></i> <span data-i18n="built_with_love">Built with ❤️ for better church parties</span>
            </p>
        </div>
    </div>

    <!-- Feedback Modal -->
    <div id="feedbackModal" class="modal">
        <div class="modal-content" style="max-width: 500px;">
            <h3><i class="fas fa-comment-dots"></i> <span data-i18n="send_feedback">Send Feedback</span></h3>
            <p style="margin-bottom: 1rem; color: var(--gray);">
                Help improve the DJ app! Choose how you'd like to send feedback:
            </p>
            
            <div style="margin-bottom: 1rem;">
                <label style="display: block; margin-bottom: 0.5rem; font-weight: 600;">Your Feedback:</label>
                <textarea id="feedbackMessage" 
                        style="width: 100%; height: 150px; padding: 12px; border-radius: 8px; background: rgba(30, 27, 46, 0.8); color: var(--light); border: 1px solid rgba(139, 95, 191, 0.3); font-family: 'Segoe UI', system-ui; resize: vertical;"
                        placeholder="🎵 What I like about the app...&#10;🔧 Suggestions for improvement...&#10;🐛 Issues I found...&#10;💡 New features I'd love to see..."></textarea>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 1rem;">
                <button onclick="sendWhatsAppFeedback()" 
                        style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; background: #25D366; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">
                    <i class="fab fa-whatsapp"></i>
                    WhatsApp
                </button>
                
                <button onclick="sendEmailFeedback()" 
                        style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; background: #EA4335; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease;">
                    <i class="fas fa-envelope"></i>
                    Email
                </button>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; gap: 10px;">
                <button onclick="fillQuickTemplate()" 
                        style="display: flex; align-items: center; gap: 0.5rem; background: transparent; border: 1px solid var(--primary); color: var(--primary-light); padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem;">
                    <i class="fas fa-magic"></i>
                    Use Template
                </button>
                
                <button onclick="closeFeedbackModal()" 
                        style="background: var(--gray); color: white; padding: 0.5rem 1rem; border: none; border-radius: 6px; cursor: pointer;">
                    Cancel
                </button>
            </div>
        </div>
    </div>

    <script src="static/js/guest.js"></script>
    <script src="static/js/language.js"></script>
</body>
</html>'''

    # Frontend static/css/guest.css
    files_content["frontend/static/css/guest.css"] = '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #8B5FBF;
    --primary-dark: #6B46C1;
    --primary-light: #9F7AEA;
    --secondary: #C084FC;
    --accent: #E879F9;
    --success: #10B981;
    --danger: #EF4444;
    --warning: #F59E0B;
    --dark: #1E1B2E;
    --darker: #151321;
    --light: #F8FAFC;
    --gray: #94A3B8;
    --card-bg: rgba(30, 27, 46, 0.95);
    --blur-bg: rgba(139, 95, 191, 0.1);
    --shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
}

body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: linear-gradient(135deg, var(--darker) 0%, var(--dark) 50%, var(--primary-dark) 100%);
    min-height: 100vh;
    padding: 20px;
    color: var(--light);
}

.app-container {
    max-width: 400px;
    margin: 0 auto;
    min-height: calc(100vh - 100px);
    display: flex;
    flex-direction: column;
}

.header {
    text-align: center;
    margin-bottom: 1.5rem;
    color: white;
    position: relative;
}

.logo {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    animation: float 3s ease-in-out infinite;
    color: var(--primary-light);
    text-shadow: 0 0 20px rgba(159, 122, 234, 0.5);
}

@keyframes float {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-10px) scale(1.05); }
}

.header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, var(--primary-light), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.header p {
    opacity: 0.9;
    font-size: 0.9rem;
    color: var(--gray);
}

/* Language Selector */
.language-selector {
    position: absolute;
    top: 0;
    right: 0;
}

.language-selector select {
    background: var(--card-bg);
    color: var(--light);
    border: 1px solid rgba(139, 95, 191, 0.3);
    border-radius: 8px;
    padding: 0.5rem;
    font-size: 0.8rem;
    cursor: pointer;
}

.language-selector select:focus {
    outline: none;
    border-color: var(--primary-light);
}

.party-stats {
    display: flex;
    justify-content: space-around;
    margin: 1rem 0;
    padding: 1rem;
    background: var(--blur-bg);
    border-radius: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(139, 95, 191, 0.2);
}

.stat {
    text-align: center;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-light);
    text-shadow: 0 0 10px rgba(159, 122, 234, 0.3);
}

.stat-label {
    font-size: 0.8rem;
    color: var(--gray);
}

.card {
    background: var(--card-bg);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow);
    border: 1px solid rgba(139, 95, 191, 0.3);
}

.search-container {
    position: relative;
    margin-bottom: 1rem;
}

.search-input {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    border: none;
    border-radius: 50px;
    background: rgba(30, 27, 46, 0.8);
    font-size: 1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
    color: var(--light);
    border: 1px solid rgba(139, 95, 191, 0.3);
}

.search-input::placeholder {
    color: var(--gray);
}

.search-input:focus {
    outline: none;
    box-shadow: 0 4px 20px rgba(139, 95, 191, 0.4);
    transform: translateY(-2px);
    border-color: var(--primary-light);
}

.search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--primary-light);
}

.btn {
    padding: 1rem 2rem;
    border: none;
    border-radius: 50px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    box-shadow: 0 4px 15px rgba(139, 95, 191, 0.4);
}

.btn-primary:hover {
    background: linear-gradient(135deg, var(--primary-light), var(--primary));
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 95, 191, 0.6);
}

.btn-success {
    background: var(--success);
    color: white;
}

.btn-full {
    width: 100%;
}

.song-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 300px;
    overflow-y: auto;
}

.song-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: rgba(30, 27, 46, 0.6);
    border-radius: 15px;
    transition: all 0.3s ease;
    cursor: pointer;
    border: 2px solid transparent;
}

.song-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    border-color: var(--primary);
    background: rgba(139, 95, 191, 0.1);
}

.approved-song-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: rgba(30, 27, 46, 0.6);
    border-radius: 15px;
    margin-bottom: 0.75rem;
    transition: all 0.3s ease;
    border: 1px solid rgba(139, 95, 191, 0.2);
}

.approved-song-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    border-color: var(--primary-light);
}

.song-art {
    width: 50px;
    height: 50px;
    border-radius: 10px;
    margin-right: 1rem;
    object-fit: cover;
    border: 2px solid var(--primary);
}

.song-info {
    flex: 1;
}

.song-title {
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: var(--light);
}

.song-artist {
    font-size: 0.85rem;
    color: var(--gray);
}

.requester {
    font-size: 0.7rem;
    color: var(--gray);
    margin-top: 0.25rem;
}

.explicit-badge {
    background: var(--danger);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 0.5rem;
}

.your-request {
    background: var(--primary);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 10px;
    font-size: 0.7rem;
    margin-top: 0.25rem;
    display: inline-block;
}

.like-section {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-left: 1rem;
}

.like-btn {
    background: none;
    border: none;
    color: var(--gray);
    cursor: pointer;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    padding: 0.5rem;
    border-radius: 50%;
}

.like-btn:hover {
    background: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

.like-btn.liked {
    color: var(--danger);
    text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
}

.like-count {
    font-weight: 600;
    color: var(--light);
    min-width: 20px;
    text-align: center;
}

.approved-badge {
    background: linear-gradient(135deg, var(--success), #059669);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.7rem;
    font-weight: 600;
    margin-left: 0.5rem;
}

.request-status {
    text-align: center;
    padding: 1rem;
    border-radius: 15px;
    margin: 1rem 0;
    animation: slideIn 0.5s ease;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.status-success {
    background: rgba(16, 185, 129, 0.1);
    border: 2px solid var(--success);
    color: var(--success);
}

.status-error {
    background: rgba(239, 68, 68, 0.1);
    border: 2px solid var(--danger);
    color: var(--danger);
}

.status-pending {
    background: rgba(245, 158, 11, 0.1);
    border: 2px solid var(--warning);
    color: var(--warning);
}

.tabs {
    display: flex;
    background: rgba(30, 27, 46, 0.8);
    border-radius: 50px;
    padding: 0.25rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(139, 95, 191, 0.3);
}

.tab {
    flex: 1;
    padding: 0.75rem;
    text-align: center;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--gray);
}

.tab.active {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    box-shadow: 0 2px 10px rgba(139, 95, 191, 0.3);
}

.queue-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: rgba(30, 27, 46, 0.6);
    border-radius: 15px;
    margin-bottom: 0.75rem;
    animation: slideIn 0.5s ease;
    border: 1px solid rgba(139, 95, 191, 0.2);
}

.queue-status {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 1rem;
}

.status-approved { background: var(--success); }
.status-pending { background: var(--warning); }
.status-rejected { background: var(--danger); }

.popular-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: rgba(30, 27, 46, 0.6);
    border-radius: 15px;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(139, 95, 191, 0.2);
}

.popular-rank {
    width: 30px;
    height: 30px;
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 1rem;
}

.request-count {
    background: var(--primary);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: bold;
}

.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid var(--primary-light);
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.empty-state {
    text-align: center;
    padding: 2rem;
    color: var(--gray);
}

.empty-state i {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.5;
    color: var(--primary-light);
}

/* Toast notifications */
.toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--card-bg);
    padding: 1rem 1.5rem;
    border-radius: 15px;
    box-shadow: var(--shadow);
    border-left: 4px solid var(--primary);
    max-width: 300px;
    transform: translateX(400px);
    transition: transform 0.3s ease;
    z-index: 1000;
    border: 1px solid rgba(139, 95, 191, 0.3);
}

.toast.show {
    transform: translateX(0);
}

.toast-success { border-left-color: var(--success); }
.toast-error { border-left-color: var(--danger); }
.toast-info { border-left-color: var(--primary); }

.toast-content {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.toast-close {
    background: none;
    border: none;
    color: var(--gray);
    cursor: pointer;
    padding: 0.25rem;
}

/* Footer */
.footer {
    text-align: center;
    margin-top: auto;
    padding: 1rem 0;
    color: var(--gray);
    font-size: 0.8rem;
    border-top: 1px solid rgba(139, 95, 191, 0.2);
}

.footer a {
    color: var(--primary-light);
    text-decoration: none;
}

.footer a:hover {
    color: var(--accent);
}

/* Modal */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    z-index: 1000;
}

.modal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--card-bg);
    padding: 25px;
    border-radius: 15px;
    max-width: 500px;
    width: 90%;
    box-shadow: var(--shadow);
    border: 1px solid rgba(139, 95, 191, 0.3);
}

/* Responsive adjustments */
@media (max-width: 480px) {
    body {
        padding: 15px;
    }
    
    .card {
        padding: 1.25rem;
    }
    
    .header h1 {
        font-size: 1.5rem;
    }
    
    .tab {
        font-size: 0.8rem;
        padding: 0.6rem;
    }
    
    .language-selector {
        position: static;
        margin-top: 1rem;
    }
}

/* Custom scrollbar */
.song-list::-webkit-scrollbar {
    width: 6px;
}

.song-list::-webkit-scrollbar-track {
    background: rgba(30, 27, 46, 0.8);
    border-radius: 10px;
}

.song-list::-webkit-scrollbar-thumb {
    background: var(--primary);
    border-radius: 10px;
}

.song-list::-webkit-scrollbar-thumb:hover {
    background: var(--primary-light);
}

/* Feedback Button Styles */
.feedback-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: var(--primary);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(139, 95, 191, 0.3);
    border: none;
    cursor: pointer;
}

.feedback-btn:hover {
    background: var(--primary-light);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(139, 95, 191, 0.4);
}
'''

    # Frontend static/js/guest.js
    files_content["frontend/static/js/guest.js"] = '''let currentTab = 'search';
let currentSearchResults = [];
let socket = null;
let lastRequestTime = 0;
const REQUEST_COOLDOWN = 10000; // 10 seconds

// Initialize WebSocket connection
function initSocket() {
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    // Listen for new requests from other guests
    socket.on('new_request', (data) => {
        showToast(`${data.song_title} was just requested!`, 'info');
        if (currentTab === 'queue') {
            loadQueue(); // Refresh queue
        }
    });
    
    // Listen for request approvals/rejections
    socket.on('request_approved', (data) => {
        showToast(`🎉 "${data.song_title}" was approved!`, 'success');
        loadApprovedSongs(); // Refresh approved songs
        loadQueue(); // Refresh queue
    });
    
    socket.on('request_rejected', (data) => {
        showToast(`❌ "${data.song_title}" was rejected`, 'error');
        loadQueue(); // Refresh queue
    });

    // Listen for like updates
    socket.on('like_updated', (data) => {
        loadApprovedSongs(); // Refresh approved songs
    });
}

// Generate unique guest ID
function getGuestId() {
    let guestId = localStorage.getItem('guest_id');
    if (!guestId) {
        guestId = 'guest_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('guest_id', guestId);
    }
    return guestId;
}

// Tab switching
function switchTab(tabName) {
    currentTab = tabName;
    
    // Update tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Show/hide content
    document.getElementById('search-tab').style.display = tabName === 'search' ? 'block' : 'none';
    document.getElementById('queue-tab').style.display = tabName === 'queue' ? 'block' : 'none';
    document.getElementById('popular-tab').style.display = tabName === 'popular' ? 'block' : 'none';
    
    if (tabName === 'queue') {
        loadQueue();
    } else if (tabName === 'popular') {
        loadPopularSongs();
    }
}

// Handle Enter key in search
function handleSearchKeypress(event) {
    if (event.key === 'Enter') {
        searchSongs();
    }
}

// Load approved songs with likes
async function loadApprovedSongs() {
    try {
        const guestId = getGuestId();
        const response = await fetch(`/approved-songs?guest_id=${guestId}`);
        const data = await response.json();
        
        const approvedSongsDiv = document.getElementById('approvedSongs');
        
        if (data && data.length > 0) {
            let html = '';
            data.forEach(song => {
                const imageUrl = song.image_url || 'https://via.placeholder.com/50x50/10b981/ffffff?text=✓';
                const isLiked = song.user_liked;
                
                html += `
                    <div class="approved-song-item">
                        <img src="${imageUrl}" alt="${song.title}" class="song-art">
                        <div class="song-info">
                            <div class="song-title">
                                ${song.title}
                                <span class="approved-badge" data-i18n="approved">APPROVED</span>
                            </div>
                            <div class="song-artist">${song.artist}</div>
                            <div class="requester">${song.request_count} <span data-i18n="requests">requests</span></div>
                        </div>
                        <div class="like-section">
                            <button class="like-btn ${isLiked ? 'liked' : ''}" 
                                    onclick="toggleLike(${song.song_id})">
                                <i class="fas fa-heart"></i>
                            </button>
                            <div class="like-count">${song.like_count || 0}</div>
                        </div>
                    </div>
                `;
            });
            approvedSongsDiv.innerHTML = html;
            updateTranslations(); // Update translations for dynamic content
        } else {
            approvedSongsDiv.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-check-circle"></i>
                    <p data-i18n="no_approved_songs">No approved songs yet</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;" data-i18n="dj_approval_pending">DJ will approve songs soon!</p>
                </div>
            `;
            updateTranslations();
        }
    } catch (error) {
        console.error('Failed to load approved songs:', error);
        document.getElementById('approvedSongs').innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load approved songs</p>
            </div>
        `;
    }
}

// Toggle like on approved song
async function toggleLike(songId) {
    try {
        const response = await fetch('/toggle-like', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                song_id: songId,
                guest_id: getGuestId()
            })
        });
        
        const data = await response.json();
        if (response.ok) {
            loadApprovedSongs(); // Refresh the list
        } else {
            showToast('Failed to update like', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
    }
}

// Search songs
async function searchSongs() {
    const query = document.getElementById('searchInput').value.trim();
    const resultsDiv = document.getElementById('searchResults');
    const searchBtn = document.getElementById('searchBtn');
    
    if (!query) {
        showStatus('Please enter a song name to search', 'error');
        return;
    }

    // Show loading state
    searchBtn.innerHTML = '<div class="loading"></div> Searching...';
    searchBtn.disabled = true;
    resultsDiv.innerHTML = '';

    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.tracks && data.tracks.length > 0) {
            currentSearchResults = data.tracks;
            let html = '';
            
            data.tracks.forEach(track => {
                const explicitBadge = track.explicit ? '<span class="explicit-badge" data-i18n="explicit">E</span>' : '';
                const imageUrl = track.image_url || 'https://via.placeholder.com/50x50/6366f1/ffffff?text=🎵';
                
                html += `
                    <div class="song-item" onclick="requestSong('${track.spotify_id}')">
                        <img src="${imageUrl}" alt="${track.title}" class="song-art">
                        <div class="song-info">
                            <div class="song-title">${track.title} ${explicitBadge}</div>
                            <div class="song-artist">${track.artist}</div>
                        </div>
                        <i class="fas fa-plus" style="color: var(--primary);"></i>
                    </div>
                `;
            });
            
            resultsDiv.innerHTML = html;
            updateTranslations(); // Update translations for badges
            showStatus(`Found ${data.tracks.length} songs! Tap to request.`, 'success');
        } else {
            resultsDiv.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-music"></i>
                    <p data-i18n="no_songs_found">No songs found. Try a different search.</p>
                </div>
            `;
            updateTranslations();
        }
    } catch (error) {
        resultsDiv.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p data-i18n="search_failed">Search failed. Please try again.</p>
            </div>
        `;
        updateTranslations();
        showStatus('Search failed. Please check your connection.', 'error');
    } finally {
        // Reset button
        searchBtn.innerHTML = '<i class="fas fa-search"></i> <span data-i18n="search_songs">Search Songs</span>';
        searchBtn.disabled = false;
        updateTranslations();
    }
}

// Request a song
async function requestSong(spotifyId) {
    const now = Date.now();
    if (now - lastRequestTime < REQUEST_COOLDOWN) {
        showToast('Please wait before making another request', 'error');
        return;
    }

    const statusDiv = document.getElementById('requestStatus');
    
    try {
        showStatus(getTranslation('submitting_request'), 'pending');
        lastRequestTime = now;
        
        const response = await fetch('/request-song', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                spotify_id: spotifyId,
                guest_id: getGuestId()
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const successMessage = getTranslation('request_success').replace('{song}', data.song_title);
            const submittedMessage = getTranslation('request_submitted').replace('{song}', data.song_title);
            
            showStatus(`🎉 ${successMessage}`, 'success');
            showToast(submittedMessage, 'success');
            
            // Clear search results
            document.getElementById('searchResults').innerHTML = '';
            document.getElementById('searchInput').value = '';
            
            // Switch to queue tab after a delay
            setTimeout(() => {
                switchTab('queue');
            }, 2000);
        } else {
            showStatus(`❌ ${data.error}`, 'error');
            if (data.reasons) {
                showStatus(`Reasons: ${data.reasons.join(', ')}`, 'error');
            }
        }
    } catch (error) {
        showStatus('❌ Network error. Please try again.', 'error');
    }
}

// Load queue
async function loadQueue() {
    const queueList = document.getElementById('queueList');
    
    try {
        const response = await fetch('/dj/requests');
        const data = await response.json();
        
        if (response.ok && data.length > 0) {
            let html = '';
            
            data.forEach(req => {
                let statusClass = 'status-pending';
                let statusText = 'Pending';
                
                if (req.status === 'Approved') {
                    statusClass = 'status-approved';
                    statusText = 'Approved';
                } else if (req.status === 'Rejected') {
                    statusClass = 'status-rejected';
                    statusText = 'Rejected';
                }
                
                html += `
                    <div class="queue-item">
                        <div class="queue-status ${statusClass}"></div>
                        <div style="flex: 1;">
                            <div class="song-title">${req.song_title}</div>
                            <div class="song-artist">${req.artist}</div>
                            <div class="requester">Requested by: ${getRequesterDisplay(req.requested_by)}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.8rem; color: var(--gray);">${statusText}</div>
                            ${req.requested_by === getGuestId() ? '<div class="your-request" data-i18n="your_request">Your Request</div>' : ''}
                        </div>
                    </div>
                `;
            });
            
            queueList.innerHTML = html;
            updateTranslations(); // Update translations for dynamic content
        } else {
            queueList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p data-i18n="no_requests">No requests yet</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;" data-i18n="be_first">Be the first to request a song!</p>
                </div>
            `;
            updateTranslations();
        }
    } catch (error) {
        queueList.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load queue</p>
            </div>
        `;
    }
}

// Load popular songs
async function loadPopularSongs() {
    try {
        const response = await fetch('/popular-songs');
        const data = await response.json();
        
        let html = '';
        if (data && data.length > 0) {
            data.forEach((song, index) => {
                html += `
                    <div class="popular-item">
                        <div class="popular-rank">${index + 1}</div>
                        <div style="flex: 1;">
                            <div class="song-title">${song.title}</div>
                            <div class="song-artist">${song.artist}</div>
                        </div>
                        <div class="request-count">${song.request_count} <span data-i18n="requests">requests</span></div>
                    </div>
                `;
            });
        } else {
            html = `
                <div class="empty-state">
                    <i class="fas fa-chart-bar"></i>
                    <p data-i18n="no_requests">No popular songs yet</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;" data-i18n="be_first">Requests will appear here</p>
                </div>
            `;
        }
        
        document.getElementById('popularList').innerHTML = html;
        updateTranslations(); // Update translations for dynamic content
    } catch (error) {
        document.getElementById('popularList').innerHTML = `
            <div class="empty-state">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load popular songs</p>
            </div>
        `;
    }
}

// Load party statistics
async function loadPartyStats() {
    try {
        const response = await fetch('/guest-stats');
        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('totalRequests').textContent = data.total_requests || 0;
            document.getElementById('activeGuests').textContent = data.unique_guests || 0;
        }
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Helper function to display requester names
function getRequesterDisplay(requesterId) {
    if (requesterId === getGuestId()) return getTranslation('your_request');
    
    // Simple anonymization - show "Guest 1", "Guest 2", etc.
    const guestNumber = parseInt(requesterId.replace('guest_', ''), 36) % 10 + 1;
    return `Guest ${guestNumber}`;
}

// Show status message
function showStatus(message, type) {
    const statusDiv = document.getElementById('requestStatus');
    statusDiv.className = `request-status status-${type}`;
    statusDiv.innerHTML = message;
    statusDiv.style.display = 'block';
    
    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.style.display = 'none';
        }, 5000);
    }
}

// Toast notification function
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <div style="flex: 1;">${message}</div>
            <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => toast.classList.add('show'), 100);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// Feedback Modal Functions
function openFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'block';
}

function closeFeedbackModal() {
    document.getElementById('feedbackModal').style.display = 'none';
    document.getElementById('feedbackMessage').value = '';
}

function fillQuickTemplate() {
    const template = `🎵 What I like about the app:
• The design is beautiful and modern
• Real-time updates work well
• Lyrics checking is very useful

🔧 Suggestions for improvement:
• 
• 
• 

🐛 Issues I found:
• 
• 
• 

💡 New features I'd love to see:
• 
• 
• 

Overall, great work! 👏`;
    
    document.getElementById('feedbackMessage').value = template;
    showToast('📝 Template loaded! Fill in your specific feedback.', 'info');
}

function sendWhatsAppFeedback() {
    const feedback = document.getElementById('feedbackMessage').value.trim();
    
    if (!feedback) {
        showToast('Please enter your feedback before sending', 'error');
        return;
    }
    
    // Encode the feedback for URL
    const encodedFeedback = encodeURIComponent(`Hi Thales! Feedback about Safety Music Zone DJ app:\\n\\n${feedback}\\n\\n---\\nSent from DJ Dashboard`);
    
    const whatsappNumber = '5548991123011';
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedFeedback}`;
    
    window.open(whatsappUrl, '_blank');
    closeFeedbackModal();
    showToast('✅ Feedback opened in WhatsApp! Thank you! 🙏', 'success');
}

function sendEmailFeedback() {
    const feedback = document.getElementById('feedbackMessage').value.trim();
    
    if (!feedback) {
        showToast('Please enter your feedback before sending', 'error');
        return;
    }
    
    const subject = encodeURIComponent('Safety Music Zone DJ App - Feedback & Suggestions');
    const body = encodeURIComponent(`Hi Thales,\\n\\nHere's my feedback about the Safety Music Zone DJ app:\\n\\n${feedback}\\n\\n---\\nSent from DJ Dashboard`);
    
    const yourEmail = 'thales.vaz.sousa.eng@gmail.com';
    const emailUrl = `mailto:${yourEmail}?subject=${subject}&body=${body}`;
    
    window.location.href = emailUrl;
    closeFeedbackModal();
    showToast('📧 Opening email client... Thank you! 🙏', 'success');
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    initSocket();
    loadPartyStats();
    loadApprovedSongs();
    
    // Update stats and approved songs every 30 seconds
    setInterval(() => {
        loadPartyStats();
        loadApprovedSongs();
    }, 30000);
});'''

    # Frontend static/js/language.js
    files_content["frontend/static/js/language.js"] = '''let currentLanguage = 'en';
let translations = {};

// Load translations from the server
async function loadTranslations(lang) {
    try {
        const response = await fetch('/api/languages');
        const allTranslations = await response.json();
        translations = allTranslations[lang] || allTranslations['en'];
        currentLanguage = lang;
        
        // Save language preference
        localStorage.setItem('preferredLanguage', lang);
        
        updateTranslations();
    } catch (error) {
        console.error('Failed to load translations:', error);
        // Fallback to English
        translations = {};
        updateTranslations();
    }
}

// Update all elements with data-i18n attributes
function updateTranslations() {
    // Update regular elements
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[key]) {
            element.textContent = translations[key];
        }
    });
    
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[key]) {
            element.setAttribute('placeholder', translations[key]);
        }
    });
    
    // Update language selector options
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        Array.from(languageSelect.options).forEach(option => {
            const key = option.getAttribute('data-i18n');
            if (key && translations[key]) {
                option.textContent = translations[key];
            }
        });
    }
    
    // Update page title
    const titleElement = document.querySelector('title[data-i18n]');
    if (titleElement && translations['app_title']) {
        document.title = translations['app_title'] + ' - Request Songs';
    }
}

// Get translation for a specific key
function getTranslation(key) {
    return translations[key] || key;
}

// Change language
function changeLanguage(lang) {
    loadTranslations(lang);
}

// Initialize language on page load
document.addEventListener('DOMContentLoaded', function() {
    // Get preferred language from localStorage or browser language
    const savedLanguage = localStorage.getItem('preferredLanguage');
    const browserLanguage = navigator.language.split('-')[0]; // Get base language code
    
    // Supported languages
    const supportedLanguages = ['en', 'pt', 'es', 'fr'];
    
    // Determine which language to use
    let preferredLang = 'en'; // Default to English
    
    if (savedLanguage && supportedLanguages.includes(savedLanguage)) {
        preferredLang = savedLanguage;
    } else if (supportedLanguages.includes(browserLanguage)) {
        preferredLang = browserLanguage;
    }
    
    // Set the language selector
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = preferredLang;
    }
    
    // Load translations
    loadTranslations(preferredLang);
});'''

    # Create other necessary frontend files
    files_content["frontend/dj-dashboard.html"] = '''<!DOCTYPE html>
<html>
<head>
    <title>Safety Music Zone - DJ Dashboard</title>
    <link rel="stylesheet" href="static/css/dj.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="logo">
                <i class="fas fa-headphones"></i>
            </div>
            <h1>Safety Music Zone - DJ Dashboard</h1>
            <p>Manage song requests and ensure safe content 🎵</p>
        </div>

        <!-- Dashboard Stats -->
        <div class="dashboard-stats">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-music"></i>
                </div>
                <div class="stat-number" id="totalRequestsStat">0</div>
                <div class="stat-label">Total Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="stat-number" id="pendingRequestsStat">0</div>
                <div class="stat-label">Pending Requests</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="stat-number" id="approvedSongsStat">0</div>
                <div class="stat-label">Approved Songs</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-users"></i>
                </div>
                <div class="stat-number" id="activeGuestsStat">0</div>
                <div class="stat-label">Active Guests</div>
            </div>
        </div>

        <!-- DJ Requests Section -->
        <div class="section">
            <h2>
                <i class="fas fa-list"></i> DJ Requests View 
                <span class="real-time-indicator" id="realTimeIndicator">
                    <i class="fas fa-circle"></i> Live Updates
                </span>
            </h2>
            <button onclick="loadRequests()">
                <i class="fas fa-sync-alt"></i> Refresh Requests
            </button>
            <div id="requestsList"></div>
        </div>
    </div>

    <!-- Lyrics Modal -->
    <div id="lyricsModal" class="modal">
        <div class="modal-content" style="max-width: 800px;">
            <h3 id="lyricsTitle"><i class="fas fa-file-alt"></i> Song Lyrics</h3>
            
            <div id="lyricsStatusBar" style="margin-bottom: 15px; padding: 10px; border-radius: 8px; background: rgba(30, 27, 46, 0.6);">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <span id="lyricsSource" style="font-size: 0.9rem; color: var(--gray);"></span>
                    </div>
                    <div id="lyricsActions" style="display: flex; gap: 8px; flex-wrap: wrap;">
                        <button onclick="refreshLyrics(currentSongId)" class="btn-info">
                            <i class="fas fa-sync-alt"></i> Refresh
                        </button>
                    </div>
                </div>
            </div>
            
            <div id="lyricsContent" style="white-space: pre-wrap; font-family: 'Segoe UI', system-ui; line-height: 1.6; max-height: 400px; overflow-y: auto; background: rgba(30, 27, 46, 0.6); padding: 20px; border-radius: 8px; border: 1px solid rgba(139, 95, 191, 0.3);"></div>
            
            <button onclick="closeLyrics()" style="margin-top: 15px; background: var(--gray); color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer;">
                <i class="fas fa-times"></i> Close
            </button>
        </div>
    </div>

    <!-- Footer -->
    <div class="footer">
        <p>in development by: <strong>Thales Vaz Sousa</strong></p>
    </div>

    <script src="static/js/dj.js"></script>
</body>
</html>'''

    # Create configuration and documentation files
    files_content[".env.example"] = '''SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SECRET_KEY=your_flask_secret_key_here
DATABASE_URL=sqlite:///data/database/church_party.db'''

    files_content[".gitignore"] = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.venv
env/
venv/
ENV/

# Database
*.db
*.sqlite3

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/'''

    files_content["README.md"] = '''# 🎵 Safety Music Zone - Church Party DJ App

A real-time web application for managing song requests at church parties with content filtering.

## 🌟 Features

- **Multi-language Support**: Portuguese, Spanish, English, and French
- **Guest Interface**: Mobile-friendly song requests
- **DJ Dashboard**: Real-time request management
- **Content Filtering**: Explicit content and lyrics analysis
- **Spotify Integration**: Song search and metadata
- **Real-time Updates**: WebSocket communication

## 🚀 Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository>
   cd church-party-dj