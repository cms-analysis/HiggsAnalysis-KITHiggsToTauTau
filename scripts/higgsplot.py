#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.harrycore as harrycore

# import analysis specific functions
import HiggsAnalysis.KITHiggsToTauTau.HarryPlotterModules.decayproducts as higgsmodule

if __name__ == "__main__":
	"""This is a template for users to make analysis-specific plots with HarryPlotter."""

	basedict = harrycore.get_basic_dictionary()

	parser = harrycore.get_basic_parser(**basedict)


	plotdict = harrycore.create_dictionary_from_parser(parser)

	# Add the module with the user-written functions to the plotdict
	plotdict['analysismodules'] =[higgsmodule]


	harrycore.plot(plotdict)
