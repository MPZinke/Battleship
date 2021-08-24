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


def do_nothing(x, y):
	print("Nothing done at [{},{}]".format(x, y));


class Field(Frame):
	def __init__(self, parent, game, player):
		Frame.__init__(self, parent, bg="red");
		self.parent = parent;
		self.buttons = [[] for x in range(FIELD_SIZE)];

		self.game = game;
		self.player = player;


	# ——————————————————————————————————————————————————— BUTTONS  ——————————————————————————————————————————————————— #

	def assign_buttons(self):
		button_points = [[x, y] for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		for point in button_points:  # button columns should be in order
			function = lambda x=point[0],y=point[1]: self.callback(x,y);
			args = {"master": self, "bg": "blue", "foreground": "white", "text": "  ", "command": function};
			self.buttons[point[0]].append(Button(**args));
			index(self.buttons, point).grid(row=point[0], column=point[1]);


	def add_ships_to_field(self, ships):
		[index(self.buttons, point)config(text=SHIP_CHAR) for ship in ships for point in ship.location.points];


	def change_button_symbol(self, location, symbol):
		index(self.buttons, location)["text"] = symbol;


	def disable_button(self, x, y):
		self.buttons[x][y]["state"] = "disable"


	def disable_field_buttons(self):
		[self.buttons[x][y].config(state="disable") for x in range(FIELD_SIZE) for x in range(FIELD_SIZE)];


	def enable_field_buttons(self):
		[self.buttons[x][y].config(state="normal") for x in range(FIELD_SIZE) for x in range(FIELD_SIZE)];



class AIField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);
		self.callback = do_nothing;
		self.assign_buttons();



class UserField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);
		self.orientation = False;
		self.parent.window.bind("<Tab>", self.switch_orientation);

		self.callback = player.place_ship;
		self.assign_buttons();


	def switch_orientation(self):
		self.orientation ^= 1;


	def highlight_ship(self, x, y):
		def function(e):
			if not self.game.select_ships: return
			points = self.points_in_range([x, y], SHIP_SIZES[len(self.parent.ships)])
			color = "yellow" if len(points) == SHIP_SIZES[len(self.parent.ships)] else "red"
			for i in range(len(points)):
			[index(self.buttons, points[i]).confi(background=color) for i in range(len(points))];
				self.buttons[points[i][0]][points[i][1]]["background"] = color
		return function


	def unhighlight_ship(self, x, y):
		def function(e):
			if not self.game.select_ships: return
			points = self.points_in_range([x, y], SHIP_SIZES[len(self.parent.ships)])
			for i in range(len(points)):
				self.buttons[points[i][0]][points[i][1]]["background"] = "blue"
		return function

