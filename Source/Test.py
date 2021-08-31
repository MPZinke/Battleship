

from time import sleep;


from Global import *;
from Ship import Ship, Location;
from Targeting import Targeting;


class Game:
	MISS = -1;
	UNKNOWN = 0;
	HIT = 1;

	def __init__(self):
		self._ai = MinAI(self);
		self.enemy = MinAI(self);


	def mainloop(self):
		self.print_boards();
		self.attack();
		while(True):
			self.print_boards()
			input("Press enter to continue");
			self.attack();


	def attack(self):
		if(not self._ai.targeting): point = [6,6];
		else:
			point = self._ai.targeting.next_move();
			print("Point: {}".format(point));

		shot_ship = self.enemy.shot(point);
		self._ai.shoot_at_enemy(point, shot_ship);


	def print_boards(self):
		print("Enemy:")
		self.enemy.print_board(True);
		print("AI:");
		self._ai.print_board();



class MinAI:
	def __init__(self, game):
		self.game = game;

		self.targeting = None;
		self.player_shots = [[Game.UNKNOWN for y in range(FIELD_SIZE)] for x in range(FIELD_SIZE)];
		# self.player_shots[6][6] = Game.HIT;

		ship_data = [[True, 5, [6,4]], [False, 4, [6,2]], [False, 3, [6,3]], [True, 3, [9,6]], [True, 2, [6, 0]]];
		ships = Ship.SHIPS;
		self.ships = [Ship(x, ships[x]["name"], ships[x]["size"], Location(*(ship_data[x]))) for x in range(len(ships))];


	def print_board(self, show_ships=False):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				if(any(ship.is_hit([x,y]) for ship in self.ships)): print('x', end="");
				elif(show_ships and any(ship.hits_ship([x,y]) for ship in self.ships)): print('S',end="");
				else: print({-1: 'O', 0: ' ', 1: 'X'}[self.player_shots[x][y]], end="");
				print("|", end="");
			print();
		print();


	def shoot_at_enemy(self, point, ship):
		self.player_shots[point[0]][point[1]] = Game.HIT if ship else Game.MISS;
		if(ship and not self.targeting): self.targeting = Targeting(self.game, self, point);
		if(ship and ship.is_sunk()): self.targeting.move_sunk_a_ship(ship, ship.location.points);
		if(self.targeting): self.targeting.record_previous_move();


	def shot(self, point):
		shot_ship = [ship for ship in self.ships if ship.shot(point)];
		if(shot_ship): return shot_ship[0];
		return None;



def main():
	game = Game();
	game.mainloop()


if __name__ == '__main__':
	main();
