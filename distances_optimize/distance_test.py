import unittest
import numpy as np
import distances
from distances import *
import sys
from csv import writer
sys.path.insert(0, 'web_scraping')
from course import Course

class TestGenerateSchedules(unittest.TestCase):
    def test_calc_perim_simple(self):#pass
        ans = 1.4
        #example thursday schedule
        scan252 = Course("spring", "2022", "SCAN252") #c david
        stat410 = Course("spring", "2022", "STAT410") #iug lincoln
        cs225 = Course("spring", "2022", "CS225") #ayh siebel
        actual = distances.Distance.calculate_perimeter_per_day(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
        np.testing.assert_array_equal(ans, actual)

    def test_calc_perim_simple_2(self):#pass
        ans = 1.2
        cs128 = Course("spring", "2022", "CS128") #DBA #cif
        math241 = Course("spring", "2022", "MATH241") #AL2 alt
        rhet105 = Course("spring", "2022", "RHET105") #E5 english
        cs173 = Course("spring", "2022", "CS173") #BDF cif
        actual = distances.Distance.calculate_perimeter_per_day(sectionsinDay=[cs128.get_section("DBA"), math241.get_section("AL2"), rhet105.get_section("E5"), cs173.get_section("BDF")])
        self.assertAlmostEqual(ans, actual, 1)
    
    def test_calc_perim_large(self):#pass
        ans = 5.4
        cs233 = Course("spring", "2022", "CS233") #alp cif 8 am
        math241 = Course("spring", "2022", "MATH241") #adb 9 am alt
        cs225 = Course("spring", "2022", "CS225") #al1 11 am - 12 ece
        cs222 = Course("spring", "2022", "CS222") #sdl siebel 12-1pm
        kin103 = Course("spring", "2022", "KIN103") #d1 gym 1-2 pm recreac center
        econ102 = Course("spring", "2022", "ECON102") #al2 2-3 pm lincoln hall
        cs107 = Course("spring", "2022", "CS107") #ayc 3:30-5 pm cif
        actual = distances.Distance.calculate_perimeter_per_day(sectionsinDay=[cs233.get_section("ALP"), math241.get_section("ADB"), cs225.get_section("AL1"), cs222.get_section("SDL"), kin103.get_section("D1"), econ102.get_section("AL2"), cs107.get_section("AYC")])
        self.assertAlmostEqual(ans, actual, 1)
        print("score:", actual)
    
    def test_calc_perim_repetitive(self):#pass
        ans = 1.4
        cs225 = Course("spring", "2022", "CS225") #ayu 9 - 11 am siebel, ayb 3-5 pm siebel
        math241 = Course("spring", "2022", "MATH241") #al2 11 am alt
        cs222 = Course("spring", "2022", "CS222") #sdl siebel 12-1pm
        #self.assertEqual(Distance.api_calls, 1)
        actual = distances.Distance.calculate_perimeter_per_day(sectionsinDay=[cs225.get_section("AYU"), math241.get_section("AL2"), cs222.get_section("SDL"), cs225.get_section("AYB")])
        self.assertAlmostEqual(ans, actual, 1)
        print("score:", actual)
    
    def test_generate_schedules_simple_no_tc(self): #pass
        #very simple 1 schedule generated - 0 time conflicts
        cs211 = Course("fall", "2022", "CS211")
        cs340 = Course("fall", "2022", "CS340")
        schedules = distances.Distance.generate_schedule_combinations([cs211, cs340])
        self.assertEqual(len(schedules), 1)
        self.assertEqual(distances.Distance.count_tc([cs211, cs340]),0)

    def test_generate_schedules_large(self):#pass
        #verify time conflict
        stat107 = Course("fall", "2022", "STAT107")
        las122 = Course("fall", "2022", "LAS122")
        cs124 = Course("fall", "2022", "CS124")
        hindi201 = Course("fall", "2022", "HNDI201")
        schedules = distances.Distance.generate_schedule_combinations([stat107, las122, cs124, hindi201])
        self.assertEqual(len(schedules), 1000)
        self.assertEqual(distances.Distance.count_tc([stat107, las122, cs124, hindi201]), 10040)

    def test_generate_schedules_med_no_tc(self):
        #very med sized schedule generated - 16 generated from Self Service UIUC Schedule Generator - 0 time conflicts
        stat410 = Course("fall", "2022", "STAT410")
        cs411 = Course("fall", "2022", "CS411")
        schedules = distances.Distance.generate_schedule_combinations([stat410, cs411])
        self.assertEqual(len(schedules), 16)
        self.assertEqual(distances.Distance.count_tc([stat410, cs411]), 0)

    def test_best_schedule_large(self):#pass
        me320 = Course("fall", "2022", "ME320")
        ece205 = Course("fall", "2022", "ECE205")
        me290 = Course("fall", "2022", "ME290")
        me270 = Course("fall", "2022", "ME270")
        tam212 = Course("fall", "2022", "TAM212")
        tam251 = Course("fall", "2022", "TAM251")
        kin103 = Course("fall", "2022", "KIN103")
        schedules = distances.Distance.generate_schedule_combinations([me320, ece205, me290, me270, tam212, tam251, kin103])
        self.assertEqual(len(schedules), 1000) #1000+ schedules
        best_schedule = distances.Distance.best_schedule(courses=[me320, ece205, me290, me270, tam212, tam251, kin103])
        #self.assertEqual(len(best_schedule), 2)
        self.assertEqual(10.4, best_schedule[0].get_score())
        print("best score: ", best_schedule[0].get_score())
        sch = []
        for ls in best_schedule[0].get_linked_sections():
            ll = []
            for s in ls:
                ll.append(s.get_name() + " " + s.get_course() + " " + s.get_location())
            sch.append(ll)
        print(sch)
        sch1 = []
        worst_schedules = distances.Distance.worst
        #self.assertEqual(len(worst_schedules), 1)
        print("worst score: ", worst_schedules[0].get_score())
        #avoids lincoln hall, furthest away
        for ls in worst_schedules[0].get_linked_sections():
            ll = []
            for s in ls:
                ll.append(s.get_name() + " " + s.get_course() + " " + s.get_location())
            sch1.append(ll)
        print(sch1)
        distances.Distance.print_dictionary()
        #self.assertEqual(9, len(Distance.api_calls))
        

    def test_generate_schedules_simple_tc(self):#pass
        #should generate 22 schedules with 2 time conflicts
        mus132 = Course("fall", "2022", "MUS132")
        mus243 = Course("fall", "2022", "MUS243")
        schedules = distances.Distance.generate_schedule_combinations([mus132, mus243])
        self.assertEqual(len(schedules), 22)
        self.assertEqual(distances.Distance.count_tc([mus132, mus243]), 2)

    def test_generate_schedules_complex(self): #pass
        #My Fall 2022 Schedule - should generate 22 schedules and 2*1*16*1 = 32 possible linked sections so 32 - 22 = 10 time conflicts
        cs211 = Course("fall", "2022", "CS211")
        cs374 = Course("fall", "2022", "CS374")
        cs411 = Course("fall", "2022", "CS411")
        cs340 = Course("fall", "2022", "CS340")
        schedules = distances.Distance.generate_schedule_combinations([cs211, cs374, cs411, cs340])
        self.assertEqual(len(schedules), 22)
        self.assertEqual(distances.Distance.count_tc([cs211, cs374, cs411, cs340]), 10)

    def test_generate_schedules_large_tc(self):
        cs225 = Course("fall", "2022", "CS225")
        math241 = Course("fall", "2022", "MATH241")
        schedules = distances.Distance.generate_schedule_combinations([cs225, math241])
        self.assertEqual(len(schedules), 1000)
        #counting time conflicts takes too long because large schedule
        #self.assertEqual(distances.Distance.count_tc(schedules), 2)

    def test_best_schedule_large(self):#pass
        #best schedule is aba, al1 cs225 and ada, al1 math241
        #                 cif  follinger      alt alt
        cs225 = Course("fall", "2022", "CS225")
        math241 = Course("fall", "2022", "MATH241")
        schedules = distances.Distance.generate_schedule_combinations([cs225, math241])
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
        #self.assertEqual(distances.Distance.count_api_calls, 14)
        self.assertEqual(best_schedule[0].get_score(), 1.9)
        
    def test_best_schedule_large_two(self):#pass
        #all schedule sections are on different days so score is 0
        cs173 = Course("fall", "2022", "CS173")
        cs128 = Course("fall", "2022", "CS128")
        cs411 = Course("fall", "2022", "CS411")
        best_schedule = distances.Distance.best_schedule(courses=[cs173, cs128, cs411])
        self.assertEqual(best_schedule[0].get_score(), 0)
        distances.Distance.print_dictionary()
        #self.assertEqual(distances.Distance.count_api_calls, 0)

    def test_best_schedule_simple(self): #pass
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
                    ll.append(s.get_name() + " " + s.get_course() + " " + s.get_location())
                sch.append(ll)
            print(sch)
        worst_schedules = distances.Distance.worst
        #avoids lincoln hall, furthest away
        for s in worst_schedules:
            sch = []
            print("worst score: ", s.get_score())
            for ls in s.get_linked_sections():
                ll = []
                for s in ls:
                    ll.append(s.get_name() + " " + s.get_course() + " " + s.get_location())
                sch.append(ll)
            print(sch)
        
        distances.Distance.print_dictionary()
        #self.assertEqual(distances.Distance.count_api_calls,3)
        self.assertEqual(best_schedule[0].get_score(), 1.3)

if __name__ == "__main__":
    unittest.main()
    


#mcb150, chem102,103, las101, aas100, anth101