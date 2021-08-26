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
from Ships import Ship;


class ShipStatus:
	def __init__(self, parent, ship):
		self.id = ship["id"];
		self.name = ship["name"];
		self.size = ship["size"];

		self.parent = parent;
		self.name_label = Label(parent, text=ship["name"]);
		self.hits_label = Label(parent, text="".join([MISS_CHAR for x in range(self.size)]));


	def grid_name(self, x):
		self.name_label.grid(row=x, column=0);


	def grid_hits(self, x):
		self.hits_label.grid(row=x, column=1);



class Status(Frame):
	def __init__(self, parent, player):
		Frame.__init__(self, parent);
		self.parent = parent;
		self.player = player;
		self.ship_statuses = {ship["id"]: ShipStatus(self, ship) for ship in Ship.SHIPS};


	def grid_ship_names(self):
		[self.ship_statuses[ship_id].grid_name(x) for x, ship_id in enumerate(self.ship_statuses)];



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
		[self.ship_statuses[ship_id].grid_hits(x) for x, ship_id in enumerate(self.ship_statuses)];
