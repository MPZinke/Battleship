#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.26                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from tkinter import Frame, Label;

from Global import *;
from Ship import Ship;


class ShipStatus:
	def __init__(self, parent, ship, ship_id):
		self.id = ship_id;
		self.name = ship["name"];
		self.size = ship["size"];

		self.parent = parent;
		self.name_label = Label(parent, text=ship["name"], bg=WINDOW_BACKGROUND, fg="white");
		kwargs = {"master": parent, "text": MISS_CHAR, "bg": WINDOW_BACKGROUND, "fg": "white"};
		self.hits_labels= [Label(**kwargs) for x in range(self.size)];


	def grid_name(self, x):
		self.name_label.grid(row=x, column=0, sticky="W");


	def grid_hits(self, row):
		[self.hits_labels[x].grid(row=row, column=x+1, sticky="W") for x in range(len(self.hits_labels))];


	def mark_hit(self, index):
		self.hits_labels[index]["text"] = HIT_CHAR;



class Status(Frame):
	def __init__(self, parent, player):
		Frame.__init__(self, parent, bg=WINDOW_BACKGROUND);
		self.parent = parent;
		self.player = player;
		self.ship_statuses = [ShipStatus(self, ship, x) for x, ship in enumerate(Ship.SHIPS)];


	def grid_ship_names(self):
		[status.grid_name(x) for x, status in enumerate(self.ship_statuses)];


	def mark_ship_as_hit(self, ship_id, hit_index):
		self.ship_statuses[ship_id].mark_hit(hit_index);



class EnemyStatus(Status):
	def __init__(self, parent, enemy):
		Status.__init__(self, parent, enemy);

		self.grid_ship_names();



class PlayerStatus(Status):
	def __init__(self, parent, player):
		Status.__init__(self, parent, player);

		self.grid_ship_names();
		self.grid_ship_hits();


	def grid_ship_hits(self):
		[ship.grid_hits(x) for x, ship in enumerate(self.ship_statuses)];
