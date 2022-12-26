# Shows a user's playlists (need to be authenticated via oauth)
import dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

dotenv.load_dotenv() 

def get_wrapped_playlists(client: spotipy.Spotify):
    playlists = client.user_playlists('lyubolp')

    wrapped_playlists = []

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if 'Top Songs' in playlist['name']:
                wrapped_playlists.append((playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = client.next(playlists)
        else:
            playlists = None

    return wrapped_playlists

def get_playlist_tracks(client: spotipy.Spotify, playlist_uri: str):
    results = client.playlist_tracks(playlist_uri)
    tracks = results['items']
    while results['next']:
        results = client.next(results)
        tracks.extend(results['items'])

    tracks = [(i+1, track['track']['id'], track['track']['name']) for i, track in enumerate(tracks)]
    return tracks

if __name__ == '__main__':
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    wrapped_playlists = get_wrapped_playlists(sp)
    
    all_tracks = [get_playlist_tracks(sp, playlist[0]) for playlist in wrapped_playlists]