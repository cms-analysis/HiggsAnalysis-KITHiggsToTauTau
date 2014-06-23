# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os
import ROOT

import Artus.HarryPlotter.plotbase as plotbase


class PlotSettingsHtt(plotbase.PlotBase):
	def __init__(self):
		super(PlotSettingsHtt, self).__init__()
	
	def modify_argument_parser(self, parser, args):
		super(PlotSettingsHtt, self).modify_argument_parser(parser, args)
	
	def prepare_args(self, parser, plotData):
		if plotData.plotdict["x_expressions"][0] == "1":
			if plotData.plotdict["x_label"] == parser.get_default("x_label"):
				plotData.plotdict["x_label"] = "Inclusive"
			if plotData.plotdict["x_bins"] == parser.get_default("x_bins"):
				plotData.plotdict["x_bins"] = ["1"]
			
		
		super(PlotSettingsHtt, self).prepare_args(parser, plotData)

