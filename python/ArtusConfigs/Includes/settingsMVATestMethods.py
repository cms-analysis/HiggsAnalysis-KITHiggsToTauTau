# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import copy

class MVATestMethods(dict):
	def __init__(self):

		self["MVATestMethodsInputQuantities"] = []
   		self["MVATestMethodsMethods"] = []
   		self["MVATestMethodsWeights"] = []
