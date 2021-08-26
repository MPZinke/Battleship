

FIELD_SIZE = 10

OCEAN_CHAR = '  '
OCEAN_CHAR_CLI = '~'
HIT_CHAR = '×'
MISS_CHAR = '○'
SHIP_CHAR = 'S'

OCEAN_CLR = "blue";
SHIP_CLR = "gray";
HIT_CLR = "red";


SHIP_NAMES = ["Carrier", "Battleship", "Friggate", "Friggate", "Cruiser"]
SHIP_SIZES = [5, 4, 3, 3, 2]


WINDOW_TITLE = "Battleship"
WINDOW_BACKGROUND = "#444444"


# Gets the value at the specified index for a multidimensional list list.
def index(multidimensional_list, point):
	value = multidimensional_list;
	for subindex in point:
		value = value[subindex];
	return value;

