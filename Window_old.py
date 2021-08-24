

from tkinter import *

from Global import *
from Board import *


class Game:
	def __init__(self):
		self.tk = Tk()

		self.enemy_board = None
		self.player_board = None

		self.tk.title(WINDOW_TITLE)
		self.tk.configure(background=WINDOW_BACKGROUND)
		self.tk.geometry("1000x700")

		self.enemy_board = self.new_element(EnemyBoard(self.tk, self), 0, 0)
		self.enemy_board.field.add_ships_to_field(self.enemy_board.ships)  #TESTING
		self.enemy_board.field.disable_field_buttons()

		self.player_board = self.new_element(PlayerBoard(self.tk, self), 1, 0)

		self.select_ships = True  # bool whether ships are being place by user



	def new_element(self, element, row, column, rowspan=1, columnspan=1):
		element.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
		return element


	# ————————————————————— ATTACK ——————————————————————

	def enemy_attack(self):
		# disable buttons
		# attack
		self.enable_unattacked_enemy_buttons()

