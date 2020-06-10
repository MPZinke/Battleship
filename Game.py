
from Global import *

import Ships


class Player:
	def __init__(self, name):
		self.name = name
		self.ships = None
		self.shots = [[False] * FIELD_SIZE] * FIELD_SIZE


	def is_hit(self, location):
		for x in range(len(self.ships)):
			for y in range(len(self.ships[x].location.points)):
				if location == self.ships[x].location.points[y]:
					self.ships[x].hit(location)
					return True
		return False


class Enemy(Player):
	def __init__(self, name):
		Player.__init__(self, name)

		self.shot = None  # previous shot
		self.targeting = False

	def attack(self):
		pass
		# attack logic


class Game:
	def __init__(self):
		self.players = [Enemy("Enemy"), Player("Player")]
		self.players[0].ships = Ships.place_ships_randomly()
		self.players[1].ships = []

		self.over = False
		self.turn = 0  # bool: 0 for player 1, 1 for player 2
		self.turn_count = 0
		self.winner = None


	def finish(self, winner):
		self.winner = winner


	def is_over(self):
		for x in range(len(self.players)):
			if all(ship.is_sunk() for ship in self.players[x].ships):
				self.over = True
				return True
		return False