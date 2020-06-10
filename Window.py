

from tkinter import *

from Global import *

from Game import *
from Ships import *


class Window:
	def __init__(self):
		self.tk = Tk()

		self.game = Game()
		self.orientation = False
		self.select_ships = True  # bool whether ships are being place by user

		self.enemy_board = None
		self.player_board = None

		self.configure()


	def configure(self):
		self.tk.title(WINDOW_TITLE)
		self.tk.configure(background=WINDOW_BACKGROUND)
		self.tk.geometry("1000x700")
		self.tk.bind("<Tab>", self.switch_orientation)


		self.enemy_board = self.new_element(Board(self.tk, self.game.players[0], self.player_shot), 0, 0)
		self.enemy_board.add_ships_to_field(self.game.players[0].ships)  #TESTING
		self.enemy_board.disable_field_buttons()

		self.player_board = self.new_element(Board(self.tk, self.game.players[1], self.place_ship), 1, 0)
		self.player_board.add_hover(self.highlight_ship, self.unhighlight_ship)


	def new_element(self, element, row, column, rowspan=1, columnspan=1):
		element.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
		return element


	# ————————————————————— ATTACK ——————————————————————

	def enemy_attack(self):
		# disable buttons
		# attack
		self.enable_unattacked_enemy_buttons()


	def player_shot(self, x, y):
		if self.game.players[0].is_hit([x, y]): self.enemy_board.change_button_symbol([x, y], HIT_CHAR)
		else: self.enemy_board.change_button_symbol([x, y], MISS_CHAR)


