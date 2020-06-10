

# shows player & data
class Board(Frame):
	def __init__(self, parent):
		# GUI
		Frame.__init__(self, parent, bg="white", bd=16)
		self.parent = parent
		self.data = Data(self)
		self.data.grid(row=0, column=1)

		# game
		self.ships = None
		self.shots = [[False] * FIELD_SIZE] * FIELD_SIZE


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


	def set_field(self, callback):
		self.field = Field(self)
		self.field.grid(row=0, column=0)


class PlayerBoard(Board):
	def __init__(self, parent):
		self.orientation = False


	# ——————————————————— SHIP PLACEMENT ———————————————————

	def end_ship_placement(self):
		self.select_ships = False
		self.player_board.disable_field_buttons()
		self.enemy_board.enable_field_buttons()


	def highlight_ship(self, x, y):
		def function(e):
			if not self.select_ships: return
			points = points_in_range(self.orientation, [x, y], SHIP_SIZES[len(self.game.players[1].ships)])
			color = "yellow" if len(points) == SHIP_SIZES[len(self.game.players[1].ships)] else "red"
			for i in range(len(points)):
				self.player_board.field.buttons[points[i][0]][points[i][1]]["background"] = color
		return function


	def unhighlight_ship(self, x, y):
		def function(e):
			if not self.select_ships: return
			points = points_in_range(self.orientation, [x, y], SHIP_SIZES[len(self.game.players[1].ships)])
			for i in range(len(points)):
				self.player_board.field.buttons[points[i][0]][points[i][1]]["background"] = "blue"
		return function


	def switch_orientation(self, e):
		highlighted_buttons = self.player_board.field.highlighted_buttons()
		self.unhighlight_ship(highlighted_buttons[0][0], highlighted_buttons[0][1])(None)
		self.orientation = not self.orientation
		self.highlight_ship(highlighted_buttons[0][0], highlighted_buttons[0][1])(None)


	def place_ship(self, x, y):
		ship_index = len(self.game.players[1].ships)
		points = points_in_range(self.orientation, [x, y], SHIP_SIZES[ship_index])
		# check if spot invalid
		if(any(point in points for ship in self.game.players[1].ships for point in ship.location.points)) \
		or len(points) != SHIP_SIZES[ship_index]:
			for i in range(len(points)):
				self.player_board.field.buttons[points[i][0]][points[i][1]]["background"] = "red"
		# spot is valid
		else:
			# check placement before proceeding
			self.unhighlight_ship(x, y)(None)

			self.game.players[1].ships.append(Ship(SHIP_NAMES[ship_index], SHIP_SIZES[ship_index]))
			self.game.players[1].ships[-1].location = Location(self.orientation, SHIP_SIZES[ship_index], [x, y])
			self.player_board.add_ships_to_field(self.game.players[1].ships)

			if ship_index+1 == len(SHIP_SIZES): self.end_ship_placement()
