import unittest
import numpy as np
import distances
from distances import *
import sys
import os
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'web_scraping'))
from course import Course

# def test_eliminate_sections():
#     math241 = Course("spring", "2022", "MATH241")
#     cs225 = Course("spring", "2022", "CS225")
#     linkedsection1 = [math241.get_section("AL1"),math241.get_section("ADM"), math241.get_section("AL1")] 
#     sections = [cs225.get_section("AL2"), math241.get_section("AL1"), math241.get_section("ADM")]
#     out = len(distances.Distance.eliminate_sections(sections))
#     ans = 3
#     np.testing.assert_array_equal(ans, out)

class TestGenerateSchedules(unittest.TestCase):

    def test_generate_tuples(self):
        math241 = Course("spring", "2022", "MATH241")
        cs225 = Course("spring", "2022", "CS225")
        section1 = math241.get_section("AL1")
        section2 = cs225.get_section("AL2")
        section3 = math241.get_section("ADM")
        sectionsInDay = [section1, section2, section3]
        out = distances.Distance.generate_tuple_sections(sectionsInDay)
        ans = [(section1, section2), (section1, section3), (section2, section3)]
        np.testing.assert_array_equal(ans, out)
        
    # def test_calculatePerimeterPerDay():
    #     ans = 3.6
    #     #example thursday schedule
    #     cs225 = Course("spring", "2022", "CS225")
    #     scan252 = Course("spring", "2022", "SCAN252")
    #     stat410 = Course("spring", "2022", "STAT410")
    #     actual = distances.Distance.calculate_perimeter_per_day(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
    #     np.testing.assert_array_equal(ans, actual)


    def test_generate_schedules_simple_no_tc(self):
        #very simple 1 schedule generated - 0 time conflicts
        cs211 = Course("fall", "2022", "CS211")
        cs340 = Course("fall", "2022", "CS340")
        schedules = distances.Distance.generate_schedule_combinations([cs211, cs340])
        self.assertEqual(len(schedules), 1)
        self.assertEqual(distances.Distance.count_tc([cs211, cs340]),0)

    def test_generate_schedules_med_no_tc(self):
        #very med sized schedule generated - 16 generated from Self Service UIUC Schedule Generator - 0 time conflicts
        stat410 = Course("fall", "2022", "STAT410")
        cs411 = Course("fall", "2022", "CS411")
        schedules = distances.Distance.generate_schedule_combinations([stat410, cs411])
        self.assertEqual(len(schedules), 16)
        self.assertEqual(distances.Distance.count_tc([stat410, cs411]), 0)

    def test_generate_schedules_simple_tc(self):
        #should generate 22 schedules with 2 time conflicts
        mus132 = Course("fall", "2022", "MUS132")
        mus243 = Course("fall", "2022", "MUS243")
        schedules = distances.Distance.generate_schedule_combinations([mus132, mus243])
        self.assertEqual(len(schedules), 22)
        self.assertEqual(distances.Distance.count_tc([mus132, mus243]), 2)

    def test_generate_schedules_complex(self):
        #My Fall 2022 Schedule - should generate 22 schedules and 2*1*16*1 = 32 possible linked sections so 32 - 22 = 10 time conflicts
        cs211 = Course("fall", "2022", "CS211")
        cs374 = Course("fall", "2022", "CS374")
        cs411 = Course("fall", "2022", "CS411")
        cs340 = Course("fall", "2022", "CS340")
        schedules = distances.Distance.generate_schedule_combinations([cs211, cs374, cs411, cs340])
        self.assertEqual(len(schedules), 22)
        self.assertEqual(distances.Distance.count_tc([cs211, cs374, cs411, cs340]), 10)

    def test_generate_schedules_large_tc(self):
        ##what number?
        cs225 = Course("fall", "2022", "CS225")
        math241 = Course("fall", "2022", "MATH241")
        schedules = distances.Distance.generate_schedule_combinations([cs225, math241])
        # self.assertEqual(len(schedules), 1300)
        # self.assertEqual(distances.Distance.count_tc(schedules), 2)

    def test_best_schedule_large(self):
        #16 api calls
        cs225 = Course("fall", "2022", "CS225")
        math241 = Course("fall", "2022", "MATH241")
        schedules = distances.Distance.generate_schedule_combinations([cs225, math241])
        #test number of schdule and time conflicts later
        print(len(schedules))
        print(distances.Distance.count_tc(courses=[cs225, math241]))
        best_schedule = distances.Distance.best_schedule(courses=[cs225, math241])
        for s in best_schedule:
            sch = []
            print("best score: ", s.get_score())
            for ls in s.get_linked_sections():
                ll = []
                for s in ls:
                    ll.append(s.get_name() + " " + s.get_course())
                sch.append(ll)
            print(sch)
            break
        distances.Distance.print_dictionary()
        print("api call count: ", distances.Distance.count_api_calls)
        distances.Distance.count_api_calls = 0 #reset api call count

    def test_best_schedule_large_two(self):
        cs173 = Course("fall", "2022", "CS173")
        cs128 = Course("fall", "2022", "CS128")
        cs411 = Course("fall", "2022", "CS411")
        schedules = distances.Distance.generate_schedule_combinations([cs173, cs128, cs411])
        #test number of schdule and time conflicts later
        print(len(schedules))
        print(distances.Distance.count_tc(courses=[cs173, cs128, cs411]))
        best_schedule = distances.Distance.best_schedule(courses=[cs173, cs128, cs411])
        for s in best_schedule:
            sch = []
            print("best score: ", s.get_score())
            for ls in s.get_linked_sections():
                ll = []
                for s in ls:
                    ll.append(s.get_name() + " " + s.get_course())
                sch.append(ll)
            print(sch)
            break
        distances.Distance.print_dictionary()
        print("api call count: ", distances.Distance.count_api_calls)
        distances.Distance.count_api_calls = 0 #reset api call count

    def test_best_schedule_simple(self):
        cs512 = Course("fall", "2022", "CS512")
        cs340 = Course("fall", "2022", "CS340")
        cs411 = Course("fall", "2022", "CS411")
        cs420 = Course("fall", "2022", "CS420")
        cs173 = Course("fall", "2022", "CS173")
        schedules = distances.Distance.generate_schedule_combinations([cs512, cs340, cs411, cs420, cs173])
        self.assertEqual(len(schedules), 16)
        self.assertEqual(distances.Distance.count_tc([cs512, cs340, cs411, cs420]),0)
        best_schedule = distances.Distance.best_schedule(courses=[cs512, cs340, cs411, cs420, cs173])
        for s in best_schedule:
            sch = []
            print("best score: ", s.get_score())
            for ls in s.get_linked_sections():
                ll = []
                for s in ls:
                    ll.append(s.get_name() + " " + s.get_course())
                sch.append(ll)
            print(sch)
        distances.Distance.print_dictionary()
        print("api call count: ", distances.Distance.count_api_calls)
        distances.Distance.count_api_calls = 0 #reset api call count

if __name__ == "__main__":
    unittest.main()

