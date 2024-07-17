import os
import time
from flask import Flask, redirect, url_for, session, request, render_template, flash
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):
    user = User()
    user.id = user_id
    return user

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-library-read playlist-read-private playlist-modify-public user-read-playback-state user-top-read user-read-recently-played"
    )

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        session["token_info"] = token_info

        user = User()
        user.id = token_info['access_token']
        login_user(user)

    except Exception as e:
        return str(e)
    return redirect(url_for('home'))

@app.route('/home')
@login_required
def home():
    try:
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_data = sp.current_user()

        # Fetch top tracks of the month
        top_tracks = sp.current_user_top_tracks(time_range='short_term', limit=10)['items']
        top_tracks_data = [{'name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'album_cover': track['album']['images'][0]['url'],
                            'preview_url': track['preview_url']} for track in top_tracks]

        # Fetch most recently played tracks
        recently_played = sp.current_user_recently_played(limit=10)['items']
        recently_played_data = [{'name': item['track']['name'],
                                 'artist': item['track']['artists'][0]['name'],
                                 'album_cover': item['track']['album']['images'][0]['url'],
                                 'preview_url': item['track']['preview_url']} for item in recently_played]

        return render_template('home.html', user_data=user_data, top_tracks=top_tracks_data, recently_played=recently_played_data)
    except Exception as e:
        return str(e)

def get_token():
    token_info = session.get("token_info", None)
    if not token_info:
        raise Exception("No token info found in session")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session["token_info"] = token_info
    return token_info

@app.route('/playlists')
@login_required
def list_playlists():
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    playlist_list = [{'name': playlist['name'], 'id': playlist['id'], 'image_url': playlist['images'][0]['url'] if playlist['images'] else None} for playlist in playlists['items']]
    return render_template('playlists.html', playlists=playlist_list)

@app.route('/playlist_tracks/<playlist_id>')
@login_required
def view_playlist_tracks(playlist_id):
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.playlist_tracks(playlist_id)
    playlist_name = sp.playlist(playlist_id)['name']
    tracks = [{'name': item['track']['name'],
               'artist': item['track']['artists'][0]['name'],
               'album_cover': item['track']['album']['images'][0]['url'],
               'id': item['track']['id'],
               'preview_url': item['track']['preview_url']} for item in results['items']]
    
    # Fetch recommendations based on multiple seed tracks from the playlist
    seed_track_ids = [track['id'] for track in tracks[:5]]  # Use up to 5 seed tracks
    if seed_track_ids:
        recommendations = sp.recommendations(seed_tracks=seed_track_ids, limit=10)
        recommended_tracks = [{'name': track['name'],
                               'artist': track['artists'][0]['name'],
                               'album_cover': track['album']['images'][0]['url'],
                               'id': track['id'],
                               'preview_url': track['preview_url']} for track in recommendations['tracks']]
    else:
        recommended_tracks = []
    
    return render_template('playlist_tracks.html', tracks=tracks, playlist_name=playlist_name, recommended_tracks=recommended_tracks)

@app.route('/create_playlist', methods=['GET'])
@login_required
def create_playlist_form():
    return render_template('create_playlist.html')

@app.route('/create_playlist_action', methods=['POST'])
@login_required
def create_playlist_action():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()

    if not name:
        flash('Playlist name cannot be empty.')
        return redirect(url_for('create_playlist_form'))
    
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, description=description)
    return redirect(url_for('list_playlists'))

@app.route('/search_results', methods=['POST'])
@login_required
def search_results():
    query = request.form.get('query', '').strip()
    if not query:
        flash('Please enter a search query.')
        return redirect(url_for('home'))
    
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(q=query, type='track', limit=10)
    tracks = [{'name': item['name'],
               'artist': item['artists'][0]['name'],
               'album_cover': item['album']['images'][0]['url'],
               'preview_url': item['preview_url'],
               'id': item['id']} for item in results['tracks']['items']]
    playlists = sp.current_user_playlists()['items']
    return render_template('search_results.html', tracks=tracks, playlists=playlists)

@app.route('/add_track_to_playlist/<track_id>', methods=['GET'])
@login_required
def add_track_to_playlist(track_id):
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlists = sp.current_user_playlists()
    playlist_list = [{'name': playlist['name'], 'id': playlist['id']} for playlist in playlists['items']]
    return render_template('add_track_to_playlist.html', track_id=track_id, playlists=playlist_list)

@app.route('/add_track_to_playlist_action/<track_id>', methods=['POST'])
@login_required
def add_track_to_playlist_action(track_id):
    token_info = get_token()
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist_id = request.form['playlist_id']
    try:
        playlist_tracks = sp.playlist_tracks(playlist_id)
        track_ids = [item['track']['id'] for item in playlist_tracks['items']]
        if track_id in track_ids:
            flash('Track is already in the playlist.')
        else:
            sp.playlist_add_items(playlist_id, [track_id])
            flash('Track added successfully.')
    except Exception as e:
        flash(f"An error occurred: {e}")
    return redirect(url_for('view_playlist_tracks', playlist_id=playlist_id))

@app.route('/recommended_songs')
@login_required
def recommended_songs():
    try:
        token_info = get_token()
        sp = spotipy.Spotify(auth=token_info['access_token'])
        
        # Get the user's top tracks or artists and use them as seeds for recommendations
        top_tracks = sp.current_user_top_tracks(limit=5)['items']
        seed_track_ids = [track['id'] for track in top_tracks]
        
        if seed_track_ids:
            recommendations = sp.recommendations(seed_tracks=seed_track_ids, limit=10)
            tracks = [{'name': track['name'],
                       'artist': track['artists'][0]['name'],
                       'album_cover': track['album']['images'][0]['url'],
                       'id': track['id'],
                       'preview_url': track['preview_url']} for track in recommendations['tracks']]
        else:
            tracks = []
        
        return render_template('recommended_songs.html', tracks=tracks)
    except Exception as e:
        return str(e)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(port=8888, debug=True)
