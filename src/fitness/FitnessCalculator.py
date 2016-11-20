import numpy as np

from fitness.ScoreCalculatorBase import ScoreCalculatorBase
from mds.MDSBase import MDSBase
from space.DistanceMatrix import DistanceMatrix

class FitnessCalculator:

    def __init__(self, score_calculator: ScoreCalculatorBase,
                 mds: MDSBase, not_gaps_values: list, not_gaps_coordinates: list,
                 size: int):
        self.score_calculator = score_calculator
        self.mds = mds
        self.not_gaps_values = not_gaps_values
        self.not_gaps_coordinates = not_gaps_coordinates
        self.size = size

    def calculate(self, gaps_values: list):

        # compose distance matrix
        distance_matrix = self.compose_distance_matrix(gaps_values)

        # MDS
        chromosome_after_mds = self.mds.run(distance_matrix)
        after_mds = chromosome_after_mds.distance_matrix.get_flatten_upper_triangular_matrix_by_coordinates(self.not_gaps_coordinates)
        score = self.score_calculator.calculate(after_mds, self.not_gaps_values)
        return score


    def compose_distance_matrix(self, gaps_values):
        n = self.size
        d = np.zeros((n, n))

        #fill diagonal
        for i in range(0, n):
            d[i, i] = 0

        gap_cur = 0
        not_gap_cur = 0
        for x in range(0, n):
            for y in range(x + 1, n):
                if [x, y] in self.not_gaps_coordinates:
                    i = self.not_gaps_coordinates.index([x, y])
                    d[x, y] = self.not_gaps_values[i]
                    d[y, x] = self.not_gaps_values[i]
                    not_gap_cur += 1
                else:
                    d[x, y] = gaps_values[gap_cur]
                    d[y, x] = gaps_values[gap_cur]

                    gap_cur += 1

        if gap_cur != len(gaps_values) or not_gap_cur != len(self.not_gaps_values):
            raise ValueError('Did not use all provided values!')

        return DistanceMatrix(d)



