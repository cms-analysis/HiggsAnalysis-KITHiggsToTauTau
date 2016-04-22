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
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	w=["( (tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))) && tauSpinnerWeight000 !=1)",
        "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)) && tauSpinnerWeight025 !=1 )",
        "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)) && tauSpinnerWeight050 !=1 )",
        "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)) && tauSpinnerWeight075 !=1 )",
        "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)) && tauSpinnerWeight100 !=1 )"]
	nicks=["alpha000","alpha025","alpha050","alpha075","alpha100"]
	colors=[ "#ff2400","#0020c2","#4cc417","#a74ac7","#3bb9ff"]
	plot_configs = []
	for i in xrange(5):
		config = {
    	"analysis_modules": [
    			"NormalizeToUnity",
				"PrintInfos"
    	],
    	"colormap": "afmhot",
     	"colors": [colors[i]],
      
     	"edgecolors": "white",
      	"filename": "genPhiCPalphaTau"+nicks[i],
       	"folders": [
    	"gen/ntuple"
     	],
     	"formats": [
     	   "png"
        
     	   ],
     	"legend_cols": 3,
      	"line_styles": [
        	"-"
    	],
    	"markers": [
     	   "-"
    	],
    	"nicks": [nicks[i]],
    
    	"plot_modules": [
     		"PlotMpl"
       	],
       	"weights": [w[i]],
        
    
    	"x_bins": [
    	    "30,0.0,6.28"
    		],
    	"x_errors": False,
      	"x_expressions": [
    		"genPhiStarCP",
	      	"genPhiStarCP",
	        "genPhiStarCP",
	        "genPhiStarCP",
	        "genPhiStarCP"
	    ],
	    "x_label": "x",
	    "x_lims": [
	        0.0,
	        6.3
	    ],
	    "y_bins": [
	        "10"
	    ],
	    "y_errors": True,
	    "y_label": "arbitrary units",
	    "y_lims": [
	        0.0,
	        0.08
	    ]
		}
		
		config["files"] = args.input
		
		
		plot_configs.append(config)
	
		if log.isEnabledFor(logging.DEBUG):
			import pprint
			pprint.pprint(plot_configs)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
