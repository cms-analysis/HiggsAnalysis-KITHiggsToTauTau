#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.core as harrycore
import HiggsAnalysis.KITHiggsToTauTau.plotting.plotroothtt as plotroothtt


def higgs_plot(args_from_script = None):
	"""
	Main plotting function
	
	Can be called from within python scripts by passing the arguments as a string
	as it would be done by calling this script in the bash.
	"""
	
	harry_core = harrycore.HarryCore()
	
	# register custom version of ROOT plots which creates plots in the officital Htautau style
	harry_core.register_processor(plotroothtt.PlotRootHtt.name(), plotroothtt.PlotRootHtt())
	
	harry_core.run(args_from_script)

