"""
Module containing the unittests for the Song class.
"""
import unittest
from src.song import Song


class TestsSongs(unittest.TestCase):
    """
    Class containing the unittests for the Song class.
    """
    def __create_dummy_instance(self, dummy_id="dummy_id", dummy_name="dummy_name",
                                dummy_year=2020, dummy_ranking=1):
        return Song(dummy_id, dummy_name, dummy_year, dummy_ranking)

    def test_01_create_instance(self):
        """
        Verify that the Song class can be instantiated.
        """
        # Arrange
        dummy_id = "dummy_id"
        dummy_name = "dummy_name"
        dummy_year = 2020
        dummy_ranking = 1

        # Act
        has_raised_exception = False
        try:
            song = Song(dummy_id, dummy_name, dummy_year, dummy_ranking)
        except Exception:
            has_raised_exception = True

        # Assert
        self.assertFalse(has_raised_exception)
        self.assertIsInstance(song, Song)

    def test_02_test_properties(self):
        """
        Verify that the properties of the Song class are set correctly.
        """
        # Arrange
        expected_id = "dummy_id"
        expected_name = "dummy_name"
        expected_year = 2020
        expected_ranking = 1

        # Act
        song = Song(expected_id, expected_name, expected_year, expected_ranking)

        # Assert
        self.assertEqual(song.identifier, expected_id)
        self.assertEqual(song.name, expected_name)
        self.assertEqual(song.year, expected_year)
        self.assertEqual(song.ranking, expected_ranking)

    def test_03_test_calculate_score(self):
        """
        Verify that the calculate_score method returns the correct score.
        """
        # Arrange
        dummy_min_year = 2018
        song = self.__create_dummy_instance()

        # weight: 0.2
        # year_multiplier: 3 * 0.2 = 0.6
        # rank_score: 101 - 1 = 100
        # expected_score: 0.6 * 100 = 60
        expected_score = 60

        # Act
        score = song.calculate_score(dummy_min_year)

        # Assert
        self.assertAlmostEqual(score, expected_score, places=6, msg="The score is not correct!")

    def test_04_test_calculate_score_with_big_ranking(self):
        """
        Assert that the calculate_score method raises a ValueError when the ranking is too big.
        """
        # Arrange
        big_ranking = 102
        dummy_min_year = 2018
        song = self.__create_dummy_instance(dummy_ranking=big_ranking)

        # Act
        with self.assertRaises(ValueError) as ex:
            song.calculate_score(dummy_min_year)

        # Assert
        self.assertEqual(str(ex.exception), "Ranking must be between 1 and 100",
                         msg="The error message is not correct!")

    def test_05_test_calcualte_score_with_2023_as_min_year(self):
        """
        Assert that the calculate_score method raises a ValueError when min year is 2023.
        """
        # Arrange
        dummy_min_year = 2023
        song = self.__create_dummy_instance()

        # Act
        with self.assertRaises(ValueError) as ex:
            song.calculate_score(dummy_min_year)
        # Assert
        self.assertEqual(str(ex.exception), "Weight must be between 0 and 1",
                         msg="The error message is not correct!")

    def test_06_test_calculate_score_with_2024_as_min_year(self):
        """
        Assert that the calculate_score method raises a ValueError when weight is negative.
        """
        # Arrange
        dummy_min_year = 2024
        song = self.__create_dummy_instance()

        # Act
        with self.assertRaises(ValueError) as ex:
            song.calculate_score(dummy_min_year)
        # Assert
        self.assertEqual(str(ex.exception), "Weight must be between 0 and 1",
                         msg="The error message is not correct!")

    def test_07_test_calculate_score_with_negative_as_year(self):
        """
        Assert that the calculate_score method raises a ValueError when year is negative.
        """
        # Arrange
        dummy_year = -1
        song = self.__create_dummy_instance(dummy_year=dummy_year)

        # Act
        with self.assertRaises(ValueError) as ex:
            song.calculate_score(2018)

        # Assert
        self.assertEqual(str(ex.exception), "Year multiplier must be greater than 0",
                         msg="The error message is not correct!")

    def test_08_test_calculate_score_with_year_equal_to_min_year_minus_one(self):
        """
        Assert that the calculate_score method raises a ValueError
            when year is equal to min year - 1.
        """
        # Arrange
        dummy_year = 2017
        dummy_min_year = 2018
        song = self.__create_dummy_instance(dummy_year=dummy_year)

        # Act
        with self.assertRaises(ValueError) as ex:
            song.calculate_score(dummy_min_year)

        # Assert
        self.assertEqual(str(ex.exception), "Year multiplier must be greater than 0",
                         msg="The error message is not correct!")
