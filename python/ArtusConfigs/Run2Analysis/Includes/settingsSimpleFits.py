# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re


class SimpleFits(dict):
	def __init__(self, nickname, legacy=True):

		self["GEFMassConstraint"] = 125.0
		self["GEFUseCollinearityTauMu"] = False
		self["GEFUseMVADecayModes"] = True
		self["GEFMinimizer"] = "Minuit"
		# self["GEFMinimizer"] = "Standard"
