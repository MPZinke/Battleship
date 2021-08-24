

from random import randint

from Global import *


class Location:
	def __init__(self, orientation, span, start):
		self.orientation = orientation;  # bool 0-horizontal, 1-vertical
		self.points = [[start[0], start[1]+x] if orientation else [start[0]+x, start[1]] for x in range(span)];
		self.span = span;  # the length of the points
		self.start = start;  # starting point


	# Checks if any ship overlaps with the points in range.
	@staticmethod
	def any_ships_overlaps_points(ships, **kwargs):
		# Makes sure function is used properly
		if("points" not in kwargs and ("orientation" not in kwargs or "start" not in kwargs or "size" not in kwargs)):
			raise Exception("Function requires ('points') OR ('orientation', 'start', 'size')");

		# Get points (if points not provided, calculate them) & check them
		if("points" in kwargs): points = kwargs["points"];
		else: points = Location.points_are_in_range(kwargs["orientation"], kwargs["start"], kwargs["size"]);
		return any(point in points for ship in ships for point in ship.location.points);


	# Checks whether the specified point is in range based on orientation, size, & start.
	@staticmethod
	def points_are_in_range(orientation, start, size):
		return ((start[orientation] + size-1) < FIELD_SIZE) and (start[not orientation] < FIELD_SIZE);


	# Creates a random location within FIELD_SIZE with a random orientation & start.
	@staticmethod
	def random_location(size):
		orientation = randint(0, 1);
		max_size = FIELD_SIZE - 1;
		# Use some good ol' boolean algebra for logic
		start = [randint(0, max_size - size * (1 - orientation)), randint(0, max_size - size * orientation)];
		return Location(orientation, size, start);



class Ship:
	SHIPS =	[
				{"id": "Carrier1", "name": "Carrier", "size": 5},
				{"id": "Battleship1", "name": "Battleship", "size": 4},
				{"id": "Friggate1", "name": "Friggate", "size": 3},
				{"id": "Friggate2", "name": "Friggate", "size": 3},
				{"id": "Cruiser1", "name": "Cruiser", "size": 2}
			];

	def __init__(self, ship_id, name, size, location=None):
		self.id = ship_id;
		self.name = name;
		self.size = size;

		self.hits = [False] * size;
		self.location = location;


	# Unsafe way of attacking ship (assumes function calling method can guarentee that the location is hit).
	def hit(self, location):
		self.hits[location[self.location.orientation] - self.location.start[self.location.orientation]] = True;
		if(self.is_sunk()): print("SUNK");


	def is_hit(self, location):
		return any()


	def is_sunk(self):
		return all(hit for hit in self.hits);


	# Ship has been shot at. Determines if it is a hit and marks it if so.
	# Takes the location that was shot at.
	# Marks the hit if it was a hit.
	# Returns whether the ship was hit.
	def shot(self, location):
		if(location not in self.location.points): return False;

		# Mark where on the ship it was hit
		self.hits[location[self.location.orientation] - self.location.start[self.location.orientation]] = True;
		return True;


	@staticmethod
	def place_ships_randomly():
		ships = [];
		for ship in Ship.SHIPS:
			# Keep trying to get a random location for the ships (up to 65536)
			for x in range(0xFFFF):
				location = Location.random_location(ship["size"]);

				if(x == 0xFFFE): raise TooManyAttempts("The ship was unable to be placed in 65535 randomized attempts");
				if(not Location.any_ships_overlaps_points(ships, points=location.points)):
					ships.append(Ship(ship["id"], ship["name"], ship["size"], location));
					break;

		return ships;
