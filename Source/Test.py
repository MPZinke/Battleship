

from random import randint;
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
		self._ai.attack();
		while(True):
			self.print_boards()
			input("Press enter to co;ntinue");
			self._ai.attack();
			if(all(ship.is_sunk() for ship in self.enemy.ships)):
				self.print_boards();
				print("YOU WON!!!");
				return


	def attack(self, point):
		shot_ship = self.enemy.shot(point);
		# update GUI stuff
		return shot_ship if(shot_ship) else None;


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
		self.sunk_enemy_ship_ids = [];  #TRANSFER

		ship_data = [[True, 5, [6,4]], [False, 4, [6,2]], [False, 3, [6,3]], [True, 3, [9,6]], [True, 2, [6, 0]]];
		ships = Ship.SHIPS;
		# self.ships = [Ship(x, ships[x]["name"], ships[x]["size"], Location(*(ship_data[x]))) for x in range(len(ships))];
		self.ships = Ship.place_all_ships_randomly();


	def print_board(self, show_ships=False):
		for x in range(FIELD_SIZE):
			for y in range(FIELD_SIZE):
				if(any(ship.is_hit([x,y]) for ship in self.ships)): print('x', end="");
				elif(show_ships and any(ship.hits_ship([x,y]) for ship in self.ships)): print('S',end="");
				else: print({-1: 'O', 0: ' ', 1: 'X'}[self.player_shots[x][y]], end="");
				print("|", end="");
			print();
		print();


	#TRANSFER
	def attack(self):
		if(self.targeting): attack_point = self.targeting.next_move();
		# elif(not self.sunk_enemy_ship_ids): attack_point = [6,6];  #IGNORE
		else:
			for x in range(0xFFFF):
				if(x == 0xFFFE): raise Exception("MinAI::attack:attack_point: OVERFLOW");
				attack_point = [randint(0, FIELD_SIZE-1), randint(0, FIELD_SIZE-1)];
				if(index(self.player_shots, attack_point) == self.game.UNKNOWN): break;

		print("MinAI::attack:attack_point: ", str(attack_point));
		shot_ship = self.game.attack(attack_point);
		self.record_previous_move(attack_point, shot_ship);


	#TRANSFER
	def record_previous_move(self, point, shot_ship):
		self.player_shots[point[0]][point[1]] = Game.HIT if shot_ship else Game.MISS;
		if(self.targeting): self.targeting.record_previous_move(shot_ship);
		elif(shot_ship): self.targeting = Targeting(self.game, self, point);

		if(shot_ship and shot_ship.is_sunk()): self.sunk_enemy_ship_ids.append(shot_ship.id);



	def shoot_at_enemy(self, point, ship):
		self.player_shots[point[0]][point[1]] = Game.HIT if ship else Game.MISS;
		if(ship and not self.targeting): self.targeting = Targeting(self.game, self, point);
		if(self.targeting): self.targeting.record_previous_move();
		if(ship and ship.is_sunk()): self.targeting.move_sunk_a_ship(ship, ship.location.points);


	def shot(self, point):
		shot_ship = [ship for ship in self.ships if ship.shot(point)];
		if(shot_ship): return shot_ship[0];
		return None;



def main():
	game = Game();
	game.mainloop()


if __name__ == '__main__':
	main();
