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


from tkinter import Frame, Button;

from Global import *;
from Ships import Location, Ship;


def do_nothing(x, y, z):
	print("Nothing done at [{},{},{}]".format(x, y, z));


class Field(Frame):
	def __init__(self, parent, game, player):
		Frame.__init__(self, parent, bg="red");
		self.parent = parent;
		self.buttons = [[] for x in range(FIELD_SIZE)];

		self.game = game;
		self.player = player;
		self.orientation = False;


	def switch_orientation(self):
		self.orientation ^= 1;



	# ——————————————————————————————————————————————————— BUTTONS  ——————————————————————————————————————————————————— #

	def add_hover(self, enter, leave):
		[self.buttons[x][y].bind("<Enter>", enter(x, y)) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		[self.buttons[x][y].bind("<Leave>", leave(x, y)) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def assign_buttons(self):
		button_points = [[x, y] for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		for point in button_points:  # button columns should be in order
			function = lambda x=point[0],y=point[1]: self.callback(x,y,self.orientation);
			args = {"master": self, "bg": "blue", "foreground": "white", "text": "  ", "command": function};
			self.buttons[point[0]].append(Button(**args));
			index(self.buttons, point).grid(row=point[0], column=point[1]);


	def add_ships_to_field(self, ships):
		[index(self.buttons, point).config(text=SHIP_CHAR) for ship in ships for point in ship.location.points];


	def change_button_symbol(self, location, symbol):
		index(self.buttons, location)["text"] = symbol;


	def disable_button(self, x, y):
		self.buttons[x][y]["state"] = "disable"


	def disable_field_buttons(self):
		[self.buttons[x][y].config(state="disable") for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def enable_field_buttons(self):
		[self.buttons[x][y].config(state="normal") for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];



class AIField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);
		self.callback = do_nothing;
		self.assign_buttons();
		self.disable_field_buttons();



class UserField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);
		# GUI::
		# GUI::BUTTONS
		self.callback = player.place_ship;
		self.assign_buttons();
		self.add_hover(self.highlight_ship, self.unhighlight_ship)


	def highlight_ship(self, x, y):
		def function(e):
			if self.player.ships_are_placed: return;
			points = Location(self.orientation, Ship.SHIPS[len(self.player.ships)]["size"], [x,y]).points;
			color = "yellow" if Location.points_are_in_range(points=points) else "red";
			[index(self.buttons, point).config(background=color) for point in Location.usable_points(points)];
		return function


	def unhighlight_ship(self, x, y):
		def function(e):
			if self.player.ships_are_placed: return;
			points = Location(self.orientation, Ship.SHIPS[len(self.player.ships)]["size"], [x,y]).points;
			[index(self.buttons, point).config(background="blue") for point in Location.usable_points(points)];
		return function
