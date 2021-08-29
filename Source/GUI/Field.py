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


from tkinter import Frame, Label;

from Global import *;
from GUI.Ocean import AIOcean, EnemyOcean, PlayerOcean;
from GUI.Status import EnemyStatus, PlayerStatus;



class Field(Frame):
	def __init__(self, board, game, player):
		Frame.__init__(self, board, bg=WINDOW_BACKGROUND, highlightbackground="white", highlightthickness=2);
		self.board = board;
		self.label = Label(self, text=player.name, bg=WINDOW_BACKGROUND, fg="white");
		self.label.grid(row=0, column=0, columnspan=2);

		self.game = game;
		self.player = player;


	def grid_ocean_and_ship_statuses(self):
		self.ocean.grid(row=1, column=0);
		self.status.grid(row=1, column=1);


	def enable_ocean_buttons(self, callback=None):
		self.ocean.enable_buttons(callback);


	def update_status(self, point, ship_id, hit_index):
		self.status.mark_ship_as_hit(ship_id, hit_index);


	def update_ocean(self, point, char):
		self.ocean.change_button_text(point, char);



# AI Field is display only...you just get to watch
class AIField(Field):
	def __init__(self, board, game, player):
		Field.__init__(self, board, game, player);

		self.ocean = AIOcean(self);
		self.status = [EnemyStatus, PlayerStatus][game.player_for_turn() == player](self, player);
		self.grid_ocean_and_ship_statuses();



class EnemyField(Field):
	def __init__(self, board, game, enemy):
		Field.__init__(self, board, game, enemy);

		self.ocean = EnemyOcean(board, self, game, enemy);
		self.status = EnemyStatus(self, enemy);
		self.grid_ocean_and_ship_statuses();


	# Attacking through the GUI will always be done by a User, so this function will always be called to increment by
	#  the User.
	def enable_attacking(self, player):
		self.ocean.enable_buttons();
		self.ocean.update_buttom_command(self.attack_and_increment_function_pointer(player));
		print("attacking enabled")


	# Creates a function pointer for calling the Game::attack function for a player.
	def attack_and_increment_function_pointer(self, player):
		def attack_function(point):
			self.game.attack(point, player);
			self.game.next_turn();
		return attack_function;



class PlayerField(Field):
	def __init__(self, board, game, player):
		Field.__init__(self, board, game, player);

		self.ocean = PlayerOcean(board, self, game, player);
		self.status = PlayerStatus(self, player);
		self.grid_ocean_and_ship_statuses();
