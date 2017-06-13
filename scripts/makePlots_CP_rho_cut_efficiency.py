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

	parser = argparse.ArgumentParser(description="Make ROC plots for rho_CP_studies.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-signal", nargs="*",
	                    help="Signal Input.")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("--ntuple",
                    help="ntuple to read in.")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	#CutEff PLOT
	plot_configs = []

	config_CutEff = {
    	"analysis_modules": [
		"CutEfficiency",
		"FullIntegral"
    	],
    	"cut_efficiency_bkg_nicks": ["bkg"],
    	"cut_efficiency_nicks": ["roc"],
    	"cut_efficiency_sig_nicks": ["#phi^{*}_{CP}"],
    	"filename": "ROC_rho_CP_studies",
		"files": [
		"/net/scratch_cms3b/wolfschlaeger/artus/2017-05-23_00-30_Run2Analysis_Summer16/merged/GluGluHToTauTau*/*.root /net/scratch_cms3b/wolfschlaeger/artus/2017-05-23_00-30_Run2Analysis_Summer16/merged/VBFH*/*.root /net/scratch_cms3b/wolfschlaeger/artus/2017-05-23_00-30_Run2Analysis_Summer16/merged/WminusH*/*.root /net/scratch_cms3b/wolfschlaeger/artus/2017-05-23_00-30_Run2Analysis_Summer16/merged/WplusH*/*.root /net/scratch_cms3b/wolfschlaeger/artus/2017-05-23_00-30_Run2Analysis_Summer16/merged/ZH*/*.root",
		"/net/scratch_cms3b/wolfschlaeger/artus/2017-05-23_00-30_Run2Analysis_Summer16/merged/DY*/*.root"
		],
    	"folders": ["tt_nominal/ntuple"],
    	"markers": [
		"LP"
    	],
    	"nicks": [
		"#phi^{*}_{CP}",
		"bkg"
		],
    	"nicks_whitelist": ["roc"],
    	"weights": [
		"(1.0)*((((decayMode_1 == 1) * (decayMode_2 == 1) * (reco_yTauL < 0))))*eventWeight*(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)*((gen_match_2 == 5)*0.95 + (gen_match_2 != 5))*(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)*((gen_match_1 == 5)*0.95 + (gen_match_1 != 5))*(pt_1 > 40)",
		"(1.0)*((((decayMode_1 == 1) * (decayMode_2 == 1) * (reco_yTauL < 0))))*eventWeight*((byMediumIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5) || (byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5 && byLooseIsolationMVArun2v1DBoldDMwLT_1 > 0.5 && byTightIsolationMVArun2v1DBoldDMwLT_1 < 0.5))*topPtReweightWeight*(pt_1 > 40)"
    	],

    	"x_expressions": [
		"recoPhiStarCP_rho"
    	],
    	"x_label": "bkg_rej",
    	"y_label": "sig_eff",
	"legend": [0.25, 0.25, 0.45, 0.45],
	"legend_cols": 1,
	"legend_markers": ["LP"]
	}

	plot_configs.append(config_CutEff)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
