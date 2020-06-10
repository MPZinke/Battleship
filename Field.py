

# shows attack field
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


	def enable_unattacked_enemy_buttons(self, previous_shots):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				if not previous_shots[x][y]:
					self.buttons[x][y]["state"] = "normal"


class PlayerField(Field):
	def __init__(self, parent, callback):
		Field.__init__(self, parent, callback)

	def highlighted_buttons(self):
		points = []
		for x in range(len(self.buttons)):
			for y in range(len(self.buttons[x])):
				if self.buttons[x][y]["background"] != "blue": points.append([x, y])
		return points


