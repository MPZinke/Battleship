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
from GUI.Board import AIBoard, UserBoard;


class Window(Tk):
	def __init__(self, game):
		Tk.__init__(self);
		self.title(WINDOW_TITLE);
		self.configure(background=WINDOW_BACKGROUND);
		self.geometry("1000x700");
		self.bind("<Tab>", self.switch_ship_placement_orientation);

		self.game = game;
		# A Window has 2 Boards (that switch for the current player)
		# A Board has two Fields, each of which has an Ocean and a Status display.
		players, boards = game.players, [UserBoard, AIBoard]  #SUGAR
		self.boards = [boards[players[x].is_AI](self, game, players[x], players[not x]) for x in range(2)];
		# self.boards[1].grid(row=0, column=0);
		# self.boards[1].grid_remove();
		self.boards[0].grid(row=0, column=0);


	def switch_boards(self):
		print("WINDOW::SWITCH_BOARDS")
		player_number = self.game.player_number_for_turn();
		self.boards[player_number].grid_remove();
		self.boards[not player_number].grid();


	def switch_ship_placement_orientation(self, e):
		self.boards[self.game.player_number_for_turn()].field.switch_orientation();


	def update_player_field(self, player_number, location, character):
		self.boards[player_number].update_field(location, character);


	def update_player_ships(self, player_number, ship_name, ship_point, character):
		self.board[player_number].update_ship_point(ship_name, ship_point);
