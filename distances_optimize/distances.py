import requests
import json
from array import *
import itertools as it
import re
import sys
sys.path.insert(0, 'web_scraping')
sys.path.insert(1, 'schedule')
from schedule import Schedule

'''
This class is used to calculate the best distance optimized schedule
Input: list of course objects the user is taking
Output: a distance optimized Schedule Object that contains the linked sections to take for each course
'''

class Distance:
	#dictionary {key = (section index, section index), value = distance}
	api_calls = dict()

	#Demo Code from https://gist.github.com/olliefr/407c64413f61bd14e7af62fada6df866
	#calls API and generates JSON file with distances between origins and destinations
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

	#Parses the JSON file generated and appends to a dictionary api_calls to keep track of distances
	def append_dict_from_JSON(r, sections):
		for i in range(len(sections)):
			for j in range(len(sections)):
				if (i != j):
					dist_str = r.json()["rows"][i]["elements"][j]["distance"]["text"]
					num = re.findall('\d*\.?\d+',dist_str)
					#order tuple (sections[i], sections[j]) based on start time
					if (sections[i].get_start() < sections[j].get_start()):
						key = (sections[i].get_location(), sections[j].get_location())
					else:
						key = (sections[j].get_location(), sections[i].get_location())
					if key in Distance.api_calls: #finding the minimum distance between section A to section B and vice versa
						if float(num[0]) < Distance.api_calls[key]:
							Distance.api_calls[key] = float(num[0])
					else: Distance.api_calls[key] = float(num[0])
					#print dictionary Distance.api_calls
		for k, v in Distance.api_calls.items():
			print(k[0], k[1], v)

	#wrapper function for distance_matrix_file and append_dict_from_JSON that calls API and appends to dictionary
	def append_to_dictionary(sections):
		locations = []
		for section in sections: locations.append(section.get_location() + " UIUC")
		file = Distance.distance_matrix_file(locations, locations)
		Distance.append_dict_from_JSON(file, sections)

	#takes in a set of linked sections and calculates score for a schedule
	def score(schedule):
		#returns 0..4 list with sections on each day
		daily_schedule = Schedule.split_sections_on_day(schedule)
		sum = 0
		for i in range(len(daily_schedule)): sum += Distance.calculate_perimeter_per_day(daily_schedule[i])
		return sum

	#generates unique sorted tuples (section, section) by start time for sections on a particular day
	#needed to identify sections that have already been called by the API or tuple of sections that needs to be called
	def generate_tuple_sections(sectionsinDay):
		sectionsinDay = list(dict.fromkeys(sectionsinDay)) #removes repeats
		sectionsinDay = sorted(sectionsinDay, key=lambda x: x.start, reverse=False) #sort based on time
		tuples = list(it.combinations(sectionsinDay, 2))
		return tuples
		
	#eliminates sections that has already been called by the API and returns list of sections to be called
	def eliminate_sections(sectionsinDay):
		tuples = Distance.generate_tuple_sections(sectionsinDay)
		res = []
		for t in tuples:
			if not(t in Distance.api_calls):
				if not(t[0] in res): res.append(t[0])
				if not(t[1] in res): res.append(t[1])
		res = sorted(res, key=lambda x: x.start, reverse=False) #sort sections based on time
		return res

	#calculates the distance of the path (perimeter) between sections on a particular day
	def calculate_perimeter_per_day(sectionsinDay):
		sections_to_call = Distance.eliminate_sections(sectionsinDay)
		if (len(sections_to_call) != 0): 
			Distance.append_to_dictionary(sections_to_call)
		tuples = Distance.generate_tuple_sections(sectionsinDay)
		perimeter = 0
		for t in tuples:
			t_loc = (t[0].get_location(), t[1].get_location())
			perimeter += Distance.api_calls[t_loc]
		return perimeter

	#generates all valid schedule combinations without time conflicts by picking one linked section from each course
	def generate_schedule_combinations(courses):
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
			
			s = Schedule(schedule)
			if (not(s.has_time_conflict())):
				all_schedule.append(s)
			
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

	#sets the score of all valid schedules
	def score_all_schedules(all_schedules):
		for schedule in all_schedules: schedule.set_score(Distance.score(schedule))
	
	#user will input in the course names they are taking
	#course name is used to create a list of course objects which is passed into best_schedule
	#generates all valid schedules
	#scores all the schedules
	#by calling score on each schedule which sums up the distances between sections on all days
	#score() calls calculate_perimeter_per_day based on sections that occur on diff days
	#calculate_perimter_per_day() calls eliminate_sections() and generate_tuple_sections() and append_to_dictionary()
	#to retrive data from previous api calls and make new api calls
	#append_to_dictionary() calls distance_matrix_file() and append_dict_from_JSON() to retrive data from Distance Matrix API
	def best_schedule(courses):
		all_schedules = Distance.generate_schedule_combinations(courses)
		Distance.score_all_schedules(all_schedules)
		min = 1000000000.0
		best_schedule = []
		for schedule in all_schedules:
			val = schedule.get_score()
			if val <= min:
				min = val
				best_schedule = schedule
		return best_schedule
	
	def print_time_conflicts(schedules):
			out = []
			for i in range(len(schedules)):
				sch = []
				for ls in schedules[i].get_linked_sections():
					ll = []
					for s in ls:
						ll.append(s.get_name() + " " + s.get_course())
					sch.append(ll)
				out.append(sch)
			print(out)

	def count_tc(courses):
		n = len(courses)
		count_tc = 0

		ll = []
		for course in courses:
			ll.append(course.get_linked_sections())
	
		indexes = []

		#initialize indexes to first combination (0, 0, 0)
		for i in range(n):
			indexes.append(0)

		while (1):
			schedule = [] 
			#Append the courses given the index combination to generate a schedule
			for i in range(n):
				schedule.append(ll[i][indexes[i]])
			
			s = Schedule(schedule)

			
			if s.has_time_conflict():
				count_tc += 1
			
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

		return count_tc
