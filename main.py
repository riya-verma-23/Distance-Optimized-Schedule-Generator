import requests
import json
from array import *
from distances import *

# #API KEY
api_key = "INSERT API KEY"

# #input all locations
origins = []
destinations = []

# #Asking User for Local Address Input 
loc1 = input("Enter loc1 address: ")
loc2 = input("Enter loc2 address: ")
loc3 = input("Enter loc3 address: ")
loc4 = input("Enter loc4 address: ")

# #origins and destinations are the same for ditance between every location with each other
origins.append(loc1)
origins.append(loc2)
origins.append(loc3)
origins.append(loc4)
destinations.append(loc1)
destinations.append(loc2)
destinations.append(loc3)
destinations.append(loc4)


# #function that generates the output file for the distance matrix as a JSON
r = distance_matrix(origins, destinations)

# #function that parses through that JSON file and stores the distances between each as a 2D matrix
matrix = generateMatrixfromJSON(r, len(origins), len(destinations))

# #Print out the matrix of distances in strings returned
print(matrix)

schedules = generateScheduleCombinations([[1,2], [3,4], [5, 6, 7]])
print(schedules)

