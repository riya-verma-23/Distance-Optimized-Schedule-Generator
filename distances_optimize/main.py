import requests
import json
from array import *
import distances
import sys
sys.path.insert(0, 'web_scraping')
from course import Course


#API KEY
api_key = "AIzaSyAc9dakhO8Q9CagQjaxXhSOLHYk_Vt4hQA"

# # #input all locations
# origins = []
# destinations = []

# # #Asking User for Local Address Input 
# loc1 = input("Enter loc1 address: ")
# loc2 = input("Enter loc2 address: ")
# loc3 = input("Enter loc3 address: ")
# loc4 = input("Enter loc4 address: ")

# # #origins and destinations are the same for ditance between every location with each other
# origins.append(loc1)
# origins.append(loc2)
# origins.append(loc3)
# origins.append(loc4)
# destinations.append(loc1)
# destinations.append(loc2)
# destinations.append(loc3)
# destinations.append(loc4)


# # #function that generates the output file for the distance matrix as a JSON
# r = distances.Distance.distance_matrix(origins, destinations)

# # #function that parses through that JSON file and stores the distances between each as a 2D matrix
# matrix = distances.Distance.generateMatrixfromJSON(r, len(origins), len(destinations))

# # #Print out the matrix of distances in strings returned
# print(matrix)

cs225 = Course("spring", "2022", "CS225")
scan252 = Course("spring", "2022", "SCAN252")
stat410 = Course("spring", "2022", "STAT410")

actual = distances.Distance.calculatePerimeterPerDay(sectionsinDay=[cs225.get_section("AYH"), scan252.get_section("C"), stat410.get_section("1UG")])
print(actual)
# print(distances.Distance.generate_tuple_sections(["AYH", "C", "1UG"]))
# print(distances.Distance.eliminate_sections(["AYH", "C", "1UG"]))
# print(distances.Distance.eliminate_sections([1,2,3]))
