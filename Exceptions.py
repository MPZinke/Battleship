#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2021.08.24                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################



class AlreadyShot(Exception):
	def __init__(self, point):
		Exception.__init__(self, message="Already Shot at point: [{},{}]".format(*point));



class OutOfBounds(Exception):
	def __init__(self, point):
		Exception.__init__(self, message="[{},{}] is out of bounds".format(*point));



class ShipInWay(Exception):
	def __init__(self, point):
		Exception.__init__(self, message="There is a conflicting ship at [{},{}]".format(*point));



class TooManyAttempts(Exception):
	def __init__(self, message):
		Exception.__init__(self, message=message);
