import unittest
import numpy as np
import distances
from distances import *
import sys
sys.path.insert(0, 'web_scraping')
from course import Course

def test_generateScheduleCombinations_integers():
    ans = [[1, 3, 5], [1, 3, 6], [1, 3, 7], [1, 4, 5], [1, 4, 6], [1, 4, 7], [2, 3, 5], [2, 3, 6], [2, 3, 7], [2, 4, 5], [2, 4, 6], [2, 4, 7]]
    schedules = distances.Distance.generate_schedule_combinations([[1,2], [3,4], [5, 6, 7]])
    np.testing.assert_array_equal(ans, schedules)
    
def test_calculatePerimeterPerDay():
    ans = 4.3
    #example thursday schedule
    cs225 = Course("spring", "2022", "CS225")
    scan252 = Course("spring", "2022", "SCAN252")
    stat410 = Course("spring", "2022", "STAT410")
    actual = distances.Distance.calculate_perimeter_per_day(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
    np.testing.assert_array_equal(ans, actual)

#added a function that checks generateschedule combinations
def test_generateScheduleCombinations():
    math241 = Course("spring", "2022", "MATH241")
    cs225 = Course("spring", "2022", "CS225")
    linkedsection1 = [math241.get_section("AL1"),math241.get_section("ADM")] 
    linkedsection2 = [cs225.get_section("AL2"),cs225.get_section("AYH")]
    schedules = distances.Distance.generate_schedule_combinations([math241, cs225])

#print schedule combination names
    out = []
    for i in range(len(schedules)):
        sch = []
        for j in range(len(schedules[i])):
            sch.append(schedules[i][j].get_name())
        out.append(sch)

    ans = [['AL1', 'AL2'], ['AL1', 'AYH'], ['ADM', 'AL2'], ['ADM', 'AYH']]
    np.testing.assert_array_equal(ans, out)


def test_eliminate_sections():
    ans = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)] 
    eliminate = distances.Distance.generate_tuple_sections([1,2,3,4,5,6])
    np.testing.assert_array_equal(ans, eliminate)
    ans = [(1, 2), (1, 3), (2, 3)]
    eliminate = distances.Distance.generate_tuple_sections([1,1,1,2,3])
    np.testing.assert_array_equal(ans, eliminate)
    ans = [(3, 4), (3, 5), (4, 5)]
    eliminate = distances.Distance.generate_tuple_sections([3,3,4,4,5,5])
    np.testing.assert_array_equal(ans, eliminate)
    distances.Distance.api_calls = {(1,2): 1.0, (1,3):2.0}
    ans = [2,3]
    actual = distances.Distance.eliminate_sections([1,1,1,2,3])
    np.testing.assert_array_equal(ans, actual)
    
if __name__ == "__main__":
    test_generateScheduleCombinations()
    test_eliminate_sections()
    test_calculatePerimeterPerDay()
    test_generateScheduleCombinations_integers()
    print("Everything passed")