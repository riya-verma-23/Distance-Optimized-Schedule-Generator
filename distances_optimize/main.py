import requests
import json
from array import *
import sys
import os
from csv import writer
from csv import reader
import random
import re
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'web_scraping'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'schedule'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'distances_optimize'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'maps'))
from distances import Distance
from section import Section
from course import Course
from schedule_class import Schedule
from mapsAPI import MapsAPI

cs411 = Course("fall", "2022", "CS411")
cs211 = Course("fall", "2022", "CS211")
stat410 = Course("fall", "2022", "STAT410")
# theat101 = Course("fall", "2022", "THEA101") # connecton errors
stat425 = Course("fall", "2022", "CS425")
cs374 = Course("fall", "2022", "CS374")
best_schedule = Distance.best_schedule(courses=[cs411, cs211, stat410, stat425, cs374])
print(len(best_schedule))
#print(distances.Distance.tuple_in_file(("Campus Instructional Facility","Digital Computer Laboratory")))
# print("bs score: ", best_schedule[0].get_score())
# sch = []
# for ls in best_schedule[0].get_linked_sections():
#     ll = []
#     for s in ls:
#         ll.append(s.get_name() + " " + s.get_course() + " " + s.get_location())
#     sch.append(ll)
# print(sch)
# sch1 = []
# worst_schedules = Distance.worst
#         #self.assertEqual(len(worst_schedules), 1)
# print("worst score: ", worst_schedules[0].get_score())
#         #avoids lincoln hall, furthest away
# for ls in worst_schedules[0].get_linked_sections():
#     ll = []
#     for s in ls:
#         ll.append(s.get_name() + " " + s.get_course() + " " + s.get_location())
#     sch1.append(ll)
# print(sch1)
# Distance.print_dictionary()
        