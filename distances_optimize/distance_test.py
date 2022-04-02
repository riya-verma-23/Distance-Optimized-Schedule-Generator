import unittest
import numpy as np
import distances
from distances import *
import sys
sys.path.insert(0, 'web_scraping')
from course import Course

def test_calculatePerimeterPerDay():
    ans = 3.6
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
    schedules = distances.Distance.generate_schedule_combinations([linkedsection1, linkedsection2])
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
    math241 = Course("spring", "2022", "MATH241")
    cs225 = Course("spring", "2022", "CS225")
    linkedsection1 = [math241.get_section("AL1"),math241.get_section("ADM"), math241.get_section("AL1")] 
    sections = [cs225.get_section("AL2"), math241.get_section("AL1"), math241.get_section("ADM")]
    out = len(distances.Distance.eliminate_sections(sections))
    ans = 3
    np.testing.assert_array_equal(ans, out)

def test_generate_tuples():
    math241 = Course("spring", "2022", "MATH241")
    cs225 = Course("spring", "2022", "CS225")
    section1 = math241.get_section("AL1")
    section2 = cs225.get_section("AL2")
    section3 = math241.get_section("ADM")
    sectionsInDay = [section1, section2, section3]
    out = distances.Distance.generate_tuple_sections(sectionsInDay)
    ans = [(section1, section2), (section1, section3), (section2, section3)]
    np.testing.assert_array_equal(ans, out)

if __name__ == "__main__":
    test_generateScheduleCombinations()
    test_generate_tuples()
    test_calculatePerimeterPerDay()
    print("Everything passed")

