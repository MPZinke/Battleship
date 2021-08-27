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


from time import sleep;

from Player import AI, User;
from GUI.Window import Window;


class Game:
	def __init__(self):
		# Players in the game
		self.players = [AI(self, "AI"), User(self, "MPZinke")];  # this is where it is defined whether single or multiplayer
		self.enemy = self.players[0];  # Sugar
		self.user = self.players[1];  # Sugar

		self.is_ship_placement = True;  # whether the current goal of the game is to place ships (Ship Placement Simulator)
		self.is_won = False;  # whether the game is finished/won
		self.turn_count = 0;
		self.winner = None;

		# A Game has a Window which has 2 Boards, which each have a Field and an Status display.
		self.window = Window(self);
		# Let the games begin
		# self.next_turn();


	# ——————————————————————————————————————————————————  ATTACKING —————————————————————————————————————————————————— #

	# Calls the attack method for a player.
	# PARAMS: The player who is attacking, the location they are attacking.
	def attack(self, player, location):
		attacker = player;
		defender = self.opposing_player_for_player(player);

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


	def next_turn(self):
		attacker = self.player_for_turn();
		defender = self.opposing_player_for_turn();
		
		# If user just went, play for them
		if(not attacker.is_AI):
			print("Turn: {}\n\tPlayer: {}".format(self.turn_count, attacker.name));  #TESTING
			self.turn_count += 1;
			attacker, defender = defender, attacker;
			self.window.switch_boards();

		# If next player is AI, let them move
		while(attacker.is_AI and self.turn_count < 0xFFFF):
			sleep(1);  # to give that authentic player experience
			print("Turn: {}\n\tPlayer: {}".format(self.turn_count, attacker.name));  #TESTING
			attacker.turn();
			self.turn_count += 1;
			attacker, defender = defender, attacker;
			self.window.switch_boards();
			sleep(1);  # to give that authentic player experience


	def is_over(self):
		for x in range(len(self.players)):
			if all(ship.is_sunk() for ship in self.players[x].ships):
				self.is_won = True
				return True
		return False


	def is_players_turn(self, player):
		return player == self.players[self.turn_count & 1];


	# ———————————————————————————————————————————————————  GETTERS ——————————————————————————————————————————————————— #

	# Returns the opposing (other) player for the current turn. (EG if it's my turn, it returns my enemy).
	def opposing_player_for_turn(self):
		return self.players[not (self.turn_count & 1)];


	# Returns the opposing (other) player for the . (EG if it's my turn, it returns my enemy).
	def opposing_player_for_player(self, player):
		return self.players[player != self.players[1]];


	# Returns the opposing (other) player's number for the current turn. 
	# (EG if it's my turn, it returns my enemy's index).
	def opposing_player_number_for_turn(self):
		return not (self.turn_count & 1);


	# Returns the player number for the current turn. (EG if it's my turn, it returns my opponents index).
	def opposing_player_number(self, player):
		return player != self.players[1];


	# Returns the player for the current turn. (EG if it's my turn, it returns me).
	def player_for_turn(self):
		return self.players[self.turn_count & 1];


	# Returns the index of a player within the players list.
	def player_number(self, player):
		return player == self.players[1];


	# Returns the player number for the current turn. (EG if it's my turn, it returns my index).
	def player_number_for_turn(self):
		return self.turn_count & 1;
