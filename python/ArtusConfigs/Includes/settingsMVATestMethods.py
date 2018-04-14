# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)


class MVATestMethods(dict):
	def __init__(self):

		self["MVATestMethodsInputQuantities"] = []
   		self["MVATestMethodsMethods"] = []
   		self["MVATestMethodsWeights"] = []
   		
