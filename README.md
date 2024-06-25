### README: Spotify Playlist Manager

#### Project Description
The Spotify Playlist Manager is a Python application that interfaces with the Spotify Web API to manage user playlists. This tool allows users to list their playlists, view specific tracks within those playlists, create new playlists, add tracks to playlists, and receive song recommendations. The application utilizes the Spotipy library, which simplifies the use of the Spotify Web API.

#### Features
- **List User Playlists:** Display all playlists associated with the user's Spotify account.
- **View Playlist Tracks:** Show all tracks within a specific playlist.
- **Create a New Playlist:** Allow users to create new playlists with a custom name and description.
- **Add Tracks to a Playlist:** Add specified tracks to a chosen playlist.
- **Get Recommendations for a Playlist:** Generate song recommendations based on the tracks in a specified playlist.

#### Prerequisites
- Python 3.6 or higher
- Spotipy library

#### Setup Instructions
1. **Install Python**: Ensure Python 3.6+ is installed on your machine.
2. **Register a Spotify Application**:
   - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and log in or create an account.
   - Create a new application to get your `client_id` and `client_secret`.
   - Set `http://localhost:8888/callback` as the Redirect URI in your application settings.
3. **Install Spotipy**:
   - Run `pip install spotipy` to install the Spotipy library.
4. **Clone/Download This Repository**:
   - `git clone https://yourrepositoryurl.com/path/to/repo` (Replace with your actual repository URL)

#### Configuration
Update the `client_id`, `client_secret`, and `redirect_uri` in the script with your own Spotify application details.

```python
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="your_client_id_here",
    client_secret="your_client_secret_here",
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-read-private playlist-modify-public user-library-read"
))
```

#### How to Run
1. Open your terminal.
2. Navigate to the directory containing the script.
3. Run the script using Python:
   ```bash
   python spotify_playlist_manager.py
   ```

#### Contribution
This project was developed by Justin Ly. While this is a personal project, suggestions and contributions are welcome. Please feel free to fork this repository and submit pull requests.

Alternatively, you can contact me directly via email at [Justinly0890@gmail.com](mailto:Justinly0890@gmail.com) to discuss more substantial changes or potential collaborations.

---
