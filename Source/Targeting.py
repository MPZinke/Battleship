#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.29                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION: This is the main targeting class for the AI. It is called when a ship is hit, and proceeds to find    #
#     points where remaining ships may exist. It maintains it's object value in AI object, and is able to end its      #
#     targeting when all the known hit points are explored. It requires a few function calls for usage: 1) __init__,   #
#     2) next_point for determining the next point to hit.                                                             #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from Global import *;
from Ship import Location;


class Targeting:
	NEGATIVE_DIRECTION = 0;
	POSITIVE_DIRECTION = 1;

	def __init__(self, game, ai, start, queued_targets=[]):
		self._game = game;
		self._ai = ai;  # the AI player for whom the Targeting object exists

		self.is_active = True;  # whether the targeting is still active
		# ITERATION
		self._orientation = False;  # orientation to travel in either a +/- direction: 0—vertical, 1—horizontal
		self._direction = False;  # pursued direction along orientation: 0—negative direction, 1—positive direction
		self._pattern_switch_queue = [];  # holds the switch function pointers to initiate the next search pattern
		# POSITIONS
		self._start = start.copy();
		self._previous_point = start.copy();
		self._all_history = [start.copy()];  # list of points that have been attempted
		self._hit_history = [start.copy()];  # list of points that have been hit for the current targeting session

		self._queued_targets = queued_targets;
		self._previous_point_sunk_ship = None;  # the ship sunk for the previous point. Used by move_sunk_a_ship()
		self._sunk_ships = {};  # {ship.id: ship.points [, ...]}

		self._setup_targeting();


	# ————————————————————————————————————————————————————  SETUP ———————————————————————————————————————————————————— #

	def _setup_targeting(self):
		surrounding_points = self.calculate_surrounding_points();
		self._pattern_switch_queue = self.queue_switching_functions(surrounding_points);
		self._load_next_pattern();


	def _reset_targeting(self):
		self._previous_point = self._start.copy();
		self._hit_history = [self._start.copy()];
		self._setup_targeting();


	# ———————————————————————————————————————————————————  GETTERS ——————————————————————————————————————————————————— #

	def direction(self):
		return [-1, 1][self._direction];


	# ——————————————————————————————————————————————— MOVE CALCULATION ——————————————————————————————————————————————— #

	# Gets the next move for the targeting.
	# If current targeting pattern yeilds a bad point, next pattern is loaded.
	def next_move(self) -> list:
		self._update_from_previous_move();
		if(self._previous_point_sunk_ship): return self.previous_move_sunk_a_ship();

		self._all_history.append(self._incremented_previous_point());
		return self._all_history[-1].copy();


	# Next point relative to current point based on pattern
	def _incremented_previous_point(self):
		incremented_point = self._previous_point.copy();
		incremented_point[self._orientation] += self.direction();

		return incremented_point;


	# SUGAR: Returns whether the current point (self._previous_point) if a HIT.
	def _previous_point_is_hit(self) -> bool:
		return index(self._ai.player_shots, self._previous_point) == self._game.HIT;


	# SUGAR: Returns whether the current point (self._previous_point) if a MISS.
	def _previous_point_is_miss(self) -> bool:
		return index(self._ai.player_shots, self._previous_point) == self._game.MISS;


	# Checks whether the next move is in bounds of the board.
	def _next_move_is_in_bounds(self, next_point=None) -> bool:
		if(not next_point): next_point = self._incremented_previous_point();
		return all(0 <= coordinate and coordinate < FIELD_SIZE for coordinate in next_point);


	# Checks whether the next move is in bounds of the board & has not been attacked already.
	def _next_move_is_invalid(self, next_point=None) -> bool:
		if(not next_point): next_point = self._incremented_previous_point();

		if(not self._next_move_is_in_bounds(next_point)): return True;
		return index(self._ai.player_shots, next_point) != self._game.UNKNOWN;


	# ————————————————————————————————————————————————— MOVE RESULTS ————————————————————————————————————————————————— #

	# The previous move is counted as a miss. Mark it and adjust tactics.
	def move_missed_a_ship(self) -> None:
		self._load_next_pattern();


	# The previous move sunk a ship. Mark it and adjust tactics.
	# Takes the ship that has been sunk.
	# Adds the destroyed ship to known destroyed ships.
	# Sets the targeting of the calling AI based on the strategy & hits' statuses.
	def previous_move_sunk_a_ship(self) -> None:
		self._sunk_ships[self._previous_point_sunk_ship.id] = self._previous_point_sunk_ship.location.points;
		self._previous_point_sunk_ship = None;

		destroyed_ships_points = [point for key in self._sunk_ships for point in self._sunk_ships[key]];
		known_hits = self._hit_history + self._queued_targets;  # ship hits known to current targeting
		nonsunk_ship_hits = [hit for hit in known_hits if hit not in destroyed_ships_points];
		# All hit points (including start) have been used to sink a ship. Cannot proceed any more with targeting.
		if(not nonsunk_ship_hits): self._ai.targeting = None;
		# If start point's ship has not been eliminated, keep searching for ship, starting at next pattern.
		elif(self._start not in destroyed_ships_points):
			self._load_next_pattern();
			self._all_history.append(self._incremented_previous_point());
			return self._all_history[-1].copy();
		# Start point's ship has been eliminated, meaning there are other ships discovered. Start new targeting.
		else:
			self._ai.targeting = Targeting(self._game, self._ai, nonsunk_ship_hits.pop(0), nonsunk_ship_hits);
			return self._ai.targeting.next_move();
	

	# Calculates/sets values for the previous hit, now that it is updated on the player's shot.
	# Takes the ship that has been hit.
	# Sets the hit/miss value for the targeting. Records & sets up the targeting if a ship has been sunk.
	# NO CHEATING: You can do some naughty things with the ship info that was passed here.
	def record_previous_move(self, ship=None) -> None:
		if(self._previous_point_is_hit()): self._hit_history.append(self._previous_point.copy());
		elif(self._previous_point_is_miss()): pass;

		if(ship and ship.is_sunk()): return self.move_sunk_a_ship(ship);


	def _sunk_ship_for_previous_point(self):
		return self._game.sunk_ship_for_players_opponent_at_point(self._ai, self._previous_point.copy());


	# Previous move has been executed. Update previous point and pattern before proceeding to next move.
	# Automatically called by Targeting::next_move.
	def _update_from_previous_move(self):
		self._previous_point = self._all_history[-1].copy();

		if(self._previous_point_is_miss()): self._load_next_pattern();
		elif(self._previous_point_is_hit()):
			self._hit_history.append(self._previous_point.copy());
			self._previous_point_sunk_ship = self._sunk_ship_for_previous_point();

		if(not self._previous_point_sunk_ship and self._next_move_is_invalid()): self._load_next_pattern();


	# ——————————————————————————————————————————————————  SWITCHING —————————————————————————————————————————————————— #

	# Calls the next switching function in the orientation/direction switch queue. Resets necessary values.
	def _load_next_pattern(self):
		# The points are no longer available for the current orientation/direction
		if(not (self._pattern_switch_queue or self._queued_targets)): raise Exception("Switching is no longer available");
		elif(not self._pattern_switch_queue):
			self._start = self._queued_targets.pop(0);
			self._reset_targeting();
		else:
			self._pattern_switch_queue.pop(0)();
			self._previous_point = self._start.copy();


	# Switches the targeting pattern to be vertical.
	def _switch_vertical(self):
		self._orientation = Location.VERTICAL;


	# Switches the targeting pattern to be horizontal.
	def _switch_horizontal(self):
		self._orientation = Location.HORIZONTAL;


	# Switches the targeting pattern to be negative.
	def _switch_negative(self):
		self._direction = Targeting.NEGATIVE_DIRECTION;


	# Switches the targeting pattern to be positive.
	def _switch_positive(self):
		self._direction = Targeting.POSITIVE_DIRECTION;


	# —————————————————————————————————————————————— QUEUE  CALCULATION —————————————————————————————————————————————— #

	# Calculates the valid points surrounding the start point.
	# Goes through player_shots in the same row and column as the start point. 
	def calculate_surrounding_points(self):
		start = self._start.copy();
		points = [[[], []], [[], []]];  # [ vertical: [ minus: [], plus: [] ], horizontal: [ minus: [], plus: [] ] ]
		for orientation in range(2):
			for direction in range(2):
				range_start = (start[orientation]+1)*direction;  # if dir == -: 0, else start[orientation]+1
				# end = start[orientation] if direction == Targeting.NEGATIVE_DIRECTION else FIELD_SIZE;
				range_end = start[orientation]*(not direction) + FIELD_SIZE*direction;
				for i in range(range_start, range_end):
					point = self._ai.player_shots[start[0] if orientation else i][i if orientation else start[1]];
					if(point == self._game.UNKNOWN): points[orientation][direction].append(point);
					elif(range_start): break;  # counting up from start+1 we hit a hit/miss; no need to continue
					else: points[orientation][direction] = []; # points don't surround start; flush points
		
		return points;


	# Creates a list of switching functions based on surrounding points.
	# Takes the points surrounding the start.
	# Goes through orientation-directions from longest to shortest. Determines proper function to switch/load targeting
	#  to that pattern.
	# Returns a list of functions that call switching to determined pattern.
	def queue_switching_functions(self, surrounding_points):
		orientations = [self._switch_vertical, self._switch_horizontal];
		directions = [self._switch_negative, self._switch_positive];

		switch_patterns = [];
		# get longest order (from vertical to horizontal if tie): [vert_neg, vert_pos, hori_neg, hori_pos]
		lengths = [len(direction) for orientation in surrounding_points for direction in orientation];
		for _ in range(len(lengths)):
			longest = max(lengths);
			index = lengths.index(longest);
			lengths[index] = 0;  # prevent calling direction again
			if(longest == 0): break;  # don't queue up useless directions

			# Find function. 0b<orientation_bit><direction_bit>; index > 
			orientation_function = orientations[(index >> 1) & 1];
			direction_function = directions[index & 1];
			switch_patterns.append(lambda_helper(execute_multiple, orientation_function, direction_function));

		return switch_patterns;
