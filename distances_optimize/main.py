import requests
import json
from array import *
import distances
import sys
sys.path.insert(0, 'web_scraping')
from course import Course



#very simple 1 schedule generated
cs211 = Course("fall", "2022", "CS211")
cs340 = Course("fall", "2022", "CS340")
schedules = distances.Distance.generate_schedule_combinations([cs211, cs340])
out = []
for i in range(len(schedules)):
    sch = []
    for ls in schedules[i].get_linked_sections():
        ll = []
        for s in ls:
            ll.append(s.get_name() + " " + s.get_course())
        sch.append(ll)
    out.append(sch)
print(out)
print("schdules generated: ", len(schedules))

cs225 = Course("fall", "2022", "CS225")
math241 = Course("fall", "2022", "MATH241")
schedules = distances.Distance.generate_schedule_combinations([cs225, math241])
out = []
for i in range(len(schedules)):
    sch = []
    for ls in schedules[i].get_linked_sections():
        ll = []
        for s in ls:
            ll.append(s.get_name() + s.get_course())
        sch.append(ll)
    out.append(sch)
print(out)
print("schdules generated: ", len(schedules))


#16 expected from schedule generator: generate all possible schedules - NO possible time conflicts (all sections work)
stat410 = Course("fall", "2022", "STAT410")
cs411 = Course("fall", "2022", "CS411")
schedules = distances.Distance.generate_schedule_combinations([stat410, cs411])
for i in range(len(schedules)):
    sch = []
    for ls in schedules[i].get_linked_sections():
        ll = []
        for s in ls:
            ll.append(s.get_name() +  " " + s.get_course())
        sch.append(ll)
    print(sch)
print("schedules generated: ", len(schedules))


#should generate 22 schedules with 2 time conflicts

mus132 = Course("fall", "2022", "MUS132")
mus243 = Course("fall", "2022", "MUS243")

print("mus132")
for l in mus132.get_sections():
    print(l.get_name())
print("mus243")
for l in mus243.get_sections():
    print(l.get_name())

print("mus132 linked sections")
for ll in mus132.get_linked_sections():
    l = []
    for s in ll:
        l.append(s.get_name())
    print(l)


schedules = distances.Distance.generate_schedule_combinations([mus132, mus243])
for i in range(len(schedules)):
    sch = []
    for ls in schedules[i].get_linked_sections():
        ll = []
        for s in ls:
            ll.append(s.get_name() + s.get_course())
        sch.append(ll)
    print(sch)

print("schdules generated: ", len(schedules))



