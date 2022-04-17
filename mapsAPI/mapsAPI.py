import sys
# sys.path.insert(0, "web_scraping")
sys.path.append('/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/web_scraping')
sys.path.append('/Users/sanyasharma/Documents/UIUC/222/course-project-tyk-b/schedule')
from schedule import Schedule
from course import Course
from section import Section
import requests 
from PIL import Image

class MapsAPI:
    # geneates map API for inputted locations
    def generate_map_API(): 
        marker1 = raw_input("Enter the first class location: ")
        marker2 = raw_input("Enter the second class location: ")
        marker3 = raw_input("Enter the third class location: ")

        marker1_adjusted = '"'+marker1.replace(' ', '+', )+"+uiuc" + '"'
        marker2_adjusted = '"'+marker2.replace(' ', '+', )+"+uiuc" + '"'
        marker3_adjusted = '"'+marker3.replace(' ', '+', )+"+uiuc" + '"'
        #print marker1_adjusted
        return "https://maps.googleapis.com/maps/api/staticmap?size=600x300" + "&markers=color:blue%7Clabel:1%7C" +marker1_adjusted+  "&markers=color:green%7Clabel:2%7C" +marker2_adjusted+"&markers=color:red%7Clabel:3%7C" +marker3_adjusted+ "&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"

# genereates map APIs based on a list of locations
    def generate_map_API_locations(locations): 
        adjusted_locations = []
        for location in locations:
            adjusted_locations.append('"'+location.replace(' ', '+', )+"+uiuc" + '"')
        markers = ""
        labels = ["&markers=color:gray%7Clabel:1%7C","&markers=color:green%7Clabel:2%7C", "&markers=color:orange%7Clabel:3%7C", "&markers=color:purple%7Clabel:4%7C", "&markers=color:red%7Clabel:5%7C", "&markers=color:white%7Clabel:6%7C", "&markers=color:yellow%7Clabel:7%7C",  "&markers=color:black%7Clabel:8%7C",  "&markers=color:blue%7Clabel:9%7C"]
        for i in range(len(adjusted_locations)):
            markers += labels[i] + adjusted_locations[i]
        
        return "https://maps.googleapis.com/maps/api/staticmap?size=600x300" + markers +"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"

    # generates maps APIs for given schedule
    # returns list of API calls for each days schedule
    def generate_map_API_schedule(schedule): 
        locations, result = [], []
        for day in schedule:
            locations_per_day = []
            for location in day:
                locations_per_day.append('"'+location.replace(' ', '+', )+"+uiuc illinois" + '"')
            locations.append(locations_per_day)
        
        labels = ["&markers=color:gray%7Clabel:1%7C","&markers=color:green%7Clabel:2%7C", "&markers=color:orange%7Clabel:3%7C", "&markers=color:purple%7Clabel:4%7C", "&markers=color:red%7Clabel:5%7C", "&markers=color:white%7Clabel:6%7C", "&markers=color:yellow%7Clabel:7%7C",  "&markers=color:black%7Clabel:8%7C",  "&markers=color:blue%7Clabel:9%7C"]
        for day in locations:
            markers = ""
            for j in range(len(day)):
                markers += labels[j] + day[j]
            if markers == "":
                result.append("")
            else:
                result.append("https://maps.googleapis.com/maps/api/staticmap?size=600x300" + markers +"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA")
        return result

cs374 = Course("spring", "2022", "CS374" )
schedule =  Schedule(cs374.get_linked_sections())
schedule_locations = schedule.return_locations()
print(MapsAPI.map_API_schedule(schedule_locations)[4])
print(schedule_locations)



# response = requests.get("https://maps.googleapis.com/maps/api/staticmap?size=600x300&markers=color:gray%7Clabel:1%7C\"Siebel+Center+for+Comp+Sci+uiuc illinois\"&markers=color:green%7Clabel:2%7C\"Campus+Instructional+Facility+uiuc illinois\"&key=AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA")

# file = open("sample_image.png", "wb")
# file.write(response.content)
# file.close()
# result = open("ballet_image.png","rb").read() == open("staticmap_374.png","rb").read()
# print(result)