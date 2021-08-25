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
from Board import AIBoard, UserBoard;


class Window(Tk):
	def __init__(self, game):
		Tk.__init__(self);
		self.title(WINDOW_TITLE);
		self.configure(background=WINDOW_BACKGROUND);
		self.geometry("1000x700");
		self.bind("<Tab>", self.switch_ship_placement_orientation);

		self.game = game;

		# A Window has 2 Boards, which each have a Field and an Status display.
		self.boards = [[UserBoard, AIBoard][player.is_AI](self, game, player) for player in self.game.players];
		for x in range(len(self.boards)): self.boards[x].grid(row=x, column=0);


	def switch_ship_placement_orientation(self, e):
		self.boards[self.game.player_number_for_turn()].field.switch_orientation();


	def update_player_field(self, player_number, location, character):
		self.boards[player_number].update_field(location, character);


	def update_player_ships(self, player_number, ship_name, ship_point, character):
		self.board[player_number].update_ship_point(ship_name, ship_point);
