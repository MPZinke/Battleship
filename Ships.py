

from random import randint

from Global import *


class Location:
	def __init__(self, orientation, span, start):
		self.orientation = orientation  # bool 0-horizontal, 1-vertical
		self.span = span
		self.start = start
		# TODO: find points in range for values

		self.points = []
		for x in range(span):
			self.points.append([start[0], start[1]+x] if orientation else [start[0]+x, start[1]])


class Ship:
	def __init__(self, name, size):
		self.name = name
		self.size = size

		self.hits = [False] * size
		self.location = None


	def hit(self, location):
		self.hits[location[self.location.orientation] - self.location.start[self.location.orientation]] = True
		if(self.is_sunk()): print("SUNK")


	def is_sunk(self):
		return not any(not hit for hit in self.hits)




def any_ship_in_range(orientation, start, size, ships):
	for x in range(size):
		location = [start[0], start[1]+x] if orientation else [start[0]+x, start[1]]
		for y in range(len(ships)):
			for z in range(len(ships[y].location.points)):
				if location == ships[y].location.points[z]: return True
	return False


def points_in_range(orientation, start, size):
	points = []
	for x in range(size):
		if (start[1] + x < FIELD_SIZE and orientation) or (start[0] + x < FIELD_SIZE and not orientation):
			points.append([start[0], start[1]+x] if orientation else [start[0]+x, start[1]])
	return points


def random_location(size):
	orientation = randint(0, 1)
	max_size = FIELD_SIZE - 1
	start = [randint(0, max_size - size * (1 - orientation)), randint(0, max_size - size * orientation)]
	return orientation, start


def place_ships_randomly():
	ships = []

	for x in range(len(SHIP_SIZES)):
		orientation, start = random_location(SHIP_SIZES[x])

		while any_ship_in_range(orientation, start, SHIP_SIZES[x], ships): orientation, start = random_location(SHIP_SIZES[x])
		ships.append(Ship(SHIP_NAMES[x], SHIP_SIZES[x]))
		ships[x].location = Location(orientation, SHIP_SIZES[x], start)

	return ships

