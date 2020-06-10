

from tkinter import *
from random import randint

from Global import *
from Field import *
from Data import *
from Ships import *


# shows player & data
class Board(Frame):
	def __init__(self, tk, game):
		# GUI
		Frame.__init__(self, tk, bg="white", bd=16)
		self.game = game
		self.data = Data(self)
		self.data.grid(row=0, column=1)

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


	# ——————————————————— SHIP PLACEMENT ———————————————————

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





class PlayerBoard(Board):
	def __init__(self, tk, game):
		Board.__init__(self, tk, game)
		self.set_field(PlayerField, self.place_ship)

		self.add_hover(self.field.highlight_ship, self.field.unhighlight_ship)


	# ——————————————————— SHIP PLACEMENT ———————————————————

	def place_ship(self, x, y):
		ship_index = len(self.ships)
		points = self.points_in_range([x, y], SHIP_SIZES[ship_index])
		# check if spot invalid
		if(any(point in points for ship in self.ships for point in ship.location.points)) \
		or len(points) != SHIP_SIZES[ship_index]:
			for i in range(len(points)):
				self.field.buttons[points[i][0]][points[i][1]]["background"] = "red"

		# spot is valid
		else:
			# check placement before proceeding
			self.field.unhighlight_ship(x, y)(None)

			self.ships.append(Ship(SHIP_NAMES[ship_index], SHIP_SIZES[ship_index]))
			self.ships[-1].location = Location(self.field.orientation, SHIP_SIZES[ship_index], [x, y])
			self.field.add_ships_to_field(self.ships)

			if ship_index+1 == len(SHIP_SIZES): self.field.end_ship_placement()



class EnemyBoard(Board):
	def __init__(self, tk, game):
		Board.__init__(self, tk, game)
		self.set_field(Field, self.player_attack)

		self.place_ships_randomly()


	def player_attack(self, x, y):
		if self.game.enemy_board.is_hit([x, y]): self.game.enemy_board.change_button_symbol([x, y], HIT_CHAR)
		else: self.game.enemy_board.change_button_symbol([x, y], MISS_CHAR)


	# ——————————————————— SHIP PLACEMENT ———————————————————

	def random_location(self, size):
		self.field.orientation = randint(0, 1)
		max_size = FIELD_SIZE - 1
		return [randint(0, max_size - size * (1 - self.field.orientation)), randint(0, max_size - size * self.field.orientation)]


	def place_ships_randomly(self):
		for x in range(len(SHIP_SIZES)):
			start = self.random_location(SHIP_SIZES[x])

			while self.any_ship_in_range(start, SHIP_SIZES[x]): start = self.random_location(SHIP_SIZES[x])
			self.ships.append(Ship(SHIP_NAMES[x], SHIP_SIZES[x]))
			self.ships[x].location = Location(self.field.orientation, SHIP_SIZES[x], start)

