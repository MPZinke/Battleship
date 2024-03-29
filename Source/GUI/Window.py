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
import platform;

from Global import *;
from GUI.Board import AIBoard, UserBoard;


class Window(Tk):
	def __init__(self, game):
		Tk.__init__(self);
		self.title(WINDOW_TITLE);
		self.configure(background=WINDOW_BACKGROUND);
		self.geometry("1000x700");
		self.bind("<Tab>", self.switch_ship_placement_orientation);

		# A Window has 2 Boards (that switch for the current player)
		# A Board has two Fields, each of which has an Ocean and a Status display.
		self.current_board_number = game.current_player_number;  # keep things in sync
		players, boards = game.players, [UserBoard, AIBoard]  #SUGAR
		self.boards = [boards[players[x].is_AI](self, game, players[x], players[not x]) for x in range(len(players))];
		[self.boards[x].grid(row=x, column=0) for x in range(len(self.boards))];
		self.switch_boards(self.current_board_number);

		self.game = game;
		
		if(game.player_for_turn().is_AI): self.after(1000, game.next_turn);  # start the first turn


	# ———————————————————————————————————————————————— UPDATE  WINDOW ———————————————————————————————————————————————— #

	def mark_players_ship_as_sunk(self, player, ship_id):
		[board.mark_players_ship_as_sunk(player, ship_id) for board in self.boards];


	# Works for 2+ players.
	def switch_boards(self, player_number):
		[getattr(self.boards[x], "grid" if x == player_number else "grid_remove")() for x in range(len(self.boards))];
		self.current_board_number = player_number;


	# Player is the one who shot and hit someone.
	def update_hit(self, point, player, ship_id, hit_index):
		[board.update_hit_on_board(point, player, ship_id, hit_index) for board in self.boards];


	def update_miss(self, player_number, point):
		self.boards[not player_number].update_player_ocean(point, char=MISS_CHAR);
		self.boards[player_number].update_enemy_ocean(point, char=MISS_CHAR)


	# ——————————————————————————————————————————————————— GETTERS  ——————————————————————————————————————————————————— #

	def current_board(self):
		return self.boards[self.player_number_for_turn()];


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def switch_ship_placement_orientation(self, e):
		self.boards[self.current_board_number].switch_orientation();
