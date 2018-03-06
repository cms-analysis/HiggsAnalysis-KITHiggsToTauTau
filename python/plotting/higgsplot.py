#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import os

import Artus.HarryPlotter.harry as harry
import Artus.HarryPlotter.core as harrycore

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsparser as higgsparser


class HiggsPlotter(harry.HarryPlotter):

	def __init__(self, list_of_config_dicts=None, list_of_args_strings=None, n_processes=1, n_plots=None, batch=None):
		standalone_executable = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/scripts/standalone_higgsplot.sh")
		super(HiggsPlotter, self).__init__(list_of_config_dicts=list_of_config_dicts,
		                                   list_of_args_strings=list_of_args_strings,
		                                   n_processes=n_processes,
		                                   n_plots=n_plots,
		                                   batch=batch,
		                                   standalone_executable=standalone_executable)
	
	def plot(self, plot_index):
		harry_args = self.harry_args[plot_index]
		parser = higgsparser.HiggsParser()
		harry_core = harrycore.HarryCore(args_from_script=harry_args, parser=parser)
		if not harry_args is None:
			log.debug("higgsplot.py " + str(harry_args))
		
		harry_core.register_modules_dir("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau/plotting/modules/input_modules")
		harry_core.register_modules_dir("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau/plotting/modules/analysis_modules")
		harry_core.register_modules_dir("$CMSSW_BASE/python/HiggsAnalysis/KITHiggsToTauTau/plotting/modules/plot_modules")
		
		# modify default program args
		harry_core.parser.set_defaults(plot_modules=["PlotRootHtt"])
		
		return harry_core.run()

