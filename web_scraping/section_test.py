from course import Course
from section import Section
import unittest

class TestSection(unittest.TestCase):
  
  def test_bad_section_input(self):
    math231 = Course("spring", "2022", "MATH231")
    self.assertRaises(KeyError, math231.get_section, "ADZ")
  
  def test_section_init_and_accessors(self):
    section = Course("spring", "2022", "MATH241").sections['ADB']
    self.assertEqual(section.get_course(), "MATH241")
    self.assertEqual(section.get_name(), "ADB")
    self.assertEqual(section.get_type(), "Discussion/Recitation")
    self.assertEqual(section.get_location(), "Altgeld Hall")
    self.assertEqual(section.get_days(), "TR")
    self.assertEqual(section.get_start().strftime("%H:%M"), "09:00")
    self.assertEqual(section.get_end().strftime("%H:%M"), "09:50")

  def test_section_equals(self):
    aas297 = Course("spring", "2022", "AAS297")
    section_a = aas297.get_section('A')

    self.assertEqual(section_a, section_a)

    self.assertNotEqual(aas297.get_section('B'), section_a)

    aas297_1 = Course("fall", "2021", "AAS297")
    self.assertNotEqual(aas297_1.get_section('A'), section_a)
    
  
  def test_section_time_conflict(self):
    math241 = Course("spring", "2022", "MATH241")
    aas100 = Course("spring", "2022", "AAS100")

    aas100_ab = aas100.get_section("AB")
    math241_ada = math241.get_section('ADA')

    # start at same time
    self.assertTrue(math241.get_section('ADB').has_time_conflict(aas100_ab))

    # start during second section
    self.assertTrue(math241.get_section('ADC').has_time_conflict(aas100_ab))
    
    # start and end at same time, overlap in days
    self.assertTrue(math241.get_section('AL1').has_time_conflict(aas100.get_section("AD2")))
    
    # after section section
    self.assertFalse(math241.get_section('ADF').has_time_conflict(aas100_ab))

    # before second section
    self.assertFalse(math241_ada.has_time_conflict(aas100_ab))

    # same section
    self.assertFalse(math241_ada.has_time_conflict(math241_ada))
  
  def test_hash(self):
    aas297 = Course("spring", "2022", "AAS297")
    dictionary = {}
    try:
      section_a = aas297.get_section('A')
      dictionary[section_a] = "hello world"
    except:
      self.fail("hash failed unexpectedly!")
 
if __name__ == '__main__':
    unittest.main()
