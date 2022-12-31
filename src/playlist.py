"""
Module containing the Playlist class.
"""
from typing import List

import spotipy

from src.song import Song


class Playlist:
    def __init__(self, name: str, uri: str) -> None:
        self.__name = name
        self.__uri = uri

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def uri(self) -> str:
        return self.__uri

    def get_playlist_tracks(self, client: spotipy.Spotify) -> List[Song]:
        year = int(self.name.split(' ')[-1])
        results = client.playlist_tracks(self.uri)
        tracks = results['items']
        while results['next']:
            results = client.next(results)
            tracks.extend(results['items'])

        tracks = [Song(track['track']['id'], track['track']['name'], year, i+1) for i, track in enumerate(tracks)]
        return tracks


def get_wrapped_playlists(client: spotipy.Spotify, username: str) -> List[Playlist]:
    playlists = client.user_playlists(username)

    wrapped_playlists = []

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            if 'Top Songs' in playlist['name']:
                wrapped_playlists.append(Playlist(playlist['name'], playlist['uri']))
        if playlists['next']:
            playlists = client.next(playlists)
        else:
            playlists = None

    return wrapped_playlists
