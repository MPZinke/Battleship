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
		self.sunk_enemy_ship_ids = [];  # IDs of enemy's ships that have been sunk
		self.player_shots = [[self.game.UNKNOWN for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];
		self.enemy_shots = [[False for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];  # places opponent has shot


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def last_placed_ship(self):
		return self.ships[-1] if self.ships else None;


	def place_ships(self, point, orientation):
		raise Exception("No function for Player::place_ships defined in a child class");


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	# Return if a shot hits a ship.
	def hits_a_ship(self, point):
		return any(ship.hits_ship(point) for ship in self.ships);


	# Function called when attacking another player.
	# Player is SHOOTing opponent.
	def shoot_at_enemy(self, point, shot_ship=None):
		self.player_shots[point[0]][point[1]] = self.game.HIT if shot_ship else self.game.MISS;


	# Function called when a player is being attacked by the other player.
	# Player is being SHOT by opponent.
	def shot(self, point):
		self.enemy_shots[point[0]][point[1]] = True;
		shot_ship = [ship for ship in self.ships if ship.shot(point)];
		return shot_ship[0] if(shot_ship) else None;


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
		if(self.targeting): attack_point = self.targeting.next_move();
		if(not self.targeting or not attack_point):
			#TODO: implement probablility points
			#TESTING
			for x in range(0xFFFF):
				if(x == 0xFFFE): raise Exception("MinAI::attack:attack_point: OVERFLOW");
				attack_point = [randint(0, FIELD_SIZE-1), randint(0, FIELD_SIZE-1)];
				if(index(self.player_shots, attack_point) == self.game.UNKNOWN): break;

		shot_ship = self.game.attack(attack_point, self);
		self.record_previous_move(attack_point, shot_ship);


	def record_previous_move(self, point, shot_ship):
		self.player_shots[point[0]][point[1]] = self.game.HIT if shot_ship else self.game.MISS;
		if(shot_ship):
			if(not self.targeting): self.targeting = Targeting(self.game, self, point);
			if(shot_ship.is_sunk()): self.sunk_enemy_ship_ids.append(shot_ship.id);


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def place_ships(self):
		self.ships.append(Ship.place_single_ship_randomly(Ship.SHIPS[len(self.ships)], self.ships));
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);


	# ————————————————————————————————————————————————————— GAME ————————————————————————————————————————————————————— #

	def turn(self):
		# Try to attack and prepare to be attacked
		if(self.ships_are_placed): self.attack();
		else:
			self.place_ships();
			print("\tAI: Placed Ship at {}".format(str(self.ships[-1].location.points[0])));  #TESTING

###

			# if(not self.targeting): point = [randint(0,9), randint(0,9)];
			# else: point = self.targeting.next_move();
			# self.game.attack(point, self);
			# print("{} attacked at [{},{}]".format(self.name, point[0], point[1]));
###


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
