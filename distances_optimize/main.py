import requests
import json
from array import *
import distances
import sys
sys.path.insert(0, 'web_scraping')
from course import Course


# cs225 = Course("spring", "2022", "CS225")
# scan252 = Course("spring", "2022", "SCAN252")
# stat410 = Course("spring", "2022", "STAT410")
# sectionsInDay = [stat410.get_section("1UG"), cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG"), scan252.get_section("C")]
# sectionsInDay = list(dict.fromkeys(sectionsInDay)) #removes repeats
# for s in sectionsInDay:
#     print(s.get_name())

# sectionsInDay = sorted(sectionsInDay, key=lambda x: x.start, reverse=False) #sort based on time
# for s in sectionsInDay:
#     print(s.get_name())

# for t in distances.Distance.generate_tuple_sections(sectionsInDay):
#     print(t[0].get_name(),t[1].get_name())

# distances.Distance.append_to_dict([cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
# actual = distances.Distance.calculatePerimeterPerDay(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
# print(actual)

# math241 = Course("spring", "2022", "MATH241")
# cs225 = Course("spring", "2022", "CS225")
# schedules = distances.Distance.generate_schedule_combinations([math241, cs225])
# print(len(schedules))

# math241 = Course("spring", "2022", "MATH241")
# cs225 = Course("spring", "2022", "CS225")
# linkedsection1 = [math241.get_section("AL1"),math241.get_section("ADM")] 
# linkedsection2 = [cs225.get_section("AL2"),cs225.get_section("AYH")]
# schedules = distances.Distance.generate_schedule_combinations([linkedsection1, linkedsection2])
# out = []
# for i in range(len(schedules)):
#     sch = []
#     for j in range(len(schedules[i])):
#         sch.append(schedules[i][j].get_name())
#     out.append(sch)
# print(out)

math241 = Course("spring", "2022", "MATH241")
cs225 = Course("spring", "2022", "CS225")
section1 = math241.get_section("AL1")
section2 = cs225.get_section("AL2")
section3 = math241.get_section("ADM")
sectionsInDay = [section1, section2, section3]
out = distances.Distance.generate_tuple_sections(sectionsInDay)
