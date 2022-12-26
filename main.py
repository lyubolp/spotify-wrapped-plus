import argparse
import dotenv
import spotipy

from typing import Dict, List, Tuple
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

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

def calculate_score(song: Tuple[int, str, str, int], min_year) -> float:
    song_ranking, song_id, song_name, year = song

    rank_score = 101 - song_ranking

    # The more recent the playlist, the more weight it has
    # e.g. for the range [2018, 2022]
    # 5 years => 0.20 weight per year

    # 2022 playlist has 1x weight
    # 2021 playlist has 0.80x (4 x 0.20) weight
    # 2020 playlist has 0.60x (3 x 0.20) weight
    # 2019 playlist has 0.40x (2 x 0.20) weight
    # 2018 playlist has 0.20x (1 x 0.20) weight

    weight = 1 / (2022 - min_year + 1)
    year_multiplier = (year - min_year + 1) * weight

    return rank_score * year_multiplier

def calculate_results(all_tracks_with_scores: List[Tuple[str, float]], min_year: int, track_id_to_name: Dict[str, str]) -> List[Tuple[str, float]]:
    results = {}
    for track, score in all_tracks_with_scores:
        if track in results:
            results[track] += score
        else:
            results[track] = score

    years = 2022 - min_year + 1
    for track in results:
        results[track] /= years

    results = [(track_id_to_name[track], score) for track, score in results.items()]    
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results

def get_all_time_playlist(username: str):
    scope = 'playlist-read-private'
    auth_manager = SpotifyOAuth(scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    wrapped_playlists = get_wrapped_playlists(sp, username)

    all_tracks = [get_playlist_tracks(sp, playlist_uri, playlist_name) for playlist_uri, playlist_name in wrapped_playlists]
    all_tracks = sum(all_tracks, [])

    track_id_to_name = {track[1]: track[2] for track in all_tracks}
    
    min_year = min([track[3] for track in all_tracks])
    all_tracks_with_scores = [(song[1], calculate_score(song, min_year)) for song in all_tracks]
    
    return calculate_results(all_tracks_with_scores, min_year, track_id_to_name)


def set_up_cli():
    parser = argparse.ArgumentParser(prog = 'Spotify Wrapped+',
                    description = 'Shows an all-time ranking of all Spotify Wrapped playlists',)
    parser.add_argument('-t', '--top', type=int, default=10, help='Number of top songs to show')
    parser.add_argument('-u', '--user', type=str, help='Spotify username', required=True)

    return parser.parse_args()


if __name__ == '__main__':
    parsed_args = set_up_cli()

    username = parsed_args.user
    amount_to_show = parsed_args.top

    top_tracks = get_all_time_playlist(username)

    for index, song_data in enumerate(top_tracks[:amount_to_show]):
        print(f'{index+1}. {song_data[0]} - {song_data[1]:.2f}')