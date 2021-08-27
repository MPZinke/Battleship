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


from Global import *

from Ships import Location, Ship;


class Player:
	def __init__(self, game, name, **kwargs):
		self.game = game;

		self.is_AI = kwargs.get("is_AI", False);
		self.ships_are_placed = False;  # whether the ships for the player have been placed
		self.name = name;
		self.ships = [];
		self.shots = [[False] * FIELD_SIZE] * FIELD_SIZE;  # places opponent has shot


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	def is_hit(self, location):
		return any(ship.is_hit(location) for ship in self.ships);


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def last_placed_ship(self):
		return self.ships[-1] if self.ships else None;


	def place_ships(self, x, y, orientation):
		raise Exception("No function for Player::place_ships defined in a child class");


	def print(self):
		for x in range(FIELD_SIZE):
			row = "";
			for y in range(FIELD_SIZE):
				value = 1;
				bools = [self.is_hit([x,y]), self.shots[x][y], self.is_hit([x,y]) and self.shots[x][y]];
				for x in range(len(bools)): value = bools[x] * (1 << x) + (not bools[x] * value);
				row += {1: OCEAN_CHAR_CLI, 2: SHIP_CHAR, 4: MISS_CHAR, 8: HIT_CHAR}[value];
			print(row);


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	# Function called when attacking another player.
	def shoot(self, location):
		if(self.shots[location[0]][location[1]]): raise AlreadyShot(location);
		self.game.attack(self, location);


	# Function called when a player is being attacked by the other player.
	def shot(self, location):
		if(self.is_hit(location)):
			ship = [ship for ship in self.ships if ship.is_hit(location)][0];
			ship.hit(location);
			self.game.update_player_board(player, location, True);
			self.game.update_player_ship(player, ship);



class AI(Player):
	def __init__(self, game, name="Enemy"):
		Player.__init__(self, game, name, is_AI=True);

		self.previous_shots = [];  # previous shots
		self.targeting = False;  # whether the enemy has found a ship and is tracking it


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	def attack(self):
		self.game.enemy_board.print()  #TESTING
		# attack logic


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def place_ships(self, x, y, orientation):
		self.ships.append(Ship.place_single_ship_randomly(Ship.SHIPS[len(self.ships)], self.ships));
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);


	# ————————————————————————————————————————————————————— GAME ————————————————————————————————————————————————————— #

	def turn(self):
		if(not self.ships_are_placed):
			print("\tAI: Placed Ship");  #TESTING
			self.place_ships(0, 0, 0);
		# Try to attack and prepare to be attacked
		else:
			print("ATTACK");



class User(Player):
	def __init__(self, game, name="User"):
		Player.__init__(self, game, name);


	# ————————————————————————————————————————————————————— GAME ————————————————————————————————————————————————————— #

	def is_my_turn(self):
		return self.game.is_players_turn(self);


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	def attack(self):
		print("PEW PEW");  #TESTING


	def turn(self):
		self.game.next_turn();


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def place_ships(self, x, y, orientation):
		print("\tUser: Placed ship");  #TESTING
		ship = Ship.SHIPS[len(self.ships)];
		self.ships.append(Ship(ship["id"], ship["name"], ship["size"], Location(orientation, ship["size"], [x,y])));
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);

		self.game.next_turn();
		return self.last_placed_ship();  # for reference by calling function
