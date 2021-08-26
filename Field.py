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
import platform;
if(platform.system() == "Darwin"): from tkmacosx import Button;

from Global import *;
from Ships import Location, Ship;


def do_nothing(x, y):
	print("Nothing done at [{},{},{}]".format(x, y, z));


class Field(Frame):
	def __init__(self, parent, game, player):
		Frame.__init__(self, parent, bg="red");
		self.parent = parent;
		self.buttons = [[] for x in range(FIELD_SIZE)];

		self.game = game;
		self.player = player;
		self.orientation = False;


	# ——————————————————————————————————————————————————— BUTTONS  ——————————————————————————————————————————————————— #

	def add_hover(self, enter, leave):
		[self.buttons[x][y].bind("<Enter>", enter(x, y)) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		[self.buttons[x][y].bind("<Leave>", leave(x, y)) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def assign_buttons(self):
		button_points = [[x, y] for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		for point in button_points:  # button columns should be in order
			function = lambda x=point[0],y=point[1]: self.callback(x,y);
			self.buttons[point[0]].append(Button(master=self, bg=WATER_CLR, text=OCEAN_CHAR, command=function));
			index(self.buttons, point).grid(row=point[0], column=point[1]);


	def change_button_color(self, location, symbol):
		index(self.buttons, location)["background"] = symbol;


	def change_button_text(self, location, symbol):
		index(self.buttons, location)["text"] = symbol;


	def disable_button(self, x, y):
		self.buttons[x][y]["state"] = "disabled" if(platform.system() == "Darwin") else "disable";


	def disable_field_buttons(self):
		state = "disabled" if(platform.system() == "Darwin") else "disable";
		[self.buttons[x][y].config(state=state) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	def enable_field_buttons(self):
		[self.buttons[x][y].config(state="normal") for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];


	# Gets all buttons specified as color.
	def colored_buttons(self, color):
		buttons = self.buttons;
		return [[x,y] for x in range(FIELD_SIZE) for y in range(FIELD_SIZE) if index(buttons, [x,y])["bg"] == color];


	def redraw_field(self, ships):
		[self.change_button_color([x,y], WATER_CLR) for x in range(FIELD_SIZE) for y in range(FIELD_SIZE)];
		[self.change_button_text(point, OCEAN_CHAR) for ship in ships for point in ship.location.points];

		[self.change_button_text(point, SHIP_CHAR) for ship in ships for point in ship.location.points];
		for ship in self.player.ships:
			for point in ship.location.points:
				char, color = [[SHIP_CHAR, SHIP_CLR], [HIT_CHAR, HIT_CLR]][ship.is_hit(point)];
				self.change_button_text(point, char);
				self.change_button_color(point, color);



class AIField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);
		self.callback = do_nothing;
		self.assign_buttons();
		self.disable_field_buttons();


	def switch_orientation(self):
		print("AI: switch_orientation");



class UserField(Field):
	def __init__(self, parent, game, player):
		Field.__init__(self, parent, game, player);
		# GUI::
		# GUI::BUTTONS
		self.callback = self.place_ships
		self.assign_buttons();
		self.add_hover(self.highlight_ship, self.unhighlight_ship)


	def place_ships(self, x, y):
		ship = self.player.place_ships(x, y, self.orientation);

		# update previous ship squares, then next ship squares
		[index(self.buttons, point).config(background=SHIP_CLR, text=SHIP_CHAR) for point in ship.location.points];
		self.highlight_ship(x, y)(None);
		# disable buttons if ship placing is complete
		if(self.player.ships_are_placed):
			self.disable_field_buttons();
			self.parent.window.boards[self.game.other_player_number(self.player)].field.enable_field_buttons();


	def switch_orientation(self):
		highlighted = self.colored_buttons("green") + self.colored_buttons("yellow") + self.colored_buttons("red");
		if(not highlighted): self.orientation ^= 1;
		else:
			self.unhighlight_ship(*(highlighted[0]))(None);
			self.orientation ^= 1;
			self.highlight_ship(*(highlighted[0]))(None);


	def highlight_ship(self, x, y):
		def function(e):
			if self.player.ships_are_placed: return;  # skip unnecessary work
			points = Location(self.orientation, Ship.SHIPS[len(self.player.ships)]["size"], [x,y]).points;

			points_are_in_range = Location.points_are_in_range(points=points);
			any_ship_overlap = Location.any_ship_overlap(self.player.ships, points=points);
			color = {0: "red", 1: "green"}[points_are_in_range and not any_ship_overlap];
			[self.change_button_color(point, color) for point in Location.usable_points(points)];

		return function


	def unhighlight_ship(self, x, y):
		def function(e):
			if self.player.ships_are_placed: return;  # skip unnecessary work

			points = Location(self.orientation, Ship.SHIPS[len(self.player.ships)]["size"], [x,y]).points;
			for point in Location.usable_points(points):
				color = {0: WATER_CLR, 1: SHIP_CLR}[Location.any_ship_overlap(self.player.ships, points=[point])];
				self.change_button_color(point, color);

		return function
