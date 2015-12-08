from math import sin, cos, sqrt, atan2, radians

from math import sin, cos, sqrt, atan2, radians

def bounding_box_centroid(box):
	c = box[0]
	lon = (c[0][0] + c[3][0]) / 2
	lat = (c[0][1] + c[2][1]) / 2
	return [lon,lat]

def distance_from_rally(coordinates,rally_location):
	# approximate radius of earth in km
	R = 6378.135
	lat1 = radians(coordinates[1])
	lon1 = radians(coordinates[0])
	lat2 = radians((rally_location[1] + rally_location[3]) / 2) 
	lon2 = radians((rally_location[0] + rally_location[2]) / 2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	#conversion to miles
	distance *= 0.621371
	return distance

def distance_from_rally(coordinates,rally_location):
	# approximate radius of earth in km
	R = 6378.135
	lat1 = radians(coordinates[1])
	lon1 = radians(coordinates[0])
	lat2 = radians((rally_location[1] + rally_location[3]) / 2) 
	lon2 = radians((rally_location[0] + rally_location[2]) / 2)
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance = R * c
	#conversion to miles
	distance *= 0.621371
	return distance
