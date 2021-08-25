

from tkinter import *
from random import randint

from Global import *
from Field import *
from Data import *
from Ships import *


# shows player & data
class Board(Frame):
	def __init__(self, window, game, player):
		# GUI
		Frame.__init__(self, window, bg="white", bd=16);
		self.window = window;

		self.game = game;
		self.player = player;

		self.data = Data(self);
		self.data.grid(row=0, column=1);

		# game
		self.ships = []
		self.shots = [[False] * FIELD_SIZE] * FIELD_SIZE


	def add_hover(self, enter, leave):
		for x in range(len(self.field.buttons)):
			for y in range(len(self.field.buttons[x])):
				self.field.buttons[x][y].bind("<Enter>", enter(x, y))
				self.field.buttons[x][y].bind("<Leave>", leave(x, y))


	def set_field(self, field, callback):
		self.field = field(self, callback)
		self.field.grid(row=0, column=0)


	def print(self):
		for row in self.field.buttons:
			print(" ".join([column.text for column in row]))


	# ———————————————————————————————————————————————— SHIP PLACEMENT ———————————————————————————————————————————————— #

	def any_ship_in_range(self, start, size):
		for x in range(size):
			location = [start[0], start[1]+x] if self.field.orientation else [start[0]+x, start[1]]
			for y in range(len(self.ships)):
				for z in range(len(self.ships[y].location.points)):
					if location == self.ships[y].location.points[z]: return True
		return False


	def points_in_range(self, start, size):
		points = []
		for x in range(size):
			if (start[1] + x < FIELD_SIZE and self.field.orientation) or (start[0] + x < FIELD_SIZE and not self.field.orientation):
				points.append([start[0], start[1]+x] if self.field.orientation else [start[0]+x, start[1]])
		return points


class UserBoard(Board):
	def __init__(self, window, game, player):
		Board.__init__(self, window, game, player)
		self.set_field(PlayerField, self.place_ship)

		self.add_hover(self.field.highlight_ship, self.field.unhighlight_ship)


	# ——————————————————— SHIP PLACEMENT ———————————————————

	def place_ship(self, x, y):
		ship = Ship.SHIPS[len(self.ships)];
		location = Location(self.field.orientation, ship["size"], [x, y]);
		points = location.points;

		# If spot is invalid: turn buttons red
		if(not Location.points_are_in_range(points) or Location.any_ship_overlap(self.ships, points=points)):
			for x in range(len(points)): self.field.buttons[points[x][0]][points[x][1]]["background"] = "red";

		# Otherwise, spot is valid
		else:
			# check placement before proceeding
			self.field.unhighlight_ship(x, y)(None)

			self.ships.append(Ship(ship["id"], ship["name"], ship["size"], location));
			self.field.add_ships_to_field(self.ships)

			if(len(self.ships) == len(Ship.SHIPS)): self.field.end_ship_placement()



class AIBoard(Board):
	def __init__(self, window, game, player):
		Board.__init__(self, window, game, player)
		self.set_field(Field, self.player_attack)

		self.place_ships_randomly()


	def player_attack(self, x, y):
		if self.game.enemy.is_hit([x, y]): self.game.enemy_board.change_button_symbol([x, y], HIT_CHAR)
		else: self.game.enemy_board.change_button_symbol([x, y], MISS_CHAR)

