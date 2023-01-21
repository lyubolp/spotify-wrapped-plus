"""
Main driver code for Spotify Wrapped+.
"""
import argparse

from typing import Dict, List, Tuple

from spotipy.oauth2 import SpotifyOAuth

import dotenv
import spotipy

from src.playlist import get_wrapped_playlists, Playlist


dotenv.load_dotenv()


# TODO - Refactor this function
def calculate_results(all_tracks_with_scores: List[Tuple[str, float]],
                      min_year: int, track_id_to_name: Dict[str, str]) -> List[Tuple[str, float]]:
    """
    Calculates the final results for the all-time ranking.
    """
    track_to_score: Dict[str, float] = {}
    for track, score in all_tracks_with_scores:
        if track in track_to_score:
            track_to_score[track] += score
        else:
            track_to_score[track] = score

    years = 2022 - min_year + 1
    for track in track_to_score:
        track_to_score[track] /= years

    results = [(track_id_to_name[track], score) for track, score in track_to_score.items()]
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results


def get_all_time_playlist(username: str):
    """
    Retuns a ranking for all songs in all Spotify Wrapped playlists.

    :param username: Spotify username
    :return: List of tuples of the form (song_name, score)
    """
    scope = 'playlist-read-private'
    auth_manager = SpotifyOAuth(scope=scope)
    spotify = spotipy.Spotify(auth_manager=auth_manager)

    wrapped_playlists: List[Playlist] = get_wrapped_playlists(spotify, username)

    all_tracks_per_playlists = [playlist.get_playlist_tracks(spotify)
                                for playlist in wrapped_playlists]

    all_tracks = [track for playlist in all_tracks_per_playlists for track in playlist]

    track_id_to_name = {track.identifier: track.name for track in all_tracks}

    min_year = min(track.year for track in all_tracks)
    all_tracks_with_scores = [(song.identifier, song.calculate_score(min_year))
                              for song in all_tracks if song.ranking <= 100]

    return calculate_results(all_tracks_with_scores, min_year, track_id_to_name)


def set_up_cli():
    """
    Sets up the CLI for the program.
    """
    parser = argparse.ArgumentParser(
        prog='Spotify Wrapped+',
        description='Shows an all-time ranking of all Spotify Wrapped playlists',)
    parser.add_argument('-u', '--user', type=str, help='Spotify username', required=True)

    me_group = parser.add_mutually_exclusive_group(required=True)
    me_group.add_argument('-t', '--top',
                          type=int,
                          help='Number of top songs to show')

    me_group.add_argument('-s', '--song',
                          type=str,
                          help='Song to search for')

    return parser.parse_args()


if __name__ == '__main__':
    parsed_args = set_up_cli()

    user = parsed_args.user
    amount_to_show = parsed_args.top

    top_tracks = get_all_time_playlist(user)

    if parsed_args.song is not None:
        song_name = parsed_args.song
        for index, song_data in enumerate(top_tracks):
            if song_data[0] == song_name:
                print(f'{song_data[0]}, ranked #{index+1}, score: {song_data[1]:.2f}')
                break
    elif parsed_args.top is not None:
        for index, song_data in enumerate(top_tracks[:amount_to_show]):
            print(f'{index+1}. {song_data[0]} - {song_data[1]:.2f}')
