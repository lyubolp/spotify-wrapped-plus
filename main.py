"""
Main driver code for Spotify Wrapped+.
"""
import argparse

from typing import Dict, List, Tuple

from spotipy.oauth2 import SpotifyOAuth

import dotenv
import spotipy

from src.playlist import Playlist, get_wrapped_playlists
from src.song import Song


dotenv.load_dotenv()


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

    all_tracks = [playlist.get_playlist_tracks(sp) for playlist in wrapped_playlists]
    all_tracks = sum(all_tracks, [])

    track_id_to_name = {track.id: track.name for track in all_tracks}
    
    min_year = min([track.year for track in all_tracks])
    all_tracks_with_scores = [(song.id, song.calculate_score(min_year)) for song in all_tracks]
    
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