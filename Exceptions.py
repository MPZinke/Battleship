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
	def __init__(self, location):
		Exception.__init__(self, message="Already Shot at location: [{},{}]".format(*location));


class OutOfBounds(Exception):
	def __init__(self, location):
		Exception.__init__(self, message="[{},{}] is out of bounds".format(*location));


class TooManyAttempts(Exception):
	def __init__(self, message):
		Exception.__init__(self, message=message);
