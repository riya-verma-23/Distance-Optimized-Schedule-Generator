
import sys
sys.path.insert(1, '/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/web_scraping')
from course import Course
from section import Section
from schedule import Schedule
import unittest

class TestSchedule(unittest.TestCase):
  
    def test_linked_sectiions(self):
        math241 = Course("spring", "2022", "MATH241")
        schedule = Schedule(math241)
        math241_linked_sections = math241.get_linked_sections()
        self.assertEqual(schedule.linked_sections, math241_linked_sections)
  
    def test_get_score(self):
        math241 = Course("spring", "2022", "MATH241")
        schedule = Schedule(math241)
        self.assertEqual(schedule.get_score(), -9)

    def test_set_score(self):
      math241 = Course("spring", "2022", "MATH241")
      schedule = Schedule(math241)
      schedule.set_score(6)
      self.assertEqual(schedule.get_score(), 6)

    def test_set_course(self):
        math241 = Course("spring", "2022", "MATH241")
        schedule = Schedule(math241)
        cs225 = Course("spring", "2022", "CS225" )
        cs225_linked_sections = cs225.get_linked_sections()
        schedule.set_course(cs225)
        self.assertEqual(schedule.linked_sections, cs225_linked_sections)

if __name__ == '__main__':
    unittest.main()
