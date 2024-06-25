import spotipy
from spotipy.oauth2 import SpotifyOAuth

def list_user_playlists(sp):
    """ Lists all playlists of the user """
    # Retrieve the current user's playlists from Spotify
    playlists = sp.current_user_playlists()

    # Iterate through each playlist and print its name and ID
    for playlist in playlists['items']:
        print(f"Playlist: {playlist['name']} - {playlist['id']}")

def view_playlist_tracks(sp, playlist_id):
    """ Displays all tracks in a specific playlist """
    # Retrieve all tracks from the specified playlist
    results = sp.playlist_tracks(playlist_id)
    print(f"Tracks in Playlist {playlist_id}:")

    # Iterate through each track and print its name and artist
    for item in results['items']:
        track = item['track']
        print(f"{track['name']} by {track['artists'][0]['name']}")

def create_playlist(sp, name, description=""):
    """ Creates a new playlist for a user """
    # Retrieve the current user's ID from Spotify
    user_id = sp.current_user()['id']

    # Create a new playlist with the provided name and description
    playlist = sp.user_playlist_create(user=user_id, name=name, description=description)
    print(f"Created Playlist: {playlist['name']} - {playlist['id']}")
    return playlist['id']

def add_tracks_to_playlist(sp, playlist_id, track_ids):
    """ Adds tracks to a specific playlist """
    # Add the specified tracks to the specified playlist
    sp.playlist_add_items(playlist_id, track_ids)
    print(f"Added tracks to Playlist {playlist_id}")

def main_menu():
    """ Displays the main menu of the application """
    # Print the main menu options to the user
    print("\nSpotify Playlist Manager")
    print("1 - List my playlists")
    print("2 - View a playlist's tracks")
    print("3 - Create a new playlist")
    print("4 - Add tracks to a playlist")
    print("5 - Exit")

def main():
    """ Main function to handle user interactions """
    # Authentication with Spotify using credentials and required scopes
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id="add own client Id",
        client_secret="add client Secret",
        redirect_uri="http://localhost:8888/callback",
        scope="playlist-read-private playlist-modify-public user-library-read"
    ))

    # Loop to handle user input and provide appropriate functionality
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            list_user_playlists(sp)
        elif choice == '2':
            playlist_id = input("Enter the Playlist ID: ")
            view_playlist_tracks(sp, playlist_id)
        elif choice == '3':
            playlist_name = input("Enter the name of the new playlist: ")
            playlist_description = input("Enter a description for the playlist: ")
            create_playlist(sp, playlist_name, playlist_description)
        elif choice == '4':
            playlist_id = input("Enter the Playlist ID where you want to add tracks: ")
            track_ids = input("Enter track IDs, separated by commas: ").split(',')
            add_tracks_to_playlist(sp, playlist_id, track_ids)
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()
