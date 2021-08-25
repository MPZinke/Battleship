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


	def is_hit(self, location):
		return any(ship.is_hit(location) for ship in self.ships);


	def place_ships(self):
		raise Exception("No function for placing ships in a child class");


	def print(self):
		for x in range(FIELD_SIZE):
			row = "";
			for y in range(FIELD_SIZE):
				value = 1;
				bools = [self.is_hit([x,y]), self.shots[x][y], self.is_hit([x,y]) and self.shots[x][y]];
				for x in range(len(bools)): value = bools[x] * (1 << x) + (not bools[x] * value);
				row += {1: OCEAN_CHAR_CLI, 2: SHIP_CHAR, 4: MISS_CHAR, 8: HIT_CHAR}[value];
			print(row);


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
		self.place_ships();


	def attack(self):
		self.game.enemy_board.print()  #TESTING
		# attack logic


	def place_ships(self):
		self.ships.append(Ship.place_single_ship_randomly(Ship.SHIPS[len(self.ships)], self.ships));
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);



class User(Player):
	def __init__(self, game, name="User"):
		Player.__init__(self, game, name);
		self.place_ships();  #TESTING


	def is_my_turn(self):
		return self.game.is_players_turn(self);


	def place_ship(self, x, y, orientation):
		print("X: {}, Y: {}, Z: {}".format(x, y, orientation))  #TESTING
		ship = Ship.SHIPS[len(self.ships)];
		self.ships.append(Ship(ship["id"], ship["name"], ship["size"], Location(orientation, ship["size"], [x,y])));
		if(len(self.ships) == len(Ship.SHIPS)):
			self.ships_are_placed = True;
			self.game.window.boards[self.game.player_number(self)].field.disable_field_buttons();



	def place_ships(self):
		self.print();  #TESTING
		self.ships_are_placed = len(self.ships) == len(Ship.SHIPS);
