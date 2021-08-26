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
	def __init__(self, parent, game, player):
		Frame.__init__(self, parent, bg="orange");

		self.player = player;
		self.label = Label(self, text=self.player.name);
		self.label.grid(row=0, column=0, columnspan=2);


	def grid_ocean_and_ship_statuses(self):
		print("FIELD::GRIDDING")
		self.ocean.grid(row=1, column=0);
		self.status.grid(row=1, column=1);



# AI Field is display only...you just get to watch
class AIField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);

		self.ocean = AIOcean(self);
		self.status = [EnemyStatus, PlayerStatus][game.player_for_turn() == player](self, player);
		self.grid_ocean_and_ship_statuses();



class EnemyField(Field):
	def __init__(self, parent, game, enemy):
		Field.__init__(self, parent, game, enemy);

		self.ocean = EnemyOcean(self, game, enemy);
		self.status = EnemyStatus(self, enemy);
		self.grid_ocean_and_ship_statuses();



class PlayerField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);

		self.ocean = PlayerOcean(self, game, player);
		self.status = PlayerStatus(self, player);
		self.grid_ocean_and_ship_statuses();
