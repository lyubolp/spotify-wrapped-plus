import unittest
from src.song import Song

class TestsSongs(unittest.TestCase):
    def __create_dummy_instance(self, dummy_id="dummy_id", dummy_name="dummy_name", 
                                dummy_year=2020, dummy_ranking=1):
        return Song(dummy_id, dummy_name, dummy_year, dummy_ranking)
    
    def test_01_create_instance(self):
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
        # Arrange
        big_ranking = 102
        dummy_min_year = 2018
        song = self.__create_dummy_instance(dummy_ranking=big_ranking)

        # year_multiplier by default is 0.6, rank_score will be -1
        expected_score = -0.6
        
        # Act
        score = song.calculate_score(dummy_min_year)

        # Assert
        self.assertTrue(score > 0, msg="The calculated score should be positive!")

    def test_05_test_calcualte_score_with_2023_as_min_year(self):
        # Arrange
        # Act
        # Assert
        pass
    def test_06_test_calculate_score_with_2024_as_min_year(self):
        # Arrange
        # Act
        # Assert
        pass
    def test_07_test_calculate_score_with_negative_as_year(self):
        # Arrange
        # Act
        # Assert
        pass
    def test_08_test_calculate_score_with_year_equal_to_min_year_minus_one(self):
        # Arrange
        # Act
        # Assert
        pass