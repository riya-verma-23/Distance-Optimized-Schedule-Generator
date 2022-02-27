import requests
import json
from array import *

#Demo Code from https://gist.github.com/olliefr/407c64413f61bd14e7af62fada6df866

def distance_matrix(origins, destinations):
	url = "https://maps.googleapis.com/maps/api/distancematrix/json?"

	payload = {
			'origins' : '|'.join(origins),
			'destinations' : '|'.join(destinations), 
			'key' : 'INSERT API KEY HERE'
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
	dist = []
	for i in range(origin_size):
		for j in range(dest_size):
			dist.append(r.json()["rows"][i]["elements"][j]["distance"]["text"])
			print("\nThe distance is ", dist)
		matrix.append(dist)
		dist.clear()

	return matrix
