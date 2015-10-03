#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate multiple plots from JSON configs.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("-j", "--json-configs", nargs="+",
	                    help="JSON config files.")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	plot_configs = []
	for json_config in args.json_configs:
		plot_config = jsonTools.JsonDict(os.path.expandvars(json_config)).doIncludes().doComments()
		plot_configs.append(plot_config)
	
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

