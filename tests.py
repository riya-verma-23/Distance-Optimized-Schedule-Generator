import unittest
import numpy as np

from distances import *

def test_distance_matrix():
    locations = ["chicago", "hendrick house", "new york city", "san francisco"]
    r = distance_matrix(locations, locations)
    matrix = generateMatrixfromJSON(r, len(locations), len(locations))
    ans = [['1 m', '222 km', '1,270 km', '3,424 km'], ['223 km', '1 m', '1,335 km', '3,460 km'], ['1,271 km', '1,331 km', '1 m', '4,670 km'], ['3,431 km', '3,466 km', '4,677 km', '1 m']]
    np.testing.assert_array_equal(matrix, ans)

def test_generateScheduleCombinations():
    ans = [[1, 3, 5], [1, 3, 6], [1, 3, 7], [1, 4, 5], [1, 4, 6], [1, 4, 7], [2, 3, 5], [2, 3, 6], [2, 3, 7], [2, 4, 5], [2, 4, 6], [2, 4, 7]]
    schedules = generateScheduleCombinations([[1,2], [3,4], [5, 6, 7]])
    np.testing.assert_array_equal(ans, schedules)

if __name__ == "__main__":
    test_distance_matrix()
    test_generateScheduleCombinations()
    print("Yay everything passed")