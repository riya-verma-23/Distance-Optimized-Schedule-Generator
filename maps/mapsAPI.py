#update function to input limited number of classes
# takes in vector of locations 
def generateMapAPI(): 
    marker1 = raw_input("Enter the first class location: ")
    marker2 = raw_input("Enter the second class location: ")
    marker3 = raw_input("Enter the third class location: ")

    marker1_adjusted = '"'+marker1.replace(' ', '+', )+"+uiuc" + '"'
    marker2_adjusted = '"'+marker2.replace(' ', '+', )+"+uiuc" + '"'
    marker3_adjusted = '"'+marker3.replace(' ', '+', )+"+uiuc" + '"'

    api_key = ''
    try:
        with open('/Users/nalintiwary/Documents/CS 222 Project/course-project-tyk-b/maps/api_key.txt', 'r') as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % 'api_key')
    #print marker1_adjusted
    return "https://maps.googleapis.com/maps/api/staticmap?size=600x300" + "&markers=color:blue%7Clabel:1%7C" +marker1_adjusted+  "&markers=color:green%7Clabel:2%7C" +marker2_adjusted+"&markers=color:red%7Clabel:3%7C" +marker3_adjusted+ "&key="+api_key

def generateMapAPITwo(locations): 
    adjusted_locations = []
    for location in locations:
        adjusted_locations.append('"'+location.replace(' ', '+', )+"+uiuc" + '"')
        #print(location)
    #print marker1_adjusted
    markers = ""
    labels = ["&markers=color:gray%7Clabel:1%7C","&markers=color:green%7Clabel:2%7C", "&markers=color:orange%7Clabel:3%7C", "&markers=color:purple%7Clabel:4%7C", "&markers=color:red%7Clabel:5%7C", "&markers=color:white%7Clabel:6%7C", "&markers=color:yellow%7Clabel:7%7C",  "&markers=color:black%7Clabel:8%7C",  "&markers=color:blue%7Clabel:9%7C"]
    for i in range(len(adjusted_locations)):
        markers += labels[i] + adjusted_locations[i]
    
    api_key = ''
    try:
        with open('/Users/nalintiwary/Documents/CS 222 Project/course-project-tyk-b/maps/api_key.txt', 'r') as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % 'api_key')
    
    return "https://maps.googleapis.com/maps/api/staticmap?size=600x300" + markers +"&key="+api_key
 #<img src = generateMapAPI()>

#generateMapAPI()
#print(generateMapAPITwo(["david kinley", "grainger library", "isr", "far"]))

# add all the distances in order – from location 1-2, 2-3, 3-4 and so on 
# return the total distance between these points 
# create d function which takes in two lists of locations and outputs whichever has min total distance  
