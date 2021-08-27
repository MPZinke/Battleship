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
		Frame.__init__(self, window, bg="white", bd=16);
		self.window = window;  # parent in this case
		self.fields = None;
		self.enemy_field = None;
		self.player_field = None;

		self.game = game;
		self.player = player;
		self.opponent = opponent;
		self.orientation = False;


	def switch_orientation(self):
		raise Exception("No function for Board::switch_orientation defined in a child class");



class AIBoard(Board):
	def __init__(self, window, game, ai, opponent):
		Board.__init__(self, window, game, ai, opponent);
		self.fields = [AIField(self, game, opponent), AIField(self, game, ai)];
		[self.fields[x].grid(row=x, column=0) for x in range(len(self.fields))];

		self.enemy_field, self.player_field = self.fields;  #SUGAR


	def switch_orientation(self):
		return;



class UserBoard(Board):
	def __init__(self, window, game, user, opponent):
		Board.__init__(self, window, game, user, opponent);
		self.fields = [EnemyField(self, game, opponent), PlayerField(self, game, user)];
		[self.fields[x].grid(row=x, column=0) for x in range(len(self.fields))];

		self.enemy_field, self.player_field = self.fields;  #SUGAR


	def switch_orientation(self):
		self.player_field.ocean.switch_orientation();
