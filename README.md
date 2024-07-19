### README: Spotify Playlist Manager

## Project Description
The Spotify Playlist Manager is a Python application that interfaces with the Spotify Web API to manage user playlists. This tool allows users to list their playlists, view specific tracks within those playlists, create new playlists, add tracks to playlists, and receive song recommendations. The application utilizes the Spotipy library, which simplifies the use of the Spotify Web API.

## Features
- **List User Playlists: Display all playlists associated with the user's Spotify account.
- **View Playlist Tracks: Show all tracks within a specific playlist.
- **Create a New Playlist**: Allow users to create new playlists with a custom name and description.
- **Add Tracks to a Playlist**: Add specified tracks to a chosen playlist.
- **Get Recommendations for a Playlist**: Generate song recommendations based on the tracks in a specified playlist.
- **Fetch Top Tracks of the Month: Retrieve and display the user's top month tracks.
- **Fetch Recently Played Tracks: Retrieve and display the user's most recently played tracks.
- **Search for Tracks: Search for tracks based on a user query.
- **Get Recommended Songs: Generate song recommendations based on the user's top tracks or artists.
- **Light mode & Dark mode for user preferences 

## Prerequisites
- Python 3.6 or higher
- Spotipy library

## Setup Instructions

### Install Python
Ensure Python 3.6+ is installed on your machine.

### Register a Spotify Application
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in or create an account.
2. Create a new application to get your `client_id` and `client_secret`.
3. Set `http://localhost:8888/callback` as the Redirect URI in your application settings.

### Install Spotipy
Run the following command to install the Spotipy library:
```sh
pip install spotipy
```

### Clone/Download This Repository
Clone the repository using the following command:
```sh
git clone https://github.com/Ly-20664/Spotify-Music-Player.git
```

## Configuration
Update the `client_id`, `client_secret`, and `redirect_uri` in the .env file script with your own Spotify application details:
```python
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="your_client_id_here",
    client_secret="your_client_secret_here",
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-read-private playlist-modify-public user-library-read"
))
```

## How to Run
1. Open your terminal.
2. Navigate to the directory containing the script.
3. Run the script using Python:
```sh
python spotify_playlist_manager.py
```

Function Descriptions

1. list_user_playlists(sp)
This function retrieves and prints a list of all playlists associated with the user's Spotify account.

2. view_playlist_tracks(sp, playlist_id)
This function takes a playlist ID as an argument and prints the tracks within that specific playlist.

3. create_new_playlist(sp, user_id, name, description)
This function creates a new playlist with the provided name and description for the user.

4. add_tracks_to_playlist(sp, playlist_id, track_ids)
This function adds the specified track IDs to a chosen playlist.

5. get_playlist_recommendations(sp, seed_tracks, limit=10)
This function generates and prints song recommendations based on the provided track IDs.

6. login()
This function initiates the OAuth flow by redirecting the user to the Spotify login page.

7. callback()
This function handles the redirect from Spotify after the user has logged in and sets the access token in the session.

8. home()
This function retrieves the user's top tracks of the month and most recently played tracks and renders them on the home page.

9. get_token()
This function retrieves the access token from the session and refreshes it if it has expired.

10. list_playlists()
This function retrieves and displays the user's playlists.

11. view_playlist_tracks(playlist_id)
This function retrieves and displays the tracks in a specific playlist and provides recommendations based on the tracks in the playlist.

12. create_playlist_form()
This function renders the form to create a new playlist.

13. create_playlist_action()
This function handles the form submission to create a new playlist.

14. search_results()
This function handles the search query and displays the search results.

15. add_track_to_playlist(track_id)
This function displays the form to add a track to a playlist.

16. add_track_to_playlist_action(track_id)
This function handles the form submission to add a track to a playlist.

17. recommended_songs()
This function retrieves and displays song recommendations based on the user's top tracks or artists.


## Images
Light Mode-
<img width="1440" alt="Screenshot 2024-07-19 at 1 47 29 PM" src="https://github.com/user-attachments/assets/96aedeb1-e5d3-4e7f-b3aa-10eec6b731f9">

Dark Mode-
<img width="1440" alt="Screenshot 2024-07-19 at 1 47 16 PM" src="https://github.com/user-attachments/assets/8de2daee-cabc-4b5e-a134-c9a85508f185">


## Contribution
This project was developed by Justin Ly. While this is a personal project, suggestions and contributions are welcome. Please feel free to fork this repository and submit pull requests.

Alternatively, you can contact me directly via email at Justinly0890@gmail.com to discuss more substantial changes or potential collaborations.
