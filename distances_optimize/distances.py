from pickle import NONE
import requests
import json
from array import *
import itertools as it
import re
import sys
import os
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'web_scraping'))
sys.path.append(os.path.join(os.path.dirname(
    sys.path[0]), 'schedule'))
from csv import writer
# sys.path.insert(0, 'web_scraping')
# sys.path.insert(1, 'schedule')
from schedule_class import Schedule
from csv import reader

'''
This class is used to calculate the best distance optimized schedule
Input: list of course objects the user is taking
Output: a distance optimized Schedule Object that contains the linked sections to take for each course
'''

class Distance:
	#dictionary {key = (location str, location str), value = distance}
	api_calls = dict()
	count_api_calls = 0
	best = []
	worst = []

	#Demo Code from https://gist.github.com/olliefr/407c64413f61bd14e7af62fada6df866
	#calls API and generates JSON file with distances between origins and destinations
	def distance_matrix_file(origins_str, destinations_str):
		origins = [origins_str]
		destinations = [destinations_str]

		url = "https://maps.googleapis.com/maps/api/distancematrix/json?mode=walking"
		#reads in api key
		api_key = ''
		try:
			path = os.path.abspath(os.path.join(os.path.pardir, 'distances_optimize/api_key.txt'))
			with open(path, 'r') as f:
				api_key = f.read().strip()
		except FileNotFoundError:
			print("'%s' file not found" % 'api_key')

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
		dist_str = r.json()["rows"][0]["elements"][0]["distance"]["text"]
		if(dist_str.find("km") == -1):
			num = re.findall('\d*\.?\d+',dist_str)
			num = float(num[0])*0.001
		else:
			num = re.findall('\d*\.?\d+',dist_str)
			num = float(num[0])
		# #order tuple (sections[i], sections[j]) alphabetically
		if (sections[0].get_location() < sections[1].get_location()):
			key = (sections[0].get_location(), sections[1].get_location())
		else:
			key = (sections[1].get_location(), sections[0].get_location())
		if key in Distance.api_calls: #finding the minimum distance between section A to section B and vice versa
			if num < Distance.api_calls[key]:
				Distance.api_calls[key] = num
		else: Distance.api_calls[key] = num

	#wrapper function for distance_matrix_file and append_dict_from_JSON that calls API and appends to dictionary
	def append_to_dictionary(sections_two):
		#for section in sections_two: locations.append(section.get_location() + " UIUC")
		file = Distance.distance_matrix_file(sections_two[0].get_location() + " UIUC", sections_two[1].get_location() + " UIUC")
		Distance.append_dict_from_JSON(file, sections_two)

	#mimics append_to_dictionary call
	def count_api():
		Distance.count_api_calls += 1

	#takes in a set of linked sections and calculates score for a schedule
	def score(schedule):
		#returns 0..4 list with sections on each day
		daily_schedule = Schedule.split_sections_on_day(schedule)
		sum = 0
		for i in range(len(daily_schedule)): 
			sum += Distance.calculate_perimeter_per_day(daily_schedule[i])
		return sum
	
	#calculates the distance of the path (perimeter) between sections on a particular day
	def calculate_perimeter_per_day(sectionsinDay):
		#sort sectionsInDay based on start time
		sectionsinDay = sorted(sectionsinDay, key=lambda x: x.start, reverse=False)
		tuples = []
		for i in range(len(sectionsinDay) - 1):
			t = (sectionsinDay[i], sectionsinDay[i+1])
			tuples.append(t)
		for t in tuples:
			section = [t[0], t[1]]
			if (not(t[0].get_location(), t[1].get_location()) in Distance.api_calls) & (not(t[1].get_location(), t[0].get_location()) in Distance.api_calls):
				if(t[0].get_location() != t[1].get_location() and Distance.tuple_in_file((t[0].get_location(), t[1].get_location())) == NONE): #to make sure same locations not called
					Distance.count_api_calls+=1
					if Distance.count_api_calls > 25: print("API calls exceeded, program terminated.")
					else: Distance.append_to_dictionary(section)
		perimeter = 0
		for t in tuples:
			t_loc_1 = (t[0].get_location(), t[1].get_location())
			t_loc_2 = (t[1].get_location(), t[0].get_location())
			if (t_loc_1 in Distance.api_calls):
				perimeter += Distance.api_calls[t_loc_1]
			elif (t_loc_2 in Distance.api_calls):
				perimeter += Distance.api_calls[t_loc_2]
			elif (Distance.tuple_in_file(t_loc_1) != NONE):
				perimeter += Distance.tuple_in_file(t_loc_1)
		return perimeter
	
	#generates all valid schedule combinations without time conflicts by picking one linked section from each course
	def generate_schedule_combinations(courses):
		n = len(courses)
		print("generate all schedules combinations called")
		ll = []
		for course in courses:
			ll.append(course.get_linked_sections())
		print("linked l", ll)
		all_schedule = [] #each schedule will be a set of linked sections, all schedules is all possible sets
		indexes = []

		#initialize indexes to first combination (0, 0, 0)
		for i in range(n):
			indexes.append(0)
		count = 0
		while (1):
			count+=1
			schedule = [] 
			#Append the courses given the index combination to generate a schedule
			for i in range(n):
				schedule.append(ll[i][indexes[i]])
			
			s = Schedule(schedule)
			if (not(s.has_time_conflict())):
				all_schedule.append(s)

			if(len(all_schedule) >= 1000 or count >= 50000): break #cap at 1000 schedules

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
		for schedule in all_schedules: 
			s = round(Distance.score(schedule), 2)
			schedule.set_score(s)

	# user will input in the course names they are taking
	# course name is used to create a list of course objects which is passed into best_schedule
	# generates all valid schedules
	# scores all the schedules
	# by calling score on each schedule which sums up the distances between sections on all days
	# score() calls calculate_perimeter_per_day based on sections that occur on diff days
	# calculate_perimter_per_day() calls eliminate_sections() and generate_tuple_sections() and append_to_dictionary()
	# to retrive data from previous api calls and make new api calls
	# append_to_dictionary() calls distance_matrix_file() and append_dict_from_JSON() to retrive data from Distance Matrix API
	# after all schedules are scored, a list of schedules with the minimum score are returned
	def set_best_worst_schedule(courses):
		Distance.count_api_calls = 0 #reset api call count
		all_schedules = Distance.generate_schedule_combinations(courses)
		print("all schedules len", len(all_schedules))
		Distance.score_all_schedules(all_schedules)
		min = float("inf")
		best_schedule = []
		scores = []
		for schedule in all_schedules:
			val = schedule.get_score()
			scores.append(val)
			if val <= min:
				min = val
		#find all indices of the schedules with the min score
		for i in range(len(scores)):
			if scores[i] == min:
				best_schedule.append(all_schedules[i])
		Distance.best = best_schedule
		#Distance.set_worst_schedule(all_schedules)
		Distance.write_to_api_json()
	
	def best_schedule(courses):
		#Distance.set_best_worst_schedule(courses)
		return Distance.best
	
	def worst_schedule(courses):
		return Distance.worst
	
	def set_worst_schedule(all_schedules):
		max = 0
		worst_schedule = []
		scores = []
		for schedule in all_schedules:
			val = schedule.get_score()
			scores.append(val)
			if val > max:
				max = val
		#find all indices of the schedules with the min score
		for i in range(len(scores)):
			if scores[i] == max:
				worst_schedule.append(all_schedules[i])
		Distance.worst = worst_schedule

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
			else: count_tc+=1
			
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

	#print items in api_call dictionary
	def print_dictionary():
		print("Dictionary")
		print(len(Distance.api_calls))
		for key, value in Distance.api_calls.items():
			print(key, value)
	
	def write_to_api_json():
		path = os.path.abspath(os.path.join(os.path.pardir, 'distances_optimize/api_calls.csv'))
		with open(path, 'a+', newline='') as write_obj:
			csv_writer = writer(write_obj)
			for key, value in Distance.api_calls.items():
				list = [key[0], key[1], value]
				if Distance.tuple_in_file(key) == NONE:
					csv_writer.writerow(list)
    
	#if the tuple is in file, returns location, else returns NONE
	def tuple_in_file(tuple):
		path = os.path.abspath(os.path.join(os.path.pardir, 'distances_optimize/api_calls.csv'))
		with open(path, 'r') as read_obj:
			csv_reader = reader(read_obj)
			for row in csv_reader:
				if (row[0], row[1]) == (tuple[0], tuple[1]) or (row[1], row[0]) == (tuple[0], tuple[1]):
					return float(row[2])
			return NONE
			