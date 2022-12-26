import dotenv
import spotipy

from typing import Dict, List, Tuple
from spotipy.oauth2 import SpotifyClientCredentials

dotenv.load_dotenv() 

def get_wrapped_playlists(client: spotipy.Spotify, username: str) -> List[Tuple[str, str]]:
    playlists = client.user_playlists(username)

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

def get_playlist_tracks(client: spotipy.Spotify, playlist_uri: str, playlist_name: str) -> List[Tuple[int, str, str, int]]:
    year = int(playlist_name.split(' ')[-1])
    results = client.playlist_tracks(playlist_uri)
    tracks = results['items']
    while results['next']:
        results = client.next(results)
        tracks.extend(results['items'])

    tracks = [(i+1, track['track']['id'], track['track']['name'], year) for i, track in enumerate(tracks)]
    return tracks

def calculate_score(song: Tuple[int, str, str, int]) -> float:
    song_ranking, song_id, song_name, year = song

    rank_score = 101 - song_ranking
    year_score = 2022 - year

    return rank_score / year_score

def calculate_results(all_tracks_with_scores: List[Tuple[str, float]], years: int, track_id_to_name: Dict[str, str]) -> List[Tuple[str, float]]:
    results = {}
    for track, score in all_tracks_with_scores:
        if track in results:
            results[track] += score
        else:
            results[track] = score

        
    for track in results:
        results[track] /= years

    results = [(track_id_to_name[track], score) for track, score in results.items()]    
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results

def get_all_time_playlist():
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    wrapped_playlists = get_wrapped_playlists(sp, 'lyubolp')

    # TODO: Wrapped 2021 and 2022 are missing.

    # I'll add them manually
    # wrapped_playlists.append(('spotify:playlist:37i9dQZF1EUMDoJuT8yJsl', 'Top Songs 2021'))
    # wrapped_playlists.append(('spotify:playlist:37i9dQZF1F0sijgNaJdgit', 'Top Songs 2022'))
    
    all_tracks = [get_playlist_tracks(sp, playlist_uri, playlist_name) for playlist_uri, playlist_name in wrapped_playlists]
    all_tracks = sum(all_tracks, [])

    track_id_to_name = {track[1]: track[2] for track in all_tracks}
    all_tracks_with_scores = [(song[1], calculate_score(song)) for song in all_tracks]
    
    years = 2022 - min([track[3] for track in all_tracks])
    return calculate_results(all_tracks_with_scores, years, track_id_to_name)

if __name__ == '__main__':
    
    top_tracks = get_all_time_playlist()
    for index, song_data in enumerate(top_tracks[:10]):
        print(f'{index+1}. {song_data[0]} - {song_data[1]:.2f}')