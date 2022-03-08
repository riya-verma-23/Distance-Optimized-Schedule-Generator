import requests
import json
from array import *
import datetime

class Section:
	day: int


#Demo Code from https://gist.github.com/olliefr/407c64413f61bd14e7af62fada6df866

def distance_matrix(origins, destinations):
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?"

	payload = {
			'origins' : '|'.join(origins),
			'destinations' : '|'.join(destinations), 
			'key' : 'INSERT API KEY'
	}

	r = requests.get(url, params = payload)

	#generates a file

	if r.status_code != 200:
			print('HTTP status code {} received, program terminated.'.format(r.status_code))
	else:
		try:
			x = json.loads(r.text)
			for isrc, src in enumerate(x['origin_addresses']):
				for idst, dst in enumerate(x['destination_addresses']):
					row = x['rows'][isrc]
					cell = row['elements'][idst]
					if cell['status'] == 'OK':
						print('{} to {}: {}, {}.'.format(src, dst, cell['distance']['text'], cell['duration']['text']))
					else:
						print('{} to {}: status = {}'.format(src, dst, cell['status']))

			with open('distancematrix.json', 'w') as f:
				f.write(r.text)

		except ValueError:
			print('Error while parsing JSON response, program terminated.')

	print(r.text)
	return r

def generateMatrixfromJSON(r, origin_size, dest_size): 
	matrix = []
	for i in range(origin_size):
		dist = []
		for j in range(dest_size):
			dist.append(r.json()["rows"][i]["elements"][j]["distance"]["text"])
			print("\nThe distance is ", dist)
		matrix.append(dist)

	return matrix

#takes in a set of linked sections (list of lists) and calculates score on each day
def score(schedule):
	daily_schedule = splitSections(schedule)
	sum = 0
	for i in range(len(daily_schedule)):
		sum += calculatePerimeterPerDay(daily_schedule[i])
	return sum


#takes in a list of linked sections and splits it based on sections on each day
def splitSections(schedule):
	daily_schedule = [0, 0, 0, 0, 0]

	for linked_section in schedule:
		for section in linked_section: #each section is going to have a day member variable initialized with 0..4
			daily_schedule.append(section.day)
	
	#list of sections on each day
	return daily_schedule


#takes in an input of the string locations for each day
def calculatePerimeterPerDay(sectionsinDay):
	distance_matrix = distance_matrix(sectionsinDay, sectionsinDay)
	perimeter = 0
	for i in range(len(distance_matrix) - 1):
		perimeter += distance_matrix[i][i+1]
	perimeter += distance_matrix[0][len(distance_matrix) - 1]
	return perimeter

#generates all schedule combinations by picking one linked section from each class and storing those schedules as a matrix of ordered locations
def generateScheduleCombinations(courses):
	n = len(courses)
	all_schedule = [] #each schedule will be a set of linked sections, all schedules is all possible sets
	indexes = []

	#initialize indexes to first combination (0, 0, 0)
	for i in range(n):
		indexes.append(0)

	while (1):
		schedule = [] 
		#Append the courses given the index combination to generate a schedule
		for i in range(n):
			schedule.append(courses[i][indexes[i]])
		all_schedule.append(schedule)
		
		#next is index of the last array
		next = n - 1
		
		#sets it to the righmost array that has more elements left
		while (next >= 0) & (indexes[next] + 1 >= len(courses[next])):
			next -= 1
			
		if next < 0:
			break
		
		#increments the index when more elements are left
		indexes[next] = indexes[next] + 1

		#set all points to 0 after
		for i in range((next+1), n, 1):
			indexes[i] = 0
		
	return all_schedule
			
def findBestSchedule(all_schedules):
	#calculate perimeter for each day which will be implemented later
	min = 1000000000
	best_schedule = []
	for schedule in range(all_schedules):
		val = score(schedule)
		if val < min:
			min = val
			best_schedule = schedule
	
	return best_schedule
