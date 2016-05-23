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

#	w_dy1=["((OneProngChargedPart1PdgId == 211 && OneProngChargedPart2PdgId == -211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
#	w_dy2=["((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
#	w_dy3=["((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
#	w_dy4=["((OneProngChargedPart1PdgId == -11 || OneProngChargedPart1PdgId == -13 && OneProngChargedPart2PdgId == 11 || OneProngChargedPart2PdgId == 13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
#	w_dy=[w_dy1,w_dy2,w_dy3,w_dy4]	
#	w1=["tauSpinnerWeight000","tauSpinnerWeight025","tauSpinnerWeight050","tauSpinnerWeight075","tauSpinnerWeight100"]
#	w_pp=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))"]
#	w_hh=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
#       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))"]
#	w_hl=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
#	w_ll=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
#       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
#	
#	w_evenandodd=[[w_pp[0],w_dy1,w_dy1],[w_hh[0],w_dy2,w_dy2],[w_hl[0],w_dy3,w_dy3],[w_ll[0],w_dy4,w_dy4]]
	

	w_pp=["( 1 * ( (OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55) ) )"]
	w_hh=["( 1 * ( ((OneProngChargedPart1PdgId == -20213 || OneProngChargedPart1PdgId == -213 || OneProngChargedPart1PdgId == -211) && (OneProngChargedPart2PdgId == 20213 || OneProngChargedPart2PdgId == 213 || OneProngChargedPart2PdgId == 211)) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55) ) )"]
	w_hl=["( 1 * ( ( ((OneProngChargedPart1PdgId == -20213 || OneProngChargedPart1PdgId == -213 || OneProngChargedPart1PdgId == -211) && (OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13)) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.44) ) || ( ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart2PdgId == 13) && (OneProngChargedPart2PdgId == 20213 || OneProngChargedPart2PdgId == 213 || OneProngChargedPart2PdgId == 211)) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.55) ) ) )"]
	w_ll=["( 1 * ( ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart2PdgId == 13) && (OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13)) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44) ) )"]

	text_pp=["$\\tau^- \\tau^+ \\rightarrow \\pi^- \\pi^+ \\nu_{\\tau} \\bar{\\nu}_{\\tau}$"]
	text_hh=["$\\tau^- \\tau^+ \\rightarrow h^- h^+ \\nu_{\\tau} \\bar{\\nu}_{\\tau}$"]
	text_hl=["$\\tau^- \\tau^+ \\rightarrow h^{\\mp} l^{\\pm} \\nu_{\\tau} \\bar{\\nu}_{\\tau} [\\nu_l, \\bar{\\nu}_l]$"]
	text_ll=["$\\tau^- \\tau^+ \\rightarrow l^- l^+ \\nu_{\\tau} \\bar{\\nu}_{\\tau} \\bar{\\nu}_l \\nu_l$"]


	w=[w_pp, w_hh, w_hl, w_ll]
	names=["_pp", "_hh", "_hl", "_ll"]
	nicks=["CPeven", "CPodd", "DY"]
	colors=[ "#ff2400","#0020c2","#4cc417","#a74ac7","#3bb9ff"]
	
	plot_configs = []
	
	# CPeven, CPodd and DY in 1 plot
	for i in xrange(4):		
		config1 = jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/gen_CP/phiCP.json"))
		#all mixingangles in 1 plot
	 	config1["colors"] = [colors]
	  	config1["filename"] = "genPhiCPalphaTau"+names[i]
		config1["nicks"] = [nicks]
	   	config1["weights"] = [w[i]]
		config1["directories"]=args.input
		config1["files"]=["GluGluHToTauTauM*/*.root VBFH*/*.root W*/*.root ZH*/*.root"]
		plot_configs.append(config1)	
	

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
