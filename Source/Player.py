#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.24                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from random import randint;

from Global import *;
from Targeting import Targeting;
from Ship import Location, Ship;


class Player:
	def __init__(self, game, player_id, name, **kwargs):
		self.game = game;

		self.id = player_id;
		self.name = name;
		self.is_AI = kwargs.get("is_AI", False);
		# SHIPS
		self.ships_are_placed = False;  # whether the ships for the player have been placed
		self.ships = [];
		# ATTACKS
		self.shot_history = [];  # list of points where player has attacked the enemy
		self.player_shots = [[Game.UNKNOWN for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];
		self.enemy_shots = [[False for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];  # places opponent has shot


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def last_placed_ship(self):
		return self.ships[-1] if self.ships else None;


	def place_ships(self, point, orientation):
		raise Exception("No function for Player::place_ships defined in a child class");


	def print(self):
		for x in range(FIELD_SIZE):
			row = "";
			for y in range(FIELD_SIZE):
				value = 1;
				bools = [self.is_hit([x,y]), self.enemy_shots[x][y], self.is_hit([x,y]) and self.enemy_shots[x][y]];
				for x in range(len(bools)): value = bools[x] * (1 << x) + (not bools[x] * value);
				row += {1: OCEAN_CHAR_CLI, 2: SHIP_CHAR, 4: MISS_CHAR, 8: HIT_CHAR}[value];
			print(row);


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	# Return if a shot hits a ship.
	def hits_a_ship(self, point):
		return any(ship.hits_ship(point) for ship in self.ships);


	# Function called when attacking another player.
	# Player is SHOOTing opponent.
	def shoot_at_enemy(self, point, shot_ship=None):
		self.player_shots[point[0]][point[1]] = Game.HIT if shot_ship else Game.MISS;


	# Function called when a player is being attacked by the other player.
	# Player is being SHOT by opponent.
	def shot(self, point):
		self.enemy_shots[point[0]][point[1]] = True;
		shot_ship = [ship for ship in self.ships if ship.shot(point)];
		if(shot_ship): return shot_ship[0];
		return None;



	# ———————————————————————————————————————————————————  GETTERS ——————————————————————————————————————————————————— #

	def remaining_ships(self):
		return [ship for ship in self.ships if not ship.is_sunk()];



class AI(Player):
	def __init__(self, game, player_id, name="Enemy"):
		Player.__init__(self, game, player_id, name, is_AI=True);

		self.previous_shots = [];  # previous shots
		self.targeting = False;  # whether the enemy has found a ship and is tracking it
		self.next_shot_queue = [];  # determine where to shoot next
		self.orientation = 0;  # orientation to travel in either a + or - direction: 0—vertical, 1—horizontal
		self._direction = False;  # direction along orientation to pursue: 0—negative direction, 1—positive direction


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	def attack(self):
		self.game.enemy_board.print()  #TESTING
		# attack logic


	def shoot_at_enemy(self, point, shot_ship=None):
		self.player_shots[point[0]][point[1]] = Game.HIT if shot_ship else Game.MISS;
		if(not self.targeting): self.targeting = Targeting(self, point);



	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def place_ships(self):
		self.ships.append(Ship.place_single_ship_randomly(Ship.SHIPS[len(self.ships)], self.ships));
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);


	# ————————————————————————————————————————————————————— GAME ————————————————————————————————————————————————————— #

	def turn(self):
		if(not self.ships_are_placed):
			self.place_ships();
			print("\tAI: Placed Ship at {}".format(str(self.ships[-1].location.points[0])));  #TESTING
		# Try to attack and prepare to be attacked
		else:
			if(not self.targeting): point = [randint(0,9), randint(0,9)];
			else: point = self.targeting.next_move();
			self.game.attack(point, self);
			# print("{} attacked at [{},{}]".format(self.name, point[0], point[1]));


	# ——————————————————————————————————————————————————  TARGETING —————————————————————————————————————————————————— #

	def direction(self):
		return [-1, 1][self._direction];



class User(Player):
	def __init__(self, game, player_id, name="User"):
		Player.__init__(self, game, player_id, name);


	# ————————————————————————————————————————————————————— GAME ————————————————————————————————————————————————————— #

	def is_my_turn(self):
		return self.game.is_players_turn(self);


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	def attack(self):
		print("PEW PEW");  #TESTING


	def turn(self):
		self.game.next_turn();


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def place_ships(self, point, orientation):
		ship = Ship.SHIPS[len(self.ships)];
		location = Location(orientation, ship["size"], point);
		if(not Location.valid_location(self.ships, points=location.points)): return None;  # ensure a ship can go here

		print("\tUser: Placed ship");  #TESTING
		self.ships.append(Ship(len(self.ships), ship["name"], ship["size"], location));
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);

		self.game.next_turn();
		return self.last_placed_ship();  # for reference by calling function
