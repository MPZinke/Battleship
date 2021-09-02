#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.28                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from random import randint;

from Global import *;
from Exceptions import *;


class Location:
	HORIZONTAL = 1;
	VERTICAL = 0;

	def __init__(self, orientation, span, start):
		self.orientation = orientation;  # index of [row, column] value that changes: bool 0-vertical, 1-horizontal
		self.points = [[start[0], start[1]+x] if orientation else [start[0]+x, start[1]] for x in range(span)];
		self.span = span;  # the length of the points
		self.start = start;  # starting point


	def usable_points(self):
		return Location.usable(self.points);


	# ———————————————————————————————————————————————————— STATIC ———————————————————————————————————————————————————— #

	# Checks if there is any ship overlap with the points in range.
	@staticmethod
	def any_ship_overlap(ships, **kwargs):
		# Makes sure function is used properly
		if("points" not in kwargs and ("orientation" not in kwargs or "start" not in kwargs or "size" not in kwargs)):
			raise Exception("Location.any_ship_overlap requires ('points') OR ('orientation', 'start', 'size')");

		# Get points (if points not provided, calculate them) & check them
		if("points" in kwargs): points = kwargs["points"];
		else: points = Location(kwargs["orientation"], kwargs["size"], kwargs["start"]).points;
		return any(point in points for ship in ships for point in ship.location.points);


	# Checks whether the specified point is in range based on orientation, size, & start.
	# Takes either (points: list) OR (orientation: bool, size: int, start: list)
	@staticmethod
	def points_are_in_range(**kwargs):
		if("points" not in kwargs and ("orientation" not in kwargs or "start" not in kwargs or "size" not in kwargs)):
			raise Exception("Location.points_are_in_range requires ('points') OR ('orientation', 'start', 'size')");

		# whether last value in array is in range (assumes that the array is sorted from least to greatest)
		if("points" in kwargs): return kwargs["points"][-1][0] < FIELD_SIZE and kwargs["points"][-1][1] < FIELD_SIZE;

		# Get by keys
		orientation, size, start = [kwargs[key] for key in ["orientation", "size", "start"]];
		return (start[orientation] + size-1) < FIELD_SIZE and (start[not orientation] < FIELD_SIZE);


	# Creates a random location within FIELD_SIZE with a random orientation & start.
	@staticmethod
	def random_location(size):
		orientation = randint(0, 1);
		max_size = FIELD_SIZE - 1;
		# Use some good ol' boolean algebra for logic
		start = [randint(0, max_size - size * (1 - orientation)), randint(0, max_size - size * orientation)];
		return Location(orientation, size, start);


	@staticmethod
	def usable(points):
		return [point for point in points if point[0] < FIELD_SIZE and point[1] < FIELD_SIZE];


	@staticmethod
	def valid_location(ships, **kwargs):
		return not Location.any_ship_overlap(ships, **kwargs) and Location.points_are_in_range(**kwargs);



class Ship:
	SHIPS =	[
				{"name": "Carrier", "size": 5},
				{"name": "Battleship", "size": 4},
				{"name": "Friggate", "size": 3},
				{"name": "Submarine", "size": 3},
				{"name": "Cruiser", "size": 2}
			];

	def __init__(self, ship_id, name, size, location=None):
		self.id = ship_id;  # this better be unique for each ship owned by a player
		self.name = name;
		self.size = size;

		self.hits = [False for x in range(size)];
		self.location = location;


	# Unsafe way of attacking ship (assumes function calling method can guarentee that the location is in ship).
	# Safe alternative is shot().
	def hit(self, point):
		orientation = self.location.orientation;
		self.hits[point[not orientation] - self.location.points[0][not orientation]] = True;
		if(self.is_sunk()): print("SUNK");


	# Determines if point is a spot within the ship's points that could be considered a hit.
	def hits_ship(self, point):
		return point in self.location.points;


	# Determines if the ship has been hit at the point.
	# Compares the array value with True to return a copy value (instead of location).
	# Takes the point that is being checked.
	def is_hit(self, point):
		if(point not in self.location.points): return False;
		return self.hits[point[not self.location.orientation] - self.location.points[0][not self.location.orientation]]; 


	def is_sunk(self):
		return all(hit for hit in self.hits);


	# Ship is shot at by enemy. Determines if it is a hit and marks it if so.
	# Takes the point that was shot at.
	# Marks the hit if it was a hit.
	# Returns whether the ship was hit.
	def shot(self, point):
		if(point not in self.location.points): return False;

		# Mark where on the ship it was hit
		orientation = self.location.orientation;
		self.hits[point[orientation] - self.location.points[0][orientation]] = True;
		return True;


	# Returns the 1D offset from the start of a ship.
	def start_offset(self, point):
		if(point not in self.location.points): raise NotShipPoint(point);
		return point[self.location.orientation] - self.location.points[0][self.location.orientation];


	# ———————————————————————————————————————————————————— STATIC ———————————————————————————————————————————————————— #

	@staticmethod
	def place_single_ship_randomly(ship, ships):
		# Keep trying to get a random location for the ships (up to 65536)
		for x in range(0xFFFF):
			if(x == 0xFFFE): raise TooManyAttempts("The ship was unable to be placed in 65535 randomized attempts");

			location = Location.random_location(ship["size"]);
			if(not Location.any_ship_overlap(ships, points=location.points)):
				return Ship(len(ships), ship["name"], ship["size"], location);


	@staticmethod
	def place_all_ships_randomly():
		ships = [];
		for x, ship in enumerate(Ship.SHIPS):
			# Keep trying to get a random location for the ships (up to 65536)
			for y in range(0xFFFF):
				if(y == 0xFFFE): raise TooManyAttempts("The ship was unable to be placed in 65535 randomized attempts");

				location = Location.random_location(ship["size"]);
				if(not Location.any_ship_overlap(ships, points=location.points)):
					ships.append(Ship(x, ship["name"], ship["size"], location));
					break;

		return ships;
