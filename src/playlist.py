"""
Module containing the Playlist class.
"""
from typing import List

import spotipy

from src.song import Song


class Playlist:
    """
    Contains all the needed information about a playlist.
    """
    def __init__(self, name: str, uri: str) -> None:
        self.__name = name
        self.__uri = uri

    @property
    def name(self) -> str:
        """
        Returns the name of the playlist.
        """
        return self.__name

    @property
    def uri(self) -> str:
        """
        Returns the Spotify URI for the playlist.
        """
        return self.__uri

    def get_playlist_tracks(self, client: spotipy.Spotify) -> List[Song]:
        """
        Returns a list of songs in the playlist.

        :param client: The Spotify client.
        :return: A list of Song objects.
        """
        year = int(self.name.split(' ')[-1])
        results = client.playlist_tracks(self.uri)
        tracks = results['items']
        while results['next']:
            results = client.next(results)
            tracks.extend(results['items'])

        tracks = [Song(track['track']['id'], track['track']['name'], year, i+1)
                  for i, track in enumerate(tracks)]
        return tracks


def get_wrapped_playlists(client: spotipy.Spotify, username: str) -> List[Playlist]:
    """
    Returns a list of all Spotify Wrapped playlists for a user.

    :param client: The Spotify client.
    :param username: The Spotify username.
    :return: A list of Playlist objects.
    """
    playlists = client.user_playlists(username)

    wrapped_playlists = []

    while playlists:
        for playlist in playlists['items']:
            if 'Top Songs' in playlist['name']:
                wrapped_playlists.append(Playlist(playlist['name'], playlist['uri']))
        if playlists['next']:
            playlists = client.next(playlists)
        else:
            playlists = None

    return wrapped_playlists
