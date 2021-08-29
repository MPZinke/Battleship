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


from tkinter import *;

from Global import *;
from GUI.Field import *;


# shows player & data
class Board(Frame):
	def __init__(self, window, game, player, opponent):
		# GUI
		Frame.__init__(self, window, bg=WINDOW_BACKGROUND, bd=16);
		self.window = window;  # parent in this case
		self.fields = None;
		self.enemy_field = None;  # first (top) field assuming this is my board
		self.player_field = None;  # second (bottom) field assuming this is my board

		self.game = game;
		self.player = player;
		self.opponent = opponent;
		self.orientation = False;


	def field_for_opponent(self, opponent):
		return self.fields[self.opponent == opponent];


	# Return the field for the specified player.
	def field_for_player(self, player):
		return self.fields[self.player == player];


	def switch_orientation(self):
		raise Exception("No function for Board::switch_orientation defined in a child class");


	# The player has hit their opponent. Update the player's board to reflect it.
	# Takes the point to update, the player that made the hit
	def update_hit_on_board(self, point, player, ship_id, hit_index):
		field = self.field_for_opponent(player);  # player attacked opponent's field; update opponent
		field.update_ocean(point, char=HIT_CHAR, color=HIT_COLOR);
		field.update_status(point, ship_id, hit_index);


	def update_enemy_ocean(self, point, **kwargs):
		self.enemy_field.update_ocean(point, **kwargs);


	def update_player_ocean(self, point, **kwargs):
		self.player_field.update_ocean(point, **kwargs);



class AIBoard(Board):
	def __init__(self, window, game, ai, opponent):
		Board.__init__(self, window, game, ai, opponent);
		self.fields = [AIField(self, game, opponent), AIField(self, game, ai)];
		# [self.fields[x].grid(row=x, column=0) for x in range(len(self.fields))];
		self.fields[0].grid(row=0, column=0, sticky="W")
		self.fields[1].grid(row=1, column=0, sticky="W")

		self.enemy_field, self.player_field = self.fields;  #SUGAR


	def switch_orientation(self):
		return;



class UserBoard(Board):
	def __init__(self, window, game, user, opponent):
		Board.__init__(self, window, game, user, opponent);
		self.fields = [EnemyField(self, game, opponent), PlayerField(self, game, user)];
		# [self.fields[x].grid(row=x, column=0) for x in range(len(self.fields))];
		self.fields[0].grid(row=0, column=0, sticky="W")
		self.fields[1].grid(row=1, column=0, sticky="W")

		self.enemy_field = self.fields[0];  #SUGAR
		self.player_field = self.fields[1];  #SUGAR


	def enable_player_to_attack_enemy(self):
		self.player_field.ocean.disable_buttons();  # don't allow player to place ships anymore
		self.enemy_field.enable_attacking(self.player);


	def switch_orientation(self):
		self.player_field.ocean.switch_orientation();
