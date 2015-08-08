
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.utility.binnings as binnings


class BinningsDict(binnings.BinningsDict):
	def __init__(self, additional_binnings=None):
		super(BinningsDict, self).__init__(additional_binnings=additional_binnings)
		self.binnings_dict["x"] = ""

