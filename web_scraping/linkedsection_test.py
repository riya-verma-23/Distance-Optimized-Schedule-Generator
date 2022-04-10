

from course import Course
from section import Section
import unittest

class TestWebScraping(unittest.TestCase):
    
    def test_linked_section_init_and_accessors(self):
        section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        'AAS297') 
        section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            'AAS297')
        
        linked = Course.LinkedSection([section_a, section_b])

        self.assertEqual(section_a, linked[0])
        self.assertEqual(section_b, linked[1])
    
    def test_linked_section_len(self):
        section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        'AAS297') 
        section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            'AAS297')
        
        linked = Course.LinkedSection([section_a, section_b])
        self.assertEqual(len(linked), 2)
    
    def test_linked_section_equals(self):
        # using section name strings in place of actual sections to test faster
        linked_section = Course.LinkedSection(['A'])
        self.assertTrue(linked_section == linked_section)

        linked_section2 = Course.LinkedSection(['AB'])
        self.assertFalse(linked_section2 == linked_section)

    def test_linked_section_add_section(self):
        section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        'AAS297') 
        section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            'AAS297')

        linked1 = Course.LinkedSection([section_a, section_b])

        linked = Course.LinkedSection([section_a])
        linked.add_section(section_b)

        self.assertEqual(linked, linked1)
    
    def test_section_ls_time_confict(self):
        
        adb = Section('ADB',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml',
                        'MATH241') 
        ab = Section('AB',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/100/69781.xml',
                        'AAS100') 
        
        linked = Course.LinkedSection([ab])
        linked1 = Course.LinkedSection([adb])

        self.assertTrue(linked.has_time_conflict(linked1))        
        self.assertFalse(linked.has_time_conflict(linked))

 
if __name__ == '__main__':
    unittest.main()
