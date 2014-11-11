#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HarryPlotter.Plotting.core as harrycore
import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.plotroothtt as plotroothtt
import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.estimateztt as estimateztt
import HiggsAnalysis.KITHiggsToTauTau.plotting.modules.estimatewjets as estimatewjets


def higgs_plot(args_from_script = None):
	"""
	Main plotting function
	
	Can be called from within python scripts by passing the arguments as a string
	as it would be done by calling this script in the bash.
	"""
	
	harry_core = harrycore.HarryCore()
	
	# register custom version of ROOT plots which creates plots in the officital Htautau style
	harry_core.register_processor(plotroothtt.PlotRootHtt.name(), plotroothtt.PlotRootHtt())
	
	# register analysis modules for sample estimations
	harry_core.register_processor(estimateztt.EstimateZtt.name(), estimateztt.EstimateZtt())
	harry_core.register_processor(estimatewjets.EstimateWjets.name(), estimatewjets.EstimateWjets())
	
	harry_core.run(args_from_script)

