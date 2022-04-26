import os
import sys
sys.path.insert(0, "web_scraping")
sys.path.insert(0, "schedule")
# sys.path.append('/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/web_scraping')
# sys.path.append('/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/schedule')
from schedule_class import Schedule
from course import Course
from section import Section
import requests 
from PIL import Image

class MapsAPI:
    def get_map_API(): 
        marker1 = raw_input("Enter the first class location: ")
        marker2 = raw_input("Enter the second class location: ")
        marker3 = raw_input("Enter the third class location: ")

        marker1_adjusted = '"'+marker1.replace(' ', '+', )+"+uiuc" + '"'
        marker2_adjusted = '"'+marker2.replace(' ', '+', )+"+uiuc" + '"'
        marker3_adjusted = '"'+marker3.replace(' ', '+', )+"+uiuc" + '"'
        #print marker1_adjusted
        return "https://maps.googleapis.com/maps/api/staticmap?size=600x300" + "&markers=color:blue%7Clabel:1%7C" +marker1_adjusted+  "&markers=color:green%7Clabel:2%7C" +marker2_adjusted+"&markers=color:red%7Clabel:3%7C" +marker3_adjusted+ "&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"

# genereates map APIs based on a list of locations
    def generate_map_API(locations): 
        adjusted_locations = []
        for location in locations:
            adjusted_locations.append('"'+location.replace(' ', '+', )+"+uiuc" + '"')
        markers = ""
        labels = ["&markers=color:gray%7Clabel:1%7C","&markers=color:green%7Clabel:2%7C", "&markers=color:orange%7Clabel:3%7C", "&markers=color:purple%7Clabel:4%7C", "&markers=color:red%7Clabel:5%7C", "&markers=color:white%7Clabel:6%7C", "&markers=color:yellow%7Clabel:7%7C",  "&markers=color:black%7Clabel:8%7C",  "&markers=color:blue%7Clabel:9%7C"]
        for i in range(len(adjusted_locations)):
            markers += labels[i] + adjusted_locations[i]
        api_key = ''
        try:
            path = os.path.abspath(os.path.join(os.path.pardir, 'maps/api_key.txt'))
            print(path)
            with open(path, 'r') as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            print("'%s' file not found" % 'api_key')
        
        return "https://maps.googleapis.com/maps/api/staticmap?size=600x300" + markers +"&key="+api_key

    # generates maps APIs for given schedule
    # returns list of API calls for each days schedule
    def map_API_schedule(schedule): 
        locations, result = [], []
        #Schedule is not a iteratable class
        for daily_schedule in schedule.split_sections_on_day():
            locations_per_day = []
            for section in daily_schedule:
                locations_per_day.append('"'+section.get_location().replace(' ', '+', )+"+uiuc illinois" + '"')
            locations.append(locations_per_day)
        
        api_key = ''
        try:
            path = os.path.abspath(os.path.join(os.path.pardir, 'maps/api_key.txt'))
            print(path)
            with open(path, 'r') as f:
                api_key = f.read().strip()
        except FileNotFoundError:
            print("'%s' file not found" % 'api_key')
        
        labels = ["&markers=color:gray%7Clabel:1%7C","&markers=color:green%7Clabel:2%7C", "&markers=color:orange%7Clabel:3%7C", "&markers=color:purple%7Clabel:4%7C", "&markers=color:red%7Clabel:5%7C", "&markers=color:white%7Clabel:6%7C", "&markers=color:yellow%7Clabel:7%7C",  "&markers=color:black%7Clabel:8%7C",  "&markers=color:blue%7Clabel:9%7C"]
        for day in locations:
            markers = ""
            for j in range(len(day)):
                markers += labels[j] + day[j]
            if markers == "":
                result.append("")
            else:
                result.append("https://maps.googleapis.com/maps/api/staticmap?size=600x300" + markers +"&key="+api_key)
        return result
