
import sys
sys.path.insert(0, 'web_scraping')
from course import Course
from section import Section
from schedule import Schedule
import unittest

class TestSchedule(unittest.TestCase):
  
    def test_linked_sectiions(self):
      math241 = Course("spring", "2022", "MATH241")
      schedule = Schedule(math241.get_linked_sections())
      math241_linked_sections = math241.get_linked_sections()
      self.assertEqual(schedule.linked_sections, math241_linked_sections)

    def test_split_sections_on_day(self):
      cs233_monday = ['AL1', 'ALP', 'AL2', 'ALR']
      cs233 = Course("spring", "2022", "CS233" )
      schedule =  Schedule(cs233.get_linked_sections())
      split_schedule = schedule.split_sections_on_day_str()
      self.assertEqual(split_schedule[0], cs233_monday)

    def test_split_sections_on_day_monday(self):
      cs233_tuesday = []
      cs233 = Course("spring", "2022", "CS233" )
      schedule =  Schedule(cs233.get_linked_sections())
      split_schedule = schedule.split_sections_on_day_str()
      self.assertEqual(split_schedule[1], cs233_tuesday)

    def test_split_sections_on_day_aas283(self):
      aas283 = Course("spring", "2022", "AAS283" )
      aas283_schedule = [[], ['AL1'], [], ['AD2', 'AL1', 'AD3'], ['AD4', 'AD1']]
      schedule =  Schedule(aas283.get_linked_sections())
      split_schedule = schedule.split_sections_on_day_str()
      self.assertEqual(split_schedule, aas283_schedule)

    def test_return_locations_friday(self):
      cs225_friday = ['Siebel Center for Comp Sci', 'Electrical & Computer Eng Bldg']
      cs225 = Course("spring", "2022", "CS225")
      schedule =  Schedule(cs225.get_linked_sections())
      self.assertEqual(schedule.return_locations()[4], cs225_friday)

    def test_return_locations(self):
      cs233 = Course("spring", "2022", "CS233")
      schedule =  Schedule(cs233.get_linked_sections())
      locations = [['Campus Instructional Facility'], [], ['Campus Instructional Facility'], [], []]
      self.assertEqual(schedule.return_locations(), locations)

    def test_get_score(self):
      math241 = Course("spring", "2022", "MATH241")
      schedule = Schedule(math241.get_linked_sections())
      self.assertEqual(schedule.get_score(), -9)

    def test_set_score(self):
      math241 = Course("spring", "2022", "MATH241")
      schedule = Schedule(math241.get_linked_sections())
      schedule.set_score(6)
      self.assertEqual(schedule.get_score(), 6)

    def test_set_course(self):
      math241 = Course("spring", "2022", "MATH241")
      schedule = Schedule(math241.get_linked_sections())
      cs225 = Course("spring", "2022", "CS225" )
      cs225_linked_sections = cs225.get_linked_sections()
      schedule.set_course(cs225)
      self.assertEqual(schedule.linked_sections, cs225_linked_sections)
    
    def test_has_time_conflict(self):
      math241 = Course("spring", "2022", "MATH241")
      schedule = Schedule(math241.get_linked_sections())
      self.assertTrue(schedule.has_time_conflict())

    def test_has_time_conflict(self):
      cs222 = Course("spring", "2022", "CS222")
      schedule = Schedule(cs222.get_linked_sections())
      self.assertFalse(schedule.has_time_conflict())

if __name__ == '__main__':
    unittest.main()
