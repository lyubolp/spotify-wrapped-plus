"""
Unit tests for the Playlist class
"""

import unittest

from abc import ABC, abstractmethod
from src.playlist import Playlist, ClientError
from src.song import Song


class SpotifyStubInterface(ABC):
    """
    Interface for the Spotify client stub.
    """
    @abstractmethod
    def playlist_tracks(self, uri: str):
        """
        Returns a list of songs in the playlist.
        """

    @abstractmethod
    def next(self, results: dict):
        """
        Returns the next page of results.
        """


class SpotifyStub(SpotifyStubInterface):
    """
    Stub for the Spotify API.
    """
    def __init__(self):
        self.__songs = [
            {
                'items': [
                    {'track': {'id': '1', 'name': 'song1'}},
                    {'track': {'id': '2', 'name': 'song2'}},
                ],
                'next': 1,
            },
            {
                'items': [
                    {'track': {'id': '3', 'name': 'song3'}},
                    {'track': {'id': '4', 'name': 'song4'}},
                    {'track': {'id': '5', 'name': 'song5'}},
                ],
                'next': None,
            }
        ]
        self.__index = 0

    def playlist_tracks(self, uri: str):
        return self.__songs[self.__index]

    def next(self, results: dict):
        self.__index += 1
        return self.__songs[self.__index]


class SpotifyStubInvalidResult(SpotifyStubInterface):
    """
    Spotify stub that returns an invalid result.
    """
    def __init__(self, playlist_tracks_to_return, next_to_return):
        self.__playlist_tracks_to_return = playlist_tracks_to_return
        self.__next_to_return = next_to_return

    def playlist_tracks(self, uri: str):
        return self.__playlist_tracks_to_return

    def next(self, results: dict):
        return self.__next_to_return


class TestPlaylist(unittest.TestCase):
    """
    Unit tests for the Playlist class.
    """
    def test_01_test_instance(self):
        """
        Asserts that the Playlist class is instantiated correctly.
        """
        # Arrange
        dummy_name = 'dummy_name'
        dummy_uri = 'dummy_uri'

        # Act
        has_raised_exception = False
        try:
            playlist = Playlist(dummy_name, dummy_uri)
        except Exception:
            has_raised_exception = True

        # Assert
        self.assertFalse(has_raised_exception)
        self.assertIsInstance(playlist, Playlist)

    def test_02_test_properties(self):
        """
        Assert that the properties of the Playlist class are working correctly.
        """
        # Arrange
        dummy_name = 'dummy_name'
        dummy_uri = 'dummy_uri'

        # Act
        playlist = Playlist(dummy_name, dummy_uri)

        # Assert
        self.assertEqual(playlist.name, dummy_name, 'The name property is not correct')
        self.assertEqual(playlist.uri, dummy_uri, 'The uri property is not correct')

    def test_03_test_get_playlist_tracks(self):
        """
        Assert that the get_playlist_tracks method is working correctly.
        """
        # Arrange
        dummy_year = 2020
        dummy_name = f'dummy_name {dummy_year}'
        dummy_uri = 'dummy_uri'

        playlist = Playlist(dummy_name, dummy_uri)
        client = SpotifyStub()

        expected_songs = [
            Song('1', 'song1', 2020, 1),
            Song('2', 'song2', 2020, 2),
            Song('3', 'song3', 2020, 3),
            Song('4', 'song4', 2020, 4),
            Song('5', 'song5', 2020, 5)
        ]

        # Act
        tracks = playlist.get_playlist_tracks(client)

        # Assert
        self.assertEqual(tracks, expected_songs, 'Returned songs don\'t match')

    def test_04_get_playlist_tracks_invalid_playlist_name(self):
        """
        Assert that the get_playlist_tracks method raises an exception
            when the playlist name is invalid.
        """
        # Arrange
        wrong_name = 'Spotify Wrapped'
        dummy_uri = 'dummy_uri'

        playlist = Playlist(wrong_name, dummy_uri)
        client = SpotifyStub()

        # Act
        with self.assertRaises(ValueError) as ex:
            playlist.get_playlist_tracks(client)
        # Assert
        self.assertIsInstance(ex.exception, ValueError, 'The exception is not of the correct type')
        self.assertEqual(str(ex.exception), 'Playlist name is not valid',
                         'The exception message is not correct')

    def test_05_get_playlist_tracks_none_result(self):
        """
        Assert that the get_playlist_tracks method raises an exception
        """
        # Arrange
        dummy_name = 'Spotify Wrapped 2019'
        dummy_uri = 'dummy_uri'
        playlist = Playlist(dummy_name, dummy_uri)

        client = SpotifyStubInvalidResult(None, None)

        # Act
        with self.assertRaises(ClientError) as ex:
            playlist.get_playlist_tracks(client)

        # Assert
        self.assertIsInstance(ex.exception, ClientError,
                              'The exception is not of the correct type')
        self.assertEqual(str(ex.exception), 'The Spotify client returned an error',
                         'The exception message is not correct')
