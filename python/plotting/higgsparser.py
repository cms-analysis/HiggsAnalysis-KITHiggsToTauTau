# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.harryparser as harryparser


class HiggsParser(harryparser.HarryParser):
	def __init__(self, **kwargs):
		super(HiggsParser, self).__init__()
		
		self.set_defaults(
				input_modules="InputRootHtt",
				plot_modules=["PlotRootHtt"]
		)
