from course import Course
from section import Section
import unittest

class TestWebScraping(unittest.TestCase):
  
  def test_course_accessors_init(self):
    math241 = Course("spring", "2022", "MATH241")
    self.assertEqual(math241.get_subject(), "MATH")
    self.assertEqual(math241.get_number(), "241")
    self.assertEqual(math241.get_section('ADB').get_course(), "MATH241")

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
  
  def test_course_equals(self):
    math241_1 = Course("spring", "2022", "MATH241")
    math241 = Course("spring", "2022", "MATH241")
    self.assertTrue(math241_1 == math241)
  
  def test_section_equals(self):
    math241 = Course("spring", "2022", "MATH241")
    self.assertTrue(math241.get_section('ADB') == math241.get_section('ADB'))
  
  def test_section_time_conflict(self):
    math241 = Course("spring", "2022", "MATH241")
    aas100 = Course("spring", "2022", "AAS100")
    self.assertTrue(math241.get_section('ADB').has_time_conflict(aas100.get_section("AB")))
  
  def test_course_time_confict(self):
    math241 = Course("spring", "2022", "MATH241")
    aas100 = Course("spring", "2022", "AAS100")
    section_ls = [math241.get_section('ADB'), aas100.get_section('AB')]
    self.assertTrue(math241.has_time_conflict(section_ls))
  
  
  def test_linked_sections_simple(self):
    aas297 = Course("spring", "2022", "AAS297")

    linked_section_ls = aas297.get_linked_sections()
    section_a = Section('A', 'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml', aas297)
    section_b = Section('B', 'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml', aas297)

    ans = [Course.LinkedSection([section_a]), Course.LinkedSection([section_b])]

    for i in range(len(linked_section_ls)):
      self.assertEqual(linked_section_ls[i], ans[i])
  

  def test_linked_sections_complex(self):
    math241 = Course("spring", "2022", "MATH241")

    linked_section_ls = math241.get_linked_sections()
    ada = Section('ADA', 'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46053.xml', math241)
    adb = Section('ADB', 'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml', math241)
    al1 = Section('AL1', 'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46060.xml', math241)
    al2 = Section('AL2', 'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46067.xml', math241)

    ans = [Course.LinkedSection([ada, al1]), Course.LinkedSection([ada, al2]), Course.LinkedSection([adb, al1]), Course.LinkedSection([adb, al2])]

    for i in range(4):
      self.assertEqual(linked_section_ls[i], ans[i])
        
  
  def test_linked_section_equals(self):
    linked_section = Course.LinkedSection(['A'])
    linked_section1 = Course.LinkedSection(['A'])
    self.assertTrue(linked_section1 == linked_section)
    linked_section2 = Course.LinkedSection(['AB'])
    self.assertFalse(linked_section2 == linked_section)
   
if __name__ == '__main__':
    unittest.main()