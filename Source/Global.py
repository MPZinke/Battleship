#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.28                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


# Gets the value at the specified index for a multidimensional list list.
def index(multidimensional_list, point):
	value = multidimensional_list;
	for subindex in point:
		value = value[subindex];
	return value;


def is_mac():
	from platform import system;
	return system() == "Darwin";


# GAME
FIELD_SIZE = 10

# GUI
# GUI::STYLING
# GUI::STYLING::TITLES
WINDOW_TITLE = "Battleship"
# GUI::STYLING::CHARS
OCEAN_CHAR = '  '
OCEAN_CHAR_CLI = '~'
HIT_CHAR = '×'
MISS_CHAR = '○'
SHIP_CHAR = 'S'
# GUI::STYLING::COLORS
HIT_CLR = "red";
OCEAN_COLOR = "blue";
SHIP_COLOR = "gray";
WINDOW_BACKGROUND = "#444444"
# GUI::FUNCTIONALITY
DISABLE = "disabled" if(is_mac()) else "disable";

