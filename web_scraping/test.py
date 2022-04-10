from course import Course
import unittest

class TestWebScraping(unittest.TestCase):
  
  def test_course_accessors_init(self):
    math241 = Course("spring", "2022", "MATH241")
    self.assertEqual(math241.get_subject(), "MATH")
    self.assertEqual(math241.get_number(), "241")
    self.assertEqual(math241.get_section('ADB').get_course(), "MATH241")

    # aas100 = Course("spring", "2022", "AAS100")
    # self.assertEqual(aas100.get_section('AB ').get_course(), "AAS100")

  def test_split_sections(self):
    aas100 = Course("spring", "2022", "AAS100")
    sections_split = aas100.split_sections_on_type()
    self.assertEqual(sections_split["Lecture-Discussion"][0].get_name(), "AB")
  
  def test_section_accessors_init(self):
    section = Course("spring", "2022", "MATH241").sections['ADB']
    self.assertEqual(section.get_course(), "MATH241")
    self.assertEqual(section.get_name(), "ADB")
    self.assertEqual(section.get_type(), "Discussion/Recitation")
    self.assertEqual(section.get_location(), "Altgeld Hall")
    self.assertEqual(section.get_days(), "TR")
  
  def test_section_time_conflict(self):
    math241 = Course("spring", "2022", "MATH241")
    aas100 = Course("spring", "2022", "AAS100")
    self.assertTrue(math241.get_section('ADB').has_time_conflict(aas100.get_section("AB")))
  
  def test_course_time_confict(self):
    math241 = Course("spring", "2022", "MATH241")
    aas100 = Course("spring", "2022", "AAS100")
    section_ls = [math241.get_section('ADB'), aas100.get_section('AB')]
    self.assertTrue(math241.has_time_conflict(section_ls))
  
  # TODO: use actual asserts in this test
  def test_linked_sections_simple(self):
    aas297 = Course("spring", "2022", "AAS297")

    linked_section_ls = aas297.get_linked_sections()
    for linked in linked_section_ls:
      for section in linked:
        print(section.get_name())
      print('\n')
  
  # TODO: use actual asserts in this test
  def test_linked_sections_complex(self):
    aas297 = Course("spring", "2022", "MATH241")

    linked_section_ls = aas297.get_linked_sections()
    for linked in linked_section_ls:
      for section in linked:
        print(section.get_name())
      print('\n')



   
if __name__ == '__main__':
    unittest.main()
