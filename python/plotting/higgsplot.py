#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.harry as harry
import Artus.HarryPlotter.core as harrycore


class HiggsPlotter(harry.HarryPlotter):

	def __init__(self, plots=None, n_processes=4):
		super(HiggsPlotter, self).__init__(plots, n_processes=n_processes)
	
	def plot(self, harry_args):
		harry_core = harrycore.HarryCore(args_from_script=harry_args)
		
		harry_core.register_modules_dir("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau/plotting/modules/analysis_modules")
		harry_core.register_modules_dir("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau/plotting/modules/plot_modules")
		
		harry_core.run()

