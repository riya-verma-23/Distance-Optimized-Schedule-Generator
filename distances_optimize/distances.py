import requests
import json
from array import *
import re
import sys
sys.path.insert(0, 'web_scraping')
from course import Course
import section
sys.path.insert(1, 'schedule')
from schedule import Schedule
import itertools as it

class Distance:
		#dictionary {key = (section index, section index), value = distance}
	api_calls = {}

#Demo Code from https://gist.github.com/olliefr/407c64413f61bd14e7af62fada6df866
	#calls API and generates JSON file
	def distance_matrix_file(origins, destinations):
		print(origins, destinations)
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
		#reads in api key
		api_key = ''
		try:
			with open('distances_optimize/api_key', 'r') as f:
				api_key = f.read().strip()
		except FileNotFoundError:
			print("'%s' file not found" % 'api_key')
		print(api_key)

		payload = {
				'origins' : '|'.join(origins),
				'destinations' : '|'.join(destinations), 
				'key' : api_key
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

	#From JSON file, function extracts a matrix of distances
	#directly create dictionary instead of matrix
	def generateMatrixfromJSON(r, origin_size, dest_size): 
		matrix = []
		for i in range(origin_size):
			dist = []
			for j in range(dest_size):
				dist_str = r.json()["rows"][i]["elements"][j]["distance"]["text"]
				num = re.findall('\d*\.?\d+',dist_str)
				dist.append(float(num[0]))
				print("\nThe distance is ", dist)
			matrix.append(dist)
		
		return matrix
	
	def appendDictfromJSON(r, sections):
		for i in range(len(sections)):
			for j in range(len(sections)):
				if (i != j):
					dist_str = r.json()["rows"][i]["elements"][j]["distance"]["text"]
					num = re.findall('\d*\.?\d+',dist_str)
					#order tuple (sections[i], sections[j]) based on start time
					if (sections[i].get_start() < sections[j].get_start()):
						key = (sections[i], sections[j])
					else:
						key = (sections[j], sections[i])
					if key in Distance.api_calls: #finding the minimum here
						if float(num[0]) < Distance.api_calls[key]:
							Distance.api_calls[key] = float(num[0])
					else: Distance.api_calls[key] = float(num[0])
					#print dictionary Distance.api_calls
		for k, v in Distance.api_calls.items():
			print(k[0].get_name(), k[1].get_name(), v)

	#wrapper function that calls API and returns matrix of distances between each section
	def append_to_dict(sections):
		locations = []
		for section in sections:
			locations.append(section.get_location() + " UIUC")
		file = Distance.distance_matrix_file(locations, locations)
		Distance.appendDictfromJSON(file, sections)

	#takes in a set of linked sections (list of lists) and calculates score on each day
	def score(schedule):
		#returns 0..4 list with sections on each day
		daily_schedule = Schedule.split_sections_on_day(schedule)
		sum = 0
		for i in range(len(daily_schedule)):
			sum += Distance.calculatePerimeterPerDay(daily_schedule[i])
		return sum

	#generates unique unordered tuples for sections in Day
	def generate_tuple_sections(sectionsinDay):
		sectionsinDay = list(dict.fromkeys(sectionsinDay)) #removes repeats
		sectionsinDay = sorted(sectionsinDay, key=lambda x: x.start, reverse=False) #sort based on time
		tuples = it.combinations(sectionsinDay, 2)
		tuples = list(tuples)
		return tuples
		
	#elimininates sections that has already been called by the API and returns list of sections to be called
	def eliminate_sections(sectionsinDay):
		tuples = Distance.generate_tuple_sections(sectionsinDay)
		res = []
		for t in tuples:
			if not(t in Distance.api_calls):
				if not(t[0] in res): res.append(t[0])
				if not(t[1] in res): res.append(t[1])
		res = sorted(res, key=lambda x: x.start, reverse=False) #sort sections based on time
		return res

	#takes in an input of the sections on each day
	def calculatePerimeterPerDay(sectionsinDay):
		sections_to_call = Distance.eliminate_sections(sectionsinDay)
		#append to api call
		if (len(sections_to_call) != 0): 
			print("appended to dictionary in cppd")
			Distance.append_to_dict(sections_to_call)
		tuples = Distance.generate_tuple_sections(sectionsinDay)
		print("tuples")
		for t in tuples:
			print(t[0].get_name(),t[1].get_name())

		perimeter = 0
		for t in tuples:
			perimeter += Distance.api_calls[t]
		return perimeter


	#generates all schedule combinations by picking one linked section from each class and storing those schedules as a matrix of ordered locations
	#finding all possible combinations of linked sections => schedule
	def generateScheduleCombinations(courses):
		n = len(courses)

		ll = []
		for course in courses:
			ll.append(course.get_linked_sections())

		all_schedule = [] #each schedule will be a set of linked sections, all schedules is all possible sets
		indexes = []

		#initialize indexes to first combination (0, 0, 0)
		for i in range(n):
			indexes.append(0)

		while (1):
			schedule = [] 
			#Append the courses given the index combination to generate a schedule
			for i in range(n):
				schedule.append(ll[i][indexes[i]])
			
			if (not(Schedule.has_time_conflict(schedule))):
				all_schedule.append(schedule)
			
			#next is index of the last array
			next = n - 1
			
			#sets it to the righmost array that has more elements left
			while (next >= 0) & (indexes[next] + 1 >= len(ll[next])):
				next -= 1
				
			if next < 0:
				break
			
			#increments the index when more elements are left
			indexes[next] = indexes[next] + 1

			#set all points to 0 after
			for i in range((next+1), n, 1):
				indexes[i] = 0
			
		return all_schedule
				
	#all_schedules = [Schedule A, Schedule B, Schedule C]
	def findBestSchedule(all_schedules):
		min = 1000000000
		best_schedule = []
		for schedule in all_schedules:
			val = schedule.get_score()
			if val <= min:
				min = val
				best_schedule = schedule
		
		return best_schedule

	#sets the score of each schedule
	def scoreAllSchedules(all_schedules):
		for schedule in all_schedules:
			schedule.set_score(Distance.score(schedule))