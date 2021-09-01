#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Global import *;
from Ship import Location;


class Targeting:
	NEGATIVE_DIRECTION = 0;
	POSITIVE_DIRECTION = 1;

	def __init__(self, game, ai, start):
		print("———————————————————————————— __init__ ————————————————————————————");
		self._game = game;
		self._ai = ai;  # the AI player for whom the Targeting object exists

		self.is_active = True;  # whether the targeting is still active
		# ITERATION
		self._orientation = False;  # orientation to travel in either a +/- direction: 0—vertical, 1—horizontal
		self._direction = False;  # pursued direction along orientation: 0—negative direction, 1—positive direction
		self._next_switch = [];  # holds the switch function pointers to initiate the next search pattern
		# POSITIONS
		self._start = start.copy();
		self._current_point = start.copy();
		self._all_history = [start.copy()];  # list of points that have been attempted
		self._hit_history = [start.copy()];  # list of points that have been hit for the current targeting session
		self._all_hit_history = [];  # holds all hit points

		self._future_targets = [];
		self._destroyed_ships = {};  # {ship.id: ship.points [, ...]}

		self._setup_targeting();


	def _setup_targeting(self):
		print("———————————————————————————— _setup_targeting ————————————————————————————");
		surrounding_points = self.calculate_surrounding_points();
		self._next_switch = self.queue_switching_functions(surrounding_points);
		self._switch_pattern();


	def _reset_targeting(self):
		print("———————————————————————————— _reset_targeting ————————————————————————————");
		self._current_point = self._start.copy();
		self._hit_history = [self._start.copy()];
		self._setup_targeting();
		print(len(self._next_switch));


	def direction(self):
		print("———————————————————————————— direction ————————————————————————————");
		return [-1, 1][self._direction];


	# ——————————————————————————————————————————————— MOVE CALCULATION ——————————————————————————————————————————————— #

	def next_move(self):
		print("———————————————————————————— next_move ————————————————————————————");
		if(self._current_point_is_miss() or self._next_move_is_invalid()): self._switch_pattern();

		self._current_point = self._incremented_point();
		self._all_history.append(self._current_point);
		return self._current_point;


	# Next point relative to 
	def _incremented_point(self):
		print("———————————————————————————— _incremented_point ————————————————————————————");
		incremented_point = self._current_point.copy();
		incremented_point[self._orientation] += self.direction();

		return incremented_point;


	def _current_point_is_hit(self):
		print("———————————————————————————— _current_point_is_hit ————————————————————————————");
		return index(self._ai.player_shots, self._current_point) == self._game.HIT;


	def _current_point_is_miss(self):
		print("———————————————————————————— _current_point_is_miss ————————————————————————————");
		return index(self._ai.player_shots, self._current_point) == self._game.MISS;


	# Checks whether the next move is in bounds of the board.
	def _next_move_is_in_bounds(self, next_point=None):
		print("———————————————————————————— _next_move_is_in_bounds ————————————————————————————");
		if(not next_point): next_point = self._incremented_point();
		return all(0 <= coordinate and coordinate < FIELD_SIZE for coordinate in next_point);


	# Checks whether the next move is in bounds of the board & has not been attacked already.
	def _next_move_is_invalid(self, next_point=None):
		print("———————————————————————————— _next_move_is_invalid ————————————————————————————");
		if(not next_point): next_point = self._incremented_point();

		if(not self._next_move_is_in_bounds(next_point)): return True;
		return index(self._ai.player_shots, next_point) != self._game.UNKNOWN;


	# ————————————————————————————————————————————————— MOVE RESULTS ————————————————————————————————————————————————— #

	# The previous move is counted as a miss. Mark it and adjust tactics.
	def move_missed_a_ship(self):
		print("———————————————————————————— move_missed_a_ship ————————————————————————————");
		self._switch_pattern();


	# The previous move sunk a ship. Mark it and adjust tactics.
	def move_sunk_a_ship(self, ship):
		print("———————————————————————————— move_sunk_a_ship ————————————————————————————");
		self._destroyed_ships[ship.id] = ship.location.points;
		#TODO: remove remaining queued points for orient/dir. # queued_points[self._orientation][self._direction] = [];

		destroyed_ships_points = [point for key in self._destroyed_ships for point in self._destroyed_ships[key]];
		print("move_sunk_a_ship::destroyed_ships_points: {}".format(str(destroyed_ships_points)));
		non_sunk_ship_hits = [hit for hit in self._hit_history if hit not in destroyed_ships_points];
		print("move_sunk_a_ship::non_sunk_ship_hits: {}".format(str(non_sunk_ship_hits)));
		# all hit points (including start) have been used to sink a ship
		if(not non_sunk_ship_hits): self.is_active = False;
		# other goes are necessary
		else:
			# Start point's ship has been eliminated, meaning there are other ships discovered. Queue them up.
			if(self._start in destroyed_ships_points):
				print("———————————HERE———————————")
				[self._future_targets.append(point) for point in non_sunk_ship_hits];
			# If start point's ship has not been eliminated, keep searching for ship, starting at next pattern.
			else: pass;
			print("————THERE————")
			self._switch_pattern();
		print("—————————————————————————————————————");


	def record_previous_move(self, ship=None):
		print("———————————————————————————— record_previous_move ————————————————————————————");
		if(self._current_point_is_hit()):
			self._hit_history.append(self._current_point.copy());
			self._all_hit_history.append(self._current_point.copy());
		# Time to change things up
		elif(self._current_point_is_miss()): pass;

		if(ship and ship.is_sunk()): self.move_sunk_a_ship(ship);



	# ——————————————————————————————————————————————————  SWITCHING —————————————————————————————————————————————————— #

	# Calls the next switching function in the orientation/direction switch queue. Resets necessary values.
	def _switch_pattern(self):
		print("———————————————————————————— _switch_pattern ————————————————————————————");
		# The points are no longer available for the current orientation/direction
		if(not self._next_switch):
			print("_switch_pattern::_next_switch::_future_targets: {}".format(str(self._future_targets)));
			if(not self._future_targets): raise Exception("Switching & searchable points is no longer available");
			self._start = self._future_targets.pop(0);
			self._reset_targeting();
		else:
			self._next_switch.pop(0)();
			self._current_point = self._start.copy();
		print("————————————————————————————")


	def _switch_vertical(self):
		print("———————————————————————————— _switch_vertical ————————————————————————————");
		self._orientation = False;


	def _switch_horizontal(self):
		print("———————————————————————————— _switch_horizontal ————————————————————————————");
		self._orientation = True;


	def _switch_minus(self):
		print("———————————————————————————— _switch_minus ————————————————————————————");
		self._direction = False;


	def _switch_plus(self):
		print("———————————————————————————— _switch_plus ————————————————————————————");
		self._direction = True;


	# —————————————————————————————————————————————— QUEUE  CALCULATION —————————————————————————————————————————————— #

	# Calculates the valid points surrounding the start point.
	def calculate_surrounding_points(self):
		print("———————————————————————————— calculate_surrounding_points ————————————————————————————");
		start = self._start.copy();
		print("Start: ", str(start))
		points = [[[], []], [[], []]];  # [ vertical: [ minus: [], plus: [] ], horizontal: [ minus: [], plus: [] ] ]
		for orientation in range(2):
			for direction in range(2):
				print("HORIZ" if orientation else "VERT", "PLUS" if direction else "MINUS");
				# start = 0 if direction == Targeting.NEGATIVE_DIRECTION else start[orientation]+1
				range_start = (start[orientation]+1)*direction;
				# end = start[orientation] if direction == Targeting.NEGATIVE_DIRECTION else FIELD_SIZE;
				range_end = start[orientation]*(not direction) + FIELD_SIZE*direction;
				for y in range(range_start, range_end):
					point = self._ai.player_shots[start[0] if orientation else y][y if orientation else start[1]];

					print("{}({})".format(str([start[0] if orientation else y, y if orientation else start[0]]), {-1:"MISS", 0:"UNKNOWN", 1:"HIT"}[point]), end=" ");
					if(point == self._game.UNKNOWN): points[orientation][direction].append(point);
					elif(range_start):
						print("<-IGNORE");
						break;  # counting up from start+1 we hit a hit/miss; no need to continue
					else:
						print("<-IGNORE");
						points[orientation][direction] = []; # points don't surround start; flush points
				print();
		
		print("\n——————————————————————————————————————————————————————————————")
		return points;


	def queue_switching_functions(self, surrounding_points):
		print("———————————————————————————— queue_switching_functions ————————————————————————————");
		orientations = [self._switch_vertical, self._switch_horizontal];
		directions = [self._switch_minus, self._switch_plus];

		fnc = {self._switch_vertical: "vertical", self._switch_horizontal: "horizontal", 
				self._switch_minus: "minus", self._switch_plus: "plus"};

		# get longest order
		switch_order = [];
		print(surrounding_points);
		lengths = [len(direction) for orientation in surrounding_points for direction in orientation];
		print(lengths)
		for _ in range(len(lengths)):
			longest = max(lengths);
			index = lengths.index(longest);
			lengths[index] = 0;  # prevent calling direction again
			if(longest == 0): break;  # don't queue up useless directions

			# Find function
			orientation_function = orientations[(index & 2) >> 1];
			direction_function = directions[index & 1];
			print(fnc[orientation_function], fnc[direction_function]);
			switch_order.append(lambda_helper(execute_multiple, orientation_function, direction_function));

		return switch_order;
