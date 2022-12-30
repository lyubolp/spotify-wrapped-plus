"""
Module containing the Song class.
"""

class Song:
    """
    Contains all the needed information about a song.
    """

    def __init__(self, id, name, year, ranking):
        self.__id = id
        self.__name = name
        self.__year = year
        self.__ranking = ranking

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def name(self) -> str:
        return self.__name

    @property
    def year(self) -> str:
        return self.__year

    @property
    def ranking(self) -> str:
        return self.__ranking

    def calculate_score(self, min_year: int) -> float:
        rank_score = 101 - self.ranking

        # The more recent the playlist, the more weight it has
        # e.g. for the range [2018, 2022]
        # 5 years => 0.20 weight per year

        # 2022 playlist has 1x weight
        # 2021 playlist has 0.80x (4 x 0.20) weight
        # 2020 playlist has 0.60x (3 x 0.20) weight
        # 2019 playlist has 0.40x (2 x 0.20) weight
        # 2018 playlist has 0.20x (1 x 0.20) weight

        weight = 1 / (2022 - min_year + 1)
        year_multiplier = (self.year - min_year + 1) * weight

        return rank_score * year_multiplier

