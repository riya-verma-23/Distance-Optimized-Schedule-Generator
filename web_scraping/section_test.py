from course import Course
from section import Section
import unittest

# TODO: global variable of section: test practice
class TestSection(unittest.TestCase):
  
  def test_section_init_and_accessors(self):

    section = Section('ADB',
                      'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml',
                      'MATH241') 

    self.assertEqual(section.get_course(), "MATH241")
    self.assertEqual(section.get_name(), "ADB")
    self.assertEqual(section.get_type(), "Discussion/Recitation")
    self.assertEqual(section.get_location(), "Altgeld Hall")
    self.assertEqual(section.get_days(), "TR")
    self.assertEqual(section.get_start().strftime("%H:%M"), "09:00")
    self.assertEqual(section.get_end().strftime("%H:%M"), "09:50")

  def test_section_equals(self):
    section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        'AAS297')

    section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            'AAS297')

    self.assertEqual(section_a, section_a)

    self.assertNotEqual(section_b, section_a)

    section_a_1 = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2021/fall/AAS/297/64421.xml',
                        'AAS297')
    self.assertNotEqual(section_a_1, section_a)
    
  
  def test_section_time_conflict(self):

    math241_ada = Section('ADA',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46053.xml',
                  'MATH241')
    math241_adb = Section('ADB',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml',
                  'MATH241') 
    math241_adc = Section('ADC',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46056.xml',
                  'MATH241')
    math241_adf = Section('ADF',
                  "https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/48355.xml",
                  'MATH241')
    math241_al1 = Section('AL1',
                  "https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46060.xml",
                  'MATH241')
    aas100_ab = Section('AB',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/100/69781.xml',
                'AAS100') 
    aas100_ad2 = Section('AD2',
                "https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/100/41729.xml",
                'AAS100')

    # start at same time
    self.assertTrue(math241_adb.has_time_conflict(aas100_ab))

    # start during second section
    self.assertTrue(math241_adc.has_time_conflict(aas100_ab))
    
    # start and end at same time, overlap in days
    self.assertTrue(math241_al1.has_time_conflict(aas100_ad2))
    
    # after section section
    self.assertFalse(math241_adf.has_time_conflict(aas100_ab))

    # before second section
    self.assertFalse(math241_ada.has_time_conflict(aas100_ab))

    # same section
    self.assertFalse(math241_ada.has_time_conflict(math241_ada))
  
  def test_days_overlap(self):

    self.assertTrue(Section.days_overlap("MWF", "MWF"))

    self.assertTrue(Section.days_overlap("MW", "WF"))

    self.assertFalse(Section.days_overlap("MWF", "TR"))
  
  def test_hash(self):
    dictionary = {}
    try:
      section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        'AAS297')
      dictionary[section_a] = "hello world"
    except:
      self.fail("hash failed unexpectedly!")
 
if __name__ == '__main__':
    unittest.main()
