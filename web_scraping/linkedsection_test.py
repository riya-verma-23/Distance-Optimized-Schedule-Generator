from course import Course
from section import Section
import unittest

class TestWebScraping(unittest.TestCase):
    
    def test_linked_section_init_and_accessors(self):
        aas297 = Course("spring", "2022", "AAS297")
        section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        aas297) 
        section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            aas297)
        
        linked = Course.LinkedSection([section_a, section_b])
        self.assertEqual(section_a, linked[0])
    
    def test_linked_section_len(self):
        aas297 = Course("spring", "2022", "AAS297")
        section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        aas297) 
        section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            aas297)
        
        linked = Course.LinkedSection([section_a, section_b])
        self.assertEqual(len(linked), 2)
    
    def test_linked_section_equals(self):
        # using section name strings in place of actual sections to test faster
        linked_section = Course.LinkedSection(['A'])
        linked_section1 = Course.LinkedSection(['A'])
        self.assertTrue(linked_section1 == linked_section)
        linked_section2 = Course.LinkedSection(['AB'])
        self.assertFalse(linked_section2 == linked_section)

    def test_linked_section_add_section(self):
        aas297 = Course("spring", "2022", "AAS297")
        section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        aas297) 
        section_b = Section('B',
                            'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                            aas297)
        
        linked = Course.LinkedSection([section_a])

        linked.add_section(section_b)

        self.assertEqual(linked, Course.LinkedSection([section_a, section_b]))
    
    def test_section_ls_time_confict(self):
        math241 = Course("spring", "2022", "MATH241")
        aas100 = Course("spring", "2022", "AAS100")
        section_ls = [math241.get_section('ADB'), aas100.get_section('AB')]

        linked = Course.LinkedSection(section_ls)
        self.assertTrue(linked.has_time_conflict())

        section_ls_1 = [math241.get_section('ADB'), math241.get_section('ADB')]
        linked1 = Course.LinkedSection(section_ls_1)
        self.assertFalse(linked1.has_time_conflict())

 
if __name__ == '__main__':
    unittest.main()
