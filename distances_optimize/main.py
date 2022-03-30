import requests
import json
from array import *
import distances
import sys
sys.path.insert(0, 'web_scraping')
from course import Course


cs225 = Course("spring", "2022", "CS225")
scan252 = Course("spring", "2022", "SCAN252")
stat410 = Course("spring", "2022", "STAT410")

actual = distances.Distance.calculatePerimeterPerDay(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
print(actual)

# math241 = Course("spring", "2022", "MATH241")
# cs225 = Course("spring", "2022", "CS225")
# schedules = distances.Distance.generateScheduleCombinations([math241, cs225])
# print(schedules)