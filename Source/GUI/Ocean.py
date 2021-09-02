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


from tkinter import Frame, Button, Label;
import platform;

from Global import *;
from Ship import Location, Ship;

if(is_mac()): from tkmacosx import Button;


def do_nothing(x, y):
	print("Nothing done at [{},{},{}]".format(x, y, z));



class Ocean(Frame):
	def __init__(self, board, field, game, player):
		Frame.__init__(self, field, bg=OCEAN_COLOR);
		self.board = board;
		self.buttons = [[] for x in range(FIELD_SIZE)];

		self.game = game;
		self.player = player;


	# ——————————————————————————————————————————————————— BUTTONS  ——————————————————————————————————————————————————— #

	def add_hover(self, enter, leave):
		[self.buttons[x][y].bind("<Enter>", enter([x,y])) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		[self.buttons[x][y].bind("<Leave>", leave([x,y])) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def assign_buttons(self, callback):
		button_points = [[x, y] for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		for point in button_points:  # button columns should be in order
			function = lambda_helper(callback, point);
			kwargs = {"master": self, "bg": OCEAN_COLOR, "text": OCEAN_CHAR, "fg": "white", "command": function};
			if(is_mac()): kwargs.update({"width": 25, "disabledbackground": OCEAN_COLOR, "disabledforeground": "white"})
			self.buttons[point[0]].append(Button(**kwargs));
			index(self.buttons, point).grid(row=point[0], column=point[1]);


	def change_button_color(self, point, color):
		index(self.buttons, point)["bg"] = color;


	def change_button_text(self, point, symbol):
		index(self.buttons, point)["text"] = symbol;


	# Gets all buttons specified as color.
	def colored_buttons(self, color):
		buttons = self.buttons;
		return [[x,y] for x in range(FIELD_SIZE) for y in range(FIELD_SIZE) if index(buttons, [x,y])["bg"] == color];


	def disable_button(self, point):
		index(self.buttons, point)["state"] = DISABLE;


	def disable_buttons(self):
		[self.buttons[x][y].config(state=DISABLE) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def enable_buttons(self):
		[self.buttons[x][y].config(state="normal") for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def redraw_field(self, ships):
		[self.change_button_color([x,y], OCEAN_COLOR) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		[self.change_button_text(point, OCEAN_CHAR) for ship in ships for point in ship.location.points];

		[self.change_button_text(point, SHIP_CHAR) for ship in ships for point in ship.location.points];
		self.redraw_ships();


	def redraw_ships(self):
		for ship in self.player.ships:
			for point in ship.location.points:
				self.change_button_color(point, Ocean.ship_point_color(point, ship));
				self.change_button_text(point, HIT_CHAR if(ship.is_hit(point)) else SHIP_CHAR);


	def update_buttom_command(self, callback, *args):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				self.buttons[x][y].config(command=lambda_helper(callback, [x,y], *args));


	# ———————————————————————————————————————————————————— STATIC ———————————————————————————————————————————————————— #

	@staticmethod
	def ship_point_color(point, ship):
		return {0: SHIP_COLOR, 1: HIT_COLOR}[ship.is_hit(point)];


	@staticmethod
	def highlight_color(location, ships):
		return {0: "red", 1: "green"}[Location.valid_location(ships, points=location.points)];


	@staticmethod
	def unhighlight_color(point, ships):
		return {0: OCEAN_COLOR, 1: SHIP_COLOR}[Location.any_ship_overlap(ships, points=[point])];



# Used by an AI Board & Field to display to user the move it makes
class AIOcean(Frame):
	def __init__(self, field):
		Frame.__init__(self, field);

		kwargs = {"text": OCEAN_CHAR, "bg": OCEAN_COLOR, "bd": 2, "relief": "solid", "padx": 4, "fg": "white"};
		self.squares = [[Label(self, **kwargs) for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];
		[[self.squares[x][y].grid(row=x, column=y) for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];


	def enable_buttons(self, callback=None):
		return


	def change_button_text(self, point, symbol):
		index(self.squares, point)["text"] = symbol;


	def change_button_color(self, point, color):
		index(self.squares, point)["bg"] = color;


	def redraw_ships(self):
		return;



class EnemyOcean(Ocean):
	def __init__(self, board, field, game, player):
		Ocean.__init__(self, board, field, game, player);
		self.assign_buttons(do_nothing);
		self.disable_buttons();


	def switch_orientation(self):
		print("AI: switch_orientation");



class PlayerOcean(Ocean):
	def __init__(self, board, field, game, player):
		Ocean.__init__(self, board, field, game, player);
		# GUI::
		# GUI::BUTTONS
		self.assign_buttons(self.place_ships);
		self.add_hover(self.highlight_ship, self.unhighlight_ship);
		self.orientation = False; # bool 0-horizontal, 1-vertical


	def enable_player_to_attack_enemy(self):
		self.board.enable_player_to_attack_enemy();


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def place_ships(self, point):
		ship = self.player.place_ships(point, self.orientation);
		if(not ship): return;  # invalid/unable to place ship. try again

		# update previous ship squares, then next ship squares
		[index(self.buttons, point).config(background=SHIP_COLOR, text=SHIP_CHAR) for point in ship.location.points];
		self.highlight_ship(point)(None);
		# Ship placing is complete: prepare for next phase by disabling buttons
		if(self.player.ships_are_placed): self.enable_player_to_attack_enemy();


	def switch_orientation(self):
		highlighted = self.colored_buttons("green") + self.colored_buttons("red");
		if(not highlighted): self.orientation ^= 1;
		else:
			self.unhighlight_ship(highlighted[0])(None);
			self.orientation ^= 1;
			self.highlight_ship(highlighted[0])(None);


	def highlight_ship(self, x_y):
		def function(e):
			if self.player.ships_are_placed: return;  # skip unnecessary work
			location = Location(self.orientation, Ship.SHIPS[len(self.player.ships)]["size"], x_y);
			color = Ocean.highlight_color(location, self.player.ships);
			[self.change_button_color(point, color) for point in location.usable_points()];

		return function;


	def unhighlight_ship(self, x_y):
		def function(e):
			if self.player.ships_are_placed: return;  # skip unnecessary work

			points = Location(self.orientation, Ship.SHIPS[len(self.player.ships)]["size"], x_y).usable_points();
			[self.change_button_color(point, Ocean.unhighlight_color(point, self.player.ships)) for point in points];

		return function;
