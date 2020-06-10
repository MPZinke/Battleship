
from tkinter import *

from Global import *


class Data(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent, bg="green")
		self.parent = parent

		# ship data
		ship_data = []
		for x in range(len(SHIP_NAMES)):
			data = {"label" : Label(self, text=SHIP_NAMES[x])}
			data["label"].grid(row=x, column=0)
			data["hits"] = [Label(self, text=SHIP_CHAR) for y in range(SHIP_SIZES[x])]
			for y in range(len(data["hits"])): data["hits"][y].grid(row=x, column=y+1)

