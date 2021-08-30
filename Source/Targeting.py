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


from Game import Game;
from Ship import Location;


class Targeting:
	NEGATIVE_DIRECTION = 0;
	POSITIVE_DIRECTION = 1;

	def __init__(self, ai, start, orientation, direction):
		self._ai = ai;  # the AI player for whom the Targeting object exists

		self.is_active = True;  # whether the targeting is still active
		# ITERATION
		self._orientation = orientation;  # orientation to travel in either a +/- direction: 0—vertical, 1—horizontal
		self._direction = direction;  # pursued direction along orientation: 0—negative direction, 1—positive direction
		self._next_switch = [];  # holds the switch function pointers to initiate the next search pattern
		# POSITIONS
		self._start = start.copy();
		self._current_point = start.copy();
		self._all_history = [start.copy()];  # list of points that have been attempted
		self._hit_history = [start.copy()];  # list of points that have been hit
		self._hits = [[[], []], [[], []]]  # [ vertical:[ -:[], +: []], horizontal:[ -:[], +: [] ] ]
		self._unknown_hits = [];

		self._destroyed_ships = {};  # {ship.id: ship.points [, ...]}


	def direction(self):
		return [-1, 1][self._direction];


	# ——————————————————————————————————————————————— MOVE CALCULATION ——————————————————————————————————————————————— #

	def next_move(self):
		next_point = self._incremented_point();
		if(self._next_move_is_invalid(next_point)): self._next_switch();


	# Next point relative to 
	def _incremented_point(self):
		incremented_point = _current_point.copy();
		incremented_point[self._orientation] += self.direction();

		return incremented_point;


	# Checks whether the next move is in bounds of the board.
	def _next_move_is_in_bounds(self, next_point=None):
		if(not next_point): next_point = self._incremented_point();

		return all(0 <= next_point[x] < FIELD_SIZE for x range(len(next_point)));


	# Checks whether the next move is in bounds of the board & has not been attacked already.
	def _next_move_is_invalid(self, next_point=None):
		if(not next_point): next_point = self._incremented_point();

		if(not self._next_move_is_in_bounds(next_point)): return True;
		return index(self._ai.player_shots, next_point) != Game.UNKNOWN;


	# ————————————————————————————————————————————————— MOVE RESULTS ————————————————————————————————————————————————— #

	# The previous move is counted as a miss. Mark it and adjust tactics.
	def move_missed_a_ship(self):
		pass;


	# The previous move sunk a ship. Mark it and adjust tactics.
	def move_sunk_a_ship(self, ship_id, ship_points):
		self._destroyed_ships[ship_id] = ship_points;
		#TODO: remove remaining queued points for orient/dir. # queued_points[self._orientation][self._direction] = [];

		destroyed_ships_points = [point for key in self._destroyed_ships for point in self._destroyed_ships[key]];
		non_sunk_ship_hits = [hit for hit in self._hits if hit not in destroyed_ships_points];
		# all hit points (including start) have been used to sink a ship
		if(len(non_sunk_ship_hits)): self.is_active = False;
		# other goes are necessary
		else:
			# If start point's ship has not been eliminated, keep searching for ship, starting at next pattern.
			if(self._start not in destroyed_ships_points): self._next_switch();
			# Start point's ship has been eliminated, meaning there are other ships discovered. Queue them up.

			#TODO: partion into other ships
			pass


	# ——————————————————————————————————————————————————  SWITCHING —————————————————————————————————————————————————— #

	# Calls the next switching function in the orientation/direction switch queue. Resets necessary values.
	def _next_switch(self):
		if(not self._next_switch): raise Exception("Switching is no longer available");
		self._next_switch.pop(0)();
		self._current_point = self._start.copy();


	def _switch_vertical(self):
		self._orientation = False;


	def _switch_horizontal(self):
		self._orientation = True;


	def _switch_minus(self):
		self._direction = False;


	def _switch_plus(self):
		self._direction = True;


	# —————————————————————————————————————————————— QUEUE  CALCULATION —————————————————————————————————————————————— #

	def calculate_hits_surrounding_points(self, start):
		points = [[[], []], [[], []]];  # [ vertical: [ minus: [], plus: [] ], horizontal: [ minus: [], plus: [] ] ]
		for orientation in range(2):
			for direction in range(2):
				# start = 0 if direction == Targeting.NEGATIVE_DIRECTION else start[orientation]+1
				start = (start[orientation]+1)*direction;
				# end = start[orientation] if direction == Targeting.NEGATIVE_DIRECTION else FIELD_SIZE;
				end = start[orientation]*(not direction) + FIELD_SIZE*direction;
				for y in range(start, end):
					point = shots[start[0] if orientation else y][y if orientation else start[0]];
					if(point == Game.UNKNOWN): points[orientation][direction].append(point);
					# points don't surround start; flush points from included points
					else: points[orientation][direction] = [];

		return points;


	def queue_points_and_switching_functions(self, points):
		pass;
