"""
Module containing the Playlist class.
"""
from typing import List
import re

import spotipy

from src.song import Song


class ClientError(Exception):
    """
    Raised when the Spotify client is not available.
    """


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
        if not self.__is_playlist_name_valid():
            raise ValueError('Playlist name is not valid')

        year = self.__get_year_from_playlist()

        results = client.playlist_tracks(self.uri)

        if results is None:
            raise ClientError('The Spotify client returned an error')

        tracks = results['items']

        while results['next']:
            results = client.next(results)
            tracks.extend(results['items'])

        tracks = [Song(track['track']['id'], track['track']['name'], year, i+1)
                  for i, track in enumerate(tracks)]
        return tracks

    def __is_playlist_name_valid(self) -> bool:
        """
        Returns True if the playlist name is valid, False otherwise.
        """
        year_regex = re.compile(r'\d{4}')
        return year_regex.search(self.name) is not None

    def __get_year_from_playlist(self) -> int:
        """
        Returns the year of the playlist.
        """
        year_regex = re.compile(r'\d{4}')
        year = year_regex.search(self.name)

        if year is None:
            raise ValueError('Playlist name is not valid')

        return int(year.group(0))


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
