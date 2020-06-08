

from tkinter import *

from Global import *

from Game import *
from Ships import *


class Data(Frame):
	def __init__(self, parent, player):
		Frame.__init__(self, parent, bg="green")

		# ship data
		ship_data = []
		for x in range(len(SHIP_NAMES)):
			data = {"label" : Label(self, text=SHIP_NAMES[x])}
			data["label"].grid(row=x, column=0)
			data["hits"] = [Label(self, text=SHIP_CHAR) for y in range(SHIP_SIZES[x])]
			for y in range(len(data["hits"])): data["hits"][y].grid(row=x, column=y+1)


class Field(Frame):
	def __init__(self, parent, callback):
		Frame.__init__(self, parent, bg="red")
		self.parent = parent

		self.buttons = []
		for x in range(FIELD_SIZE):
			self.buttons.append([])
			for y in range(FIELD_SIZE):
				function = lambda x=x, y=y: callback(x, y)
				args = {"master": self, "bg": "blue", "foreground": "white", "text": " ", "command": function}
				self.buttons[x].append(Button(**args))
				self.buttons[x][y].grid(row=x, column=y)


	def highlighted_buttons(self):
		points = []
		for x in range(len(self.buttons)):
			for y in range(len(self.buttons[x])):
				if self.buttons[x][y]["background"] != "blue": points.append([x, y])
		return points



class Board(Frame):
	def __init__(self, parent, player, callback):
		Frame.__init__(self, parent, bg="white", bd=16)
		self.parent = parent
		self.field = Field(self, callback)
		self.field.grid(row=0, column=0)
		self.data = Data(self, player)
		self.data.grid(row=0, column=1)



	def add_hover(self, enter, leave):
		for x in range(len(self.field.buttons)):
			for y in range(len(self.field.buttons[x])):
				self.field.buttons[x][y].bind("<Enter>", enter(x, y))
				self.field.buttons[x][y].bind("<Leave>", leave(x, y))


	def add_ships_to_field(self, ships):
		for x in range(len(ships)):
			for point in ships[x].location.points:
				self.field.buttons[point[0]][point[1]]["text"] = SHIP_CHAR


	def change_button_symbol(self, location, symbol):
		self.field.buttons[location[0]][location[1]]["text"] = symbol


	def disable_button(self, x, y):
		self.field.buttons[x][y]["state"] = "disable"


	def disable_field_buttons(self):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				self.field.buttons[x][y]["state"] = "disable"


	def enable_field_buttons(self):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				self.field.buttons[x][y]["state"] = "normal"



class Window:
	def __init__(self):
		self.tk = Tk()

		self.game = Game()
		self.orientation = False
		self.select_ships = True  # bool whether ships are being place by user

		self.enemy_board = None
		self.player_board = None

		self.configure()


	def add_element(self, element, row, column, rowspan=1, columnspan=1):
		element.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
		return element


	def configure(self):
		self.tk.title(WINDOW_TITLE)
		self.tk.configure(background=WINDOW_BACKGROUND)
		self.tk.geometry("1600x900")
		self.tk.bind("<Tab>", self.switch_orientation)


		self.enemy_board = self.add_element(Board(self.tk, self.game.players[0], self.player_shot), 0, 0)
		self.enemy_board.add_ships_to_field(self.game.players[0].ships)  #TESTING
		self.enemy_board.disable_field_buttons()

		self.player_board = self.add_element(Board(self.tk, self.game.players[1], self.place_ship), 1, 0)
		self.player_board.add_hover(self.highlight_ship, self.unhighlight_ship)


	def end_ship_placement(self):
		self.select_ships = False
		self.player_board.disable_field_buttons()
		self.enemy_board.enable_field_buttons()


	def enemy_shot(self, x, y):
		self.game.players[1].is_hit([x, y])


	def player_shot(self, x, y):
		if self.game.players[0].is_hit([x, y]): self.enemy_board.change_button_symbol([x, y], HIT_CHAR)
		else: self.enemy_board.change_button_symbol([x, y], MISS_CHAR)
		self.enemy_board.disable_button(x, y)


	def highlight_ship(self, x, y):
		def function(e):
			if not self.select_ships: return
			points = points_in_range(self.orientation, [x, y], SHIP_SIZES[len(self.game.players[1].ships)])
			color = "yellow" if len(points) == SHIP_SIZES[len(self.game.players[1].ships)] else "red"
			for i in range(len(points)): self.player_board.field.buttons[points[i][0]][points[i][1]]["background"] = color
		return function


	def unhighlight_ship(self, x, y):
		def function(e):
			if not self.select_ships: return
			points = points_in_range(self.orientation, [x, y], SHIP_SIZES[len(self.game.players[1].ships)])
			for i in range(len(points)): self.player_board.field.buttons[points[i][0]][points[i][1]]["background"] = "blue"
		return function


	def switch_orientation(self, e):
		highlighted_buttons = self.player_board.field.highlighted_buttons()
		self.unhighlight_ship(highlighted_buttons[0][0], highlighted_buttons[0][1])(None)
		self.orientation = not self.orientation
		self.highlight_ship(highlighted_buttons[0][0], highlighted_buttons[0][1])(None)


	def place_ship(self, x, y):
		# check placement before proceeding
		self.unhighlight_ship(x, y)(None)

		ship_index = len(self.game.players[1].ships)
		self.game.players[1].ships.append(Ship(SHIP_NAMES[ship_index], SHIP_SIZES[ship_index]))
		self.game.players[1].ships[-1].location = Location(self.orientation, SHIP_SIZES[ship_index], [x, y])
		self.player_board.add_ships_to_field(self.game.players[1].ships)

		if len(self.game.players[1].ships) == len(SHIP_SIZES): self.end_ship_placement()

