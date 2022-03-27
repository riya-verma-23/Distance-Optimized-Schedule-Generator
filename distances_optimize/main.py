import requests
import json
from array import *
import distances
import sys
from web_scraping.course import Course
import web_scraping.section


#API KEY
api_key = "INSERT API KEY HERE"

cs225 = Course("spring", "2022", "CS225")
scan252 = Course("spring", "2022", "SCAN252")
stat410 = Course("spring", "2022", "STAT410")

actual = distances.Distance.calculatePerimeterPerDay(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
print(actual)
