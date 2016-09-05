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

	parser = argparse.ArgumentParser(description="Make recoPhiStarCP distributions in different channels.",
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
	                    default="$CMSSW_BASE/src/plots/",
	                    help="Output directory. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	files=["GluGluH*/*.root VBFH*/*.root WminusH*/*.root WplusH*/*.root ZH*/*.root", "SUSYGluGlu*/*.root", "DY*/*.root"]
	samples=["SM", "SUSY", "DY"]

	channels=["ll", "pl", "pp"]
	texts=[
		"#tau^{-} #tau^{+} #rightarrow l^{-} l^{+} #nu_{#tau} #bar{#nu}_{#tau} #bar{#nu}_{l} #nu_{l}",
		"#tau^{-} #tau^{+} #rightarrow #pi^{#mp} l^{#pm} #nu_{#tau} #bar{#nu}_{#tau} [#nu_{l}, #bar{#nu}_{l}]",
		"#tau^{-} #tau^{+} #rightarrow #pi^{-} #pi^{+} #nu_{#tau} #bar{#nu}_{#tau}"
		]
	folders=["em_jecUncNom/ntuple", "et_jecUncNom_tauEsNom/ntuple mt_jecUncNom_tauEsNom/ntuple", "tt_jecUncNom_tauEsNom/ntuple"]

	# reco weights
	wll_reco="1"
	whl_reco="decayMode_1==0 || decayMode_2==0"
	whh_reco="decayMode_1==0 && decayMode_2==0"

	w_reco=[wll_reco, whl_reco, whh_reco]

	plot_configs = []
	
	# doing the plots
	for i in xrange(3):
		config = jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/reco_CP/recoPhiStarCP.json"))
		config["files"] = [files]
		config["folders"] = [folders[i]]
		config["filename"] = "recogenPhiStarCP_"+channels[i]
		config["directories"] = args.input
		config["texts"] = texts[i]
		config["weights"] = [w_reco[i]]
		plot_configs.append(config.copy())

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

