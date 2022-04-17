import sys
import requests
import warnings
# sys.path.insert(0, "web_scraping")
# sys.path.insert(0, "schedule")
sys.path.append('/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/web_scraping')
sys.path.append('/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/schedule')
from course import Course
from section import Section
from schedule import Schedule
from mapsapi import MapsAPI
from PIL import Image
import unittest

class TestMapsAPI(unittest.TestCase):

    # def test_api_single_day(self):
    #     math241_monday_api = "https://maps.googleapis.com/maps/api/staticmap?size=600x300&markers=color:gray%7Clabel:1%7C\"Altgeld+Hall+uiuc illinois\"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"
    #     math241 = Course("spring", "2022", "MATH241" )
    #     schedule =  Schedule(math241.get_linked_sections())
    #     schedule_locations = schedule.return_locations()
    #     apis = MapsAPI.map_API_schedule(schedule_locations)
    #     self.assertEqual(apis[0], math241_monday_api)

    # def test_api_day(self):
    #     math241_thursday_api = "https://maps.googleapis.com/maps/api/staticmap?size=600x300&markers=color:gray%7Clabel:1%7C\"Altgeld+Hall+uiuc illinois\"&markers=color:green%7Clabel:2%7C\"Henry+Administration+Bldg+uiuc illinois\"&markers=color:orange%7Clabel:3%7C\"Engineering+Hall+uiuc illinois\"&markers=color:purple%7Clabel:4%7C\"Noyes+Laboratory+uiuc illinois\"&markers=color:red%7Clabel:5%7C\"Pennsylvania+Lounge+Bld+-+PAR+uiuc illinois\"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"
    #     math241 = Course("spring", "2022", "MATH241" )
    #     schedule =  Schedule(math241.get_linked_sections())
    #     schedule_locations = schedule.return_locations()
    #     apis = MapsAPI.map_API_schedule(schedule_locations)
    #     self.assertEqual(apis[3], math241_thursday_api)

    # def test_api_entire_list(self):
    #     cs222_api_list = ['', '', 'https://maps.googleapis.com/maps/api/staticmap?size=600x300&markers=color:gray%7Clabel:1%7C\"Siebel+Center+for+Comp+Sci+uiuc illinois\"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA', '', '']
    #     cs222 = Course("spring", "2022", "CS222" )
    #     schedule =  Schedule(cs222.get_linked_sections())
    #     schedule_locations = schedule.return_locations()
    #     api = MapsAPI.map_API_schedule(schedule_locations)
    #     self.assertEqual(api, cs222_api_list)

    # def test_image_size(self):
    #     math241 = Course("spring", "2022", "MATH241" )
    #     schedule =  Schedule(math241.get_linked_sections())
    #     schedule_locations = schedule.return_locations()
    #     api = MapsAPI.map_API_schedule(schedule_locations)[0]
    #     self.assertEqual(api[52:59], "600x300")

    # def test_incorrect_api(self):
    #     math241_monday_api = "https://maps.googleapis.com/maps/api/staticmap?size=600x300&markers=color:gray%7Clabel:1%7C\"Altgeld+Hall+uiuc illinois\"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"
    #     math241 = Course("spring", "2022", "MATH241" )
    #     schedule =  Schedule(math241.get_linked_sections())
    #     schedule_locations = schedule.return_locations()
    #     apis = MapsAPI.map_API_schedule(schedule_locations)
    #     self.assertNotEqual(apis[1], math241_monday_api)

    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    def tearDown(self):
        warnings.simplefilter("default", ResourceWarning)

    # def test_374_image_api(self):
    #     cs374 = Course("spring", "2022", "CS374" )
    #     schedule =  Schedule(cs374.get_linked_sections())
    #     schedule_locations = schedule.return_locations()
    #     api = MapsAPI.map_API_schedule(schedule_locations)[4]
    #     response = requests.get(api)
        
    #     file = open("CS_374_map.png", "wb")
    #     file.write(response.content)
    #     file.close()
    #     self.assertTrue(open("CS_374_map.png","rb").read() == open("staticmap_CS374.png","rb").read())

    # def test_241_image_api(self):
    #     math241 = Course("spring", "2022", "MATH241" )
    #     schedule =  Schedule(math241.get_linked_sections())
    #     api = MapsAPI.map_API_schedule(schedule.return_locations())[4]
    #     response = requests.get(api)

    #     file = open("Math_241_map.png", "wb")
    #     file.write(response.content)
    #     file.close()
    #     self.assertTrue(open("Math_241_map.png","rb").read() == open("staticmap_Math241.png","rb").read())

    # def test_241_incorrect_image_api(self):
    #     math241 = Course("spring", "2022", "MATH241" )
    #     schedule =  Schedule(math241.get_linked_sections())
    #     api = MapsAPI.map_API_schedule(schedule.return_locations())[3]
    #     response = requests.get(api)

    #     file = open("Math_241_map_Thursday.png", "wb")
    #     file.write(response.content)
    #     file.close()
    #     self.assertFalse(open("Math_241_map_Thursday.png","rb").read() == open("staticmap_Math241.png","rb").read())

    def test_image_size(self):
        cs374 = Course("spring", "2022", "CS374" )
        schedule =  Schedule(cs374.get_linked_sections())
        schedule_locations = schedule.return_locations()
        api = MapsAPI.map_API_schedule(schedule_locations)[2]
        response = requests.get(api)
        file = open("staticmap_374_size.png", "wb")
        file.write(response.content)
        file.close()
        im = Image.open('staticmap_374_size.png')
        width, height = im.size
        self.assertEqual(width, 600)
        self.assertEqual(height, 300)

if __name__ == '__main__':
    unittest.main()