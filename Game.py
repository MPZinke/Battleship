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


from Player import AI, User;
from Window import Window;


class Game:
	def __init__(self):
		# Players in the game
		self.players = [AI(self), User(self)];  # this is where it is defined whether single or multiplayer
		self.enemy = self.players[0];  # Sugar
		self.user = self.players[1];  # Sugar

		self.is_ship_placement = True;  # whether the current goal of the game is to place ships (Ship Placement Simulator)
		self.is_won = False;  # whether the game is finished/won
		self.turn_count = 0;
		self.winner = None;

		# A Game has a Window which has 2 Boards, which each have a Field and an Status display.
		self.window = Window(self);


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	# Calls the attack method for a player.
	# PARAMS: The player who is attacking, the location they are attacking.
	def attack(self, player, location):
		attacker = self.player[self.player_number(player)];
		defender = self.player[not self.player_number(player)];

		attacker.shoot(location);
		defender.shot(location);


	# Updates a player field for an attack.
	def update_player_field(self, player, location, is_hit):
		player_number = self.player_number(player);
		self.window.update_field(player_number, location, HIT_CHAR if is_hit else MISS_CHAR);


	def update_player_ship(self, player, ship_id, ship_point, character):
		player_number = self.player_number(player);
		self.window.update_player_ship(player_number, ship_id, ship_point, character);


	# ————————————————————————————————————————————————————— GAME ————————————————————————————————————————————————————— #

	def mainloop(self):
		self.window.mainloop();


	def increment_turn(self):
		player = self.player_for_turn();
		other_player = self.other_player(player);
		if(self.is_ship_placement and player.ships_are_placed and other_player.ships_are_placed):
			self.is_ship_placement = False;
		if(other_player.is_AI): other_player.attack();  #TODO: build attack function
		self.turn_count += 1;


	def is_over(self):
		for x in range(len(self.players)):
			if all(ship.is_sunk() for ship in self.players[x].ships):
				self.is_won = True
				return True
		return False


	def is_players_turn(self, player):
		return player == self.players[self.turn_count & 1];


	def player_for_turn(self):
		return self.players[self.turn_count & 1];


	def player_number_for_turn(self):
		return self.turn_count & 1;


	# ———————————————————————————————————————————————————  GETTERS ——————————————————————————————————————————————————— #

	def other_player(self, player):
		return self.players[player != self.players[1]];


	def player_number(self, player):
		return player == self.players[1];
