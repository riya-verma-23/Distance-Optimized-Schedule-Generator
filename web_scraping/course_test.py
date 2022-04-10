from course import Course
from section import Section
import unittest

# TODO: global variable of section: test practice
# TODO: global variable of course: test practice
# TODO: validation
# TODO: score threshold for generated schedules
# when the frontend and backend are linked we can each work on fullstack features
# for each of these features new branch
# for next week link front and back and make sure it works then discuss w tyler 
# how to improve in week 6 weekly meeting
class TestWebScraping(unittest.TestCase):
  
  def test_bad_course_input(self):
    self.assertRaises(ValueError, Course, "spring", "2022", "MATH10001")
    self.assertRaises(ValueError, Course, "spring", "3022", "MATH241")
    self.assertRaises(ValueError, Course, "spring", "-2022", "MATH241")
    self.assertRaises(ValueError, Course, "notasemester", "3022", "MATH241")
    self.assertRaises(ValueError, Course, "spring", "3022", "NOTASUBJECT241")
    
    try:
      Course("spring", "2022", "STAT400")
    except:
      self.fail("Course stat400 failed unexpectedly!")
    
  
  def test_bad_section_input(self):
    math231 = Course("spring", "2022", "MATH231")
    self.assertRaises(KeyError, math231.get_section, "ADZ")
  
  def test_course_init_and_accessors(self):
    math241 = Course("spring", "2022", "MATH241")
    self.assertEqual(math241.get_subject(), "MATH")
    self.assertEqual(math241.get_number(), "241")

    adb = Section('ADB',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml', 
                  "MATH241")
    self.assertEqual(math241.get_section('ADB'), adb)
  
  def test_equal_courses(self):
    math241 = Course("spring", "2022", "MATH241")
    self.assertEqual(math241, math241)

    math241_1 = Course("fall", "2021", "MATH241")
    self.assertNotEqual(math241_1, math241)

    aas100 = Course("spring", "2022", "AAS100")
    self.assertNotEqual(math241, aas100)
    
  def test_section_ls_time_confict(self):

    aas297 = Course("spring", "2022", "AAS297")

    aas100_ab = Section('AB',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/100/69781.xml',
                'AAS100')
    math241_adb = Section('ADB',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml', 
                  "MATH241")

    section_ls = [math241_adb, aas100_ab]
    self.assertTrue(aas297.has_time_conflict(section_ls))

    section_ls_1 = [math241_adb, math241_adb]
    self.assertFalse(aas297.has_time_conflict(section_ls_1))
  
  def test_section_ls_time_confict_complex(self):

    aas297 = Course("spring", "2022", "AAS297")

    cs211_ea1 = Section('EA1',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/fall/CS/211/74483.xml',
                'CS211')
    cs374_adf = Section('ADF',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/fall/CS/374/66451.xml',
                'CS374')
    cs374_al1 = Section('AL1',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/fall/CS/374/66445.xml',
                'CS374')
    cs411_qg = Section('QG',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/fall/CS/411/40086.xml',
                'CS411')
    cs340_ics = Section('ICS',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/fall/CS/340/77096.xml',
                'CS340')
    
    section_ls = [cs211_ea1, cs374_adf, cs374_al1, cs411_qg, cs340_ics]
    
    self.assertTrue(aas297.has_time_conflict(section_ls))
  
  def test_split_sections(self):
    aas283 = Course("spring", "2022", "AAS283")
    sections_split = aas283.split_sections_on_type()
    
    aas100_ad1 = Section('AD1',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/283/71840.xml',
                'AAS283')
    aas100_ad2 = Section('AD2',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/283/71842.xml',
                'AAS283')
    aas100_ad3 = Section('AD3',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/283/71844.xml',
                'AAS283')
    aas100_ad4 = Section('AD4',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/283/71846.xml',
                'AAS283')
    aas100_al1 = Section('AL1',
                'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/283/71838.xml',
                'AAS283')
    self.assertEqual(sections_split["Lecture"][0], aas100_al1)
    self.assertEqual(sections_split["Discussion/Recitation"][0], aas100_ad1)
    self.assertEqual(sections_split["Discussion/Recitation"][1], aas100_ad2)
    self.assertEqual(sections_split["Discussion/Recitation"][2], aas100_ad3)
    self.assertEqual(sections_split["Discussion/Recitation"][3], aas100_ad4)
  
  def test_linked_sections_simple(self):
    aas297 = Course("spring", "2022", "AAS297")

    linked_section_ls = aas297.get_linked_sections()
    section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        "AAS297") 
    section_b = Section('B',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                        "AAS297") 

    ans = [Course.LinkedSection([section_a]), Course.LinkedSection([section_b])]

    self.assertEqual(ans[0], linked_section_ls[0])
    self.assertEqual(ans[1], linked_section_ls[1])
  

  def test_linked_sections_complex(self):
    math241 = Course("spring", "2022", "MATH241")

    linked_section_ls = math241.get_linked_sections()
    ada = Section('ADA',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46053.xml',
                  "MATH241")
    adb = Section('ADB',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46054.xml', 
                  "MATH241")
    al1 = Section('AL1',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46060.xml',
                  "MATH241")
    al2 = Section('AL2',
                  'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/MATH/241/46067.xml',
                  "MATH241")

    ans = [Course.LinkedSection([ada, al1]), Course.LinkedSection([ada, al2]), Course.LinkedSection([adb, al1]), 
          Course.LinkedSection([adb, al2])]

    for i in range(4):
      self.assertEqual(linked_section_ls[i], ans[i])
  
  def test_key_in_dict(self):

    aas297 = Course("spring", "2022", "AAS297")

    section_dict = {}

    section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        "AAS297")

    section_dict["Lecture-Discussion"] = [section_a]

    self.assertEqual(aas297.key_in_dict("Lecture-Discussion", section_dict), "Lecture-Discussion")
    self.assertEqual(aas297.key_in_dict("Lecture", section_dict), "Lecture-Discussion")
    self.assertEqual(aas297.key_in_dict("Discussion", section_dict), "Lecture-Discussion")
    self.assertEqual(aas297.key_in_dict("Recitation", section_dict), "")

  def test_linked_sections_section_overlap(self):
    mus132 = Course("spring", "2022", "MUS132")
    linked = mus132.get_linked_sections()
    self.assertEqual(len(linked[0]), 2)

  def test_get_sections(self):
    aas297 = Course("spring", "2022", "AAS297")
    section_a = Section('A',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/62166.xml',
                        "AAS297") 
    section_b = Section('B',
                        'https://courses.illinois.edu/cisapp/explorer/schedule/2022/spring/AAS/297/73220.xml',
                        "AAS297")
    
    ans_ls = [section_a, section_b]
    section_ls = aas297.get_sections()

    self.assertEqual(ans_ls[0], section_ls[0])
    self.assertEqual(ans_ls[1], section_ls[1])

 
if __name__ == '__main__':
    unittest.main()
