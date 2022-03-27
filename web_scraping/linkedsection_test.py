from course import Course
from section import Section
import unittest

class TestWebScraping(unittest.TestCase):
  
  def test_linked_section_equals(self):
    linked_section = Course.LinkedSection(['A'])
    linked_section1 = Course.LinkedSection(['A'])
    self.assertTrue(linked_section1 == linked_section)
    linked_section2 = Course.LinkedSection(['AB'])
    self.assertFalse(linked_section2 == linked_section)

 
if __name__ == '__main__':
    unittest.main()