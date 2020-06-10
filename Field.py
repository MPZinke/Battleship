

from tkinter import *

from tkinter import *

from Global import *


# shows attack field
class Field(Frame):
	def __init__(self, parent, callback):
		Frame.__init__(self, parent, bg="red")
		self.parent = parent
		self.game = parent.game

		self.orientation = False
		self.buttons = []
		for x in range(FIELD_SIZE):
			self.buttons.append([])
			for y in range(FIELD_SIZE):
				function = lambda x=x, y=y: callback(x, y)
				args = {"master": self, "bg": "blue", "foreground": "white", "text": " ", "command": function}
				self.buttons[x].append(Button(**args))
				self.buttons[x][y].grid(row=x, column=y)


	def enable_unattacked_enemy_buttons(self, previous_shots):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				if not previous_shots[x][y]:
					self.buttons[x][y]["state"] = "normal"


	def points_in_range(self, start, size):
		points = []
		for x in range(size):
			if (start[1] + x < FIELD_SIZE and self.orientation) or (start[0] + x < FIELD_SIZE and not self.orientation):
				points.append([start[0], start[1]+x] if self.orientation else [start[0]+x, start[1]])
		return points


	# ————————————————————— DISPLAY —————————————————————

	def add_ships_to_field(self, ships):
		for x in range(len(ships)):
			for point in ships[x].location.points:
				self.buttons[point[0]][point[1]]["text"] = SHIP_CHAR


	def change_button_symbol(self, location, symbol):
		self.buttons[location[0]][location[1]]["text"] = symbol


	def disable_button(self, x, y):
		self.buttons[x][y]["state"] = "disable"


	def disable_field_buttons(self):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				self.buttons[x][y]["state"] = "disable"


	def enable_field_buttons(self):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				self.buttons[x][y]["state"] = "normal"




class PlayerField(Field):
	def __init__(self, parent, callback):
		Field.__init__(self, parent, callback)

		self.game.tk.bind("<Tab>", self.switch_orientation)



	def highlighted_buttons(self):
		points = []
		for x in range(len(self.buttons)):
			for y in range(len(self.buttons[x])):
				if self.buttons[x][y]["background"] != "blue": points.append([x, y])
		return points


	# ——————————————————— SHIP PLACEMENT ———————————————————

	def end_ship_placement(self):
		self.game.select_ships = False
		self.disable_field_buttons()
		self.game.enemy_board.field.enable_field_buttons()


	def highlight_ship(self, x, y):
		def function(e):
			if not self.game.select_ships: return
			points = self.points_in_range([x, y], SHIP_SIZES[len(self.parent.ships)])
			color = "yellow" if len(points) == SHIP_SIZES[len(self.parent.ships)] else "red"
			for i in range(len(points)):
				self.buttons[points[i][0]][points[i][1]]["background"] = color
		return function


	def unhighlight_ship(self, x, y):
		def function(e):
			if not self.game.select_ships: return
			points = self.points_in_range([x, y], SHIP_SIZES[len(self.parent.ships)])
			for i in range(len(points)):
				self.buttons[points[i][0]][points[i][1]]["background"] = "blue"
		return function


	def switch_orientation(self, e):
		highlighted_buttons = self.highlighted_buttons()
		self.unhighlight_ship(highlighted_buttons[0][0], highlighted_buttons[0][1])(None)
		self.orientation = not self.orientation
		self.highlight_ship(highlighted_buttons[0][0], highlighted_buttons[0][1])(None)

