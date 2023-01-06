import unittest

from abc import ABC, abstractmethod
from src.playlist import Playlist, ClientNotAvailableError
from src.song import Song

class SpotifyStubInterface(ABC):
    @abstractmethod
    def playlist_tracks(self, uri: str):
        pass
    
    @abstractmethod
    def next(self, results: dict):
        pass


class SpotifyStub(SpotifyStubInterface):
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
    def __init__(self, playlist_tracks_to_return, next_to_return):
        self.__playlist_tracks_to_return = playlist_tracks_to_return
        self.__next_to_return = next_to_return

    def playlist_tracks(self, uri: str):
        return self.__playlist_tracks_to_return

    def next(self, results: dict):
        return self.__next_to_return


class TestPlaylist(unittest.TestCase):
    def test_01_test_instance(self):
        # Arrange
        # Act
        # Assert
        pass

    def test_02_test_properties(self):
        # Arrange
        # Act
        # Assert
        pass

    def test_03_test_get_playlist_tracks(self):
        # Arrange
        dummy_year = 2020
        dummy_name = f"dummy_name {dummy_year}"
        dummy_uri = "dummy_uri"

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
        self.assertEqual(tracks, expected_songs, "Returned songs don't match")

    def test_04_get_playlist_tracks_invalid_playlist_name(self):
        # Arrange
        wrong_name = "Spotify Wrapped"
        dummy_uri = "dummy_uri"

        playlist = Playlist(wrong_name, dummy_uri)
        client = SpotifyStub()

        # Act
        with self.assertRaises(ValueError) as ex:
            playlist.get_playlist_tracks(client)
        # Assert
        self.assertIsInstance(ex.exception, ValueError, "The exception is not of the correct type")
        self.assertEqual(str(ex.exception), "The playlist name is not valid", "The exception message is not correct")
    
    def test_05_get_playlist_tracks_none_result(self):
        # Arrange
        dummy_name = "dummy_name"
        dummy_uri = "dummy_uri"
        playlist = Playlist(dummy_name, dummy_uri)

        client = SpotifyStubInvalidResult(None, None)

        # Act
        with self.assertRaises(ClientNotAvailableError) as ex:
            playlist.get_playlist_tracks(client)
        
        # Assert
        self.assertIsInstance(ex.exception, ClientNotAvailableError, "The exception is not of the correct type")
        self.assertEqual(str(ex.exception), "The Spotify client returned an error", "The exception message is not correct")
