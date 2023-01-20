"""
Module containing the Song class.
"""


class Song:
    """
    Contains all the needed information about a song.
    """

    def __init__(self, identifier, name, year, ranking):
        self.__identifier = identifier
        self.__name = name
        self.__year = year
        self.__ranking = ranking

    @property
    def identifier(self) -> str:
        """
        Returns the Spotify identifier for the song.
        """
        return self.__identifier

    @property
    def name(self) -> str:
        """
        Returns the name of the song.
        """
        return self.__name

    @property
    def year(self) -> int:
        """
        Returns the year the song was on the playlist.
        """
        return self.__year

    @property
    def ranking(self) -> int:
        """
        Returns the ranking of the song on the playlist.
        """
        return self.__ranking

    def calculate_score(self, min_year: int) -> float:
        """
        Calculates the score of the song based on its ranking and the year it was on the playlist.
        """
        # TODO: Ranking bigger than 100 breaks the code
        rank_score = 101 - self.ranking

        if rank_score <= 0:
            raise ValueError('Ranking must be between 1 and 100')

        # The more recent the playlist, the more weight it has
        # e.g. for the range [2018, 2022]
        # 5 years => 0.20 weight per year

        # 2022 playlist has 1x weight
        # 2021 playlist has 0.80x (4 x 0.20) weight
        # 2020 playlist has 0.60x (3 x 0.20) weight
        # 2019 playlist has 0.40x (2 x 0.20) weight
        # 2018 playlist has 0.20x (1 x 0.20) weight

        # TODO - Replace 2022 with max year
        weight_delimiter = (2022 - min_year + 1)

        if weight_delimiter == 0:
            raise ValueError('Weight must be between 0 and 1')

        weight = 1 / weight_delimiter

        if not 0 <= weight <= 1:
            raise ValueError('Weight must be between 0 and 1')

        year_multiplier = (self.year - min_year + 1) * weight

        if year_multiplier <= 0:
            raise ValueError('Year multiplier must be greater than 0')

        return rank_score * year_multiplier

    def __eq__(self, other):
        return self.identifier == other.identifier
