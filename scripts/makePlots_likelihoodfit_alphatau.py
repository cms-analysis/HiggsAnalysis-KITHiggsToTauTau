#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot

import sys

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make CP plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input", required=True, nargs="*",
	                    help="Input.")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/genCP_plots/",
	                    help="Output directory. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	dirs=["CMSSW_7_1_5/src/plots/htt_datacards/datacards/combined","CMSSW_7_1_5/src/plots/htt_datacards/datacards/channel/tt","CMSSW_7_1_5/src/plots/htt_datacards/datacards/channel/mt", "CMSSW_7_1_5/src/plots/htt_datacards/datacards/channel/et", "CMSSW_7_1_5/src/plots/htt_datacards/datacards/channel/em"]
	plot_configs = []
	labels=["combined","channel_tt","channel_mt","channel_et","channel_em"]	
	#plotting likelihood ratio
	for i in range(len(dirs)):	
		json_config=jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/likelihood_ratio_alphatau.json"))		
		json_config["directories"]= dirs[i]
		json_config["labels"]= [labels[i]]
		json_config["filename"]="likelihoodratio"+"_"+labels[i]		
		plot_configs.append(json_config)
	
		
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
