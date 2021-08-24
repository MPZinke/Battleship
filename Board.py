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
from Field import *;


# shows player & data
class Board(Frame):
	def __init__(self, window, game, player):
		# GUI
		Frame.__init__(self, window, bg="white", bd=16);
		self.window = window;  # parent in this case

		self.game = game;
		self.player = player;


class AIBoard(Board):
	def __init__(self, window, game, player):
		Board.__init__(self, window, game, player);
		self.field = AIField(self, game, player);
		self.field.grid(row=0, column=0);



class UserBoard(Board):
	def __init__(self, window, game, player):
		Board.__init__(self, window, game, player);
		self.field = UserField(self, game, player);
		self.field.grid(row=0, column=0);
