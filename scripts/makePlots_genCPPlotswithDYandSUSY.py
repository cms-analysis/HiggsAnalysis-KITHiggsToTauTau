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
	w_dy1=["((OneProngChargedPart1PdgId == 211 && OneProngChargedPart2PdgId == -211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
	w_dy2=["((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
	w_dy3=["((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
	w_dy4=["((OneProngChargedPart1PdgId == -11 || OneProngChargedPart1PdgId == -13 && OneProngChargedPart2PdgId == 11 || OneProngChargedPart2PdgId == 13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
	w_dy=[w_dy1,w_dy2,w_dy3,w_dy4]	
	w1=["tauSpinnerWeight000","tauSpinnerWeight025","tauSpinnerWeight050","tauSpinnerWeight075","tauSpinnerWeight100"]
	w_pp=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == -211 && OneProngChargedPart2PdgId == 211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))"]
	w_hh=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))"]
	w_hl=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
	w_ll=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 11 || OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11 || OneProngChargedPart2PdgId == -13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
	
	w_evenandodd=[[w_pp[0],w_dy1,w_dy1],[w_hh[0],w_dy2,w_dy2],[w_hl[0],w_dy3,w_dy3],[w_ll[0],w_dy4,w_dy4]]
	

	w=[w_pp,w_hh,w_hl,w_ll]
	names=["_pionpion","_hadronhadron","_hadronlepton","_leptonlepton"]
	names_dy=["_dypipi","_dyhh","_dyhl","_dyll"]
	#y_lims=[[0.0,0.1],[0.0,0.1],[0.02,0.06],[0.028,0.045]]
	nicks=["alpha000","alpha025","alpha050","alpha075","alpha100"]
	colors=[ "#ff2400","#0020c2","#4cc417","#a74ac7","#3bb9ff"]	
	colors_evenandodd=["#ff2400","#3bb9ff","#4cc417"]
	nicks_evenandodd=["alpha000","alpha100","DYbkg"]
	
	plot_configs = []
	
	#all mixingangles in 1 plot
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
	#only CP-even and CP-odd in 1 plot with DYbkg and SUSY
	for j in xrange(4):	
		config2=jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/gen_CP/phiCPevenandodd.json"))		
		config2["colors"]=[colors_evenandodd]
		config2["filename"]= "genPhiCPonlyevenandodd" + names[j]
		config2["nicks"]=[nicks_evenandodd]
		config2["weights"]=[w_evenandodd[j]]
		config2["directories"] = args.input
		config2["files"]=["GluGluHToTauTauM*/*.root VBFH*/*.root W*/*.root ZH*/*.root","SUSY*/*.root","DYJets*/*root"]
		plot_configs.append(config2)
	
	
		
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
