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


def execute_multiple(*args):
	for arg in args: arg();


# Gets the value at the specified index for a multidimensional list list.
def index(multidimensional_list, point):
	value = multidimensional_list;
	for subindex in point:
		value = value[subindex];
	return value;


def is_mac():
	from platform import system;
	return system() == "Darwin";


def lambda_helper(function, *args):
	if(len(args) == 0): return lambda: function();
	if(len(args) == 1): return lambda w=args[0]: function(w);
	if(len(args) == 2): return lambda w=args[0], x=args[1]: function(w,x);
	if(len(args) == 2): return lambda w=args[0], x=args[1], y=args[2]: function(w,x,y);
	if(len(args) == 2): return lambda w=args[0], x=args[1], y=args[2], z=args[3]: function(w,x,y,z);


def print_trace():
	import traceback;
	for line in traceback.format_stack():
		print(line.strip())


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
HIT_COLOR = "red";
OCEAN_COLOR = "blue";
SHIP_COLOR = "gray";
WINDOW_BACKGROUND = "#444444"
# GUI::FUNCTIONALITY
DISABLE = "disabled" if(is_mac()) else "disable";

