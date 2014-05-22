#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.core as harrycore
import HiggsAnalysis.KITHiggsToTauTau.plotting.plotroothtt as plotroothtt


if __name__ == "__main__":
	harry_core = harrycore.HarryCore()
	
	# register custom version of ROOT plots which creates plots in the officital Htautau style
	harry_core.register_processor(plotroothtt.PlotRootHtt.name(), plotroothtt.PlotRootHtt())
	
	harry_core.run()

