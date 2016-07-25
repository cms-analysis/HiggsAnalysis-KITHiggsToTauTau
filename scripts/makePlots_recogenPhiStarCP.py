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

	parser = argparse.ArgumentParser(description="Make genPhiStarCP and recoPhiStarCP comparison.",
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

	channels=["ll", "hl", "hh"]
	texts=["ll ch.", "hl ch.", "hh ch."]
	folders_gen="gen/ntuple"
	folders_reco=["em_jecUncNom/ntuple", "et_jecUncNom_tauEsNom/ntuple mt_jecUncNom_tauEsNom/ntuple", "tt_jecUncNom_tauEsNom/ntuple"]

	# gen weights
	#wll_SM_gen="(OneProngChargedPart1PdgId==11 || OneProngChargedPart1PdgId==13) && (OneProngChargedPart2PdgId==-11 || OneProngChargedPart2PdgId==-13) && (Tau1OneProngsSize==3 && Tau2OneProngsSize==3) && (TauMProngEnergy>=0.44 && TauPProngEnergy>=0.44)"
	#whl_SM_gen="((OneProngChargedPart1PdgId==-211 && (OneProngChargedPart2PdgId==-11 || OneProngChargedPart2PdgId==-13)) && (Tau1OneProngsSize==2 && Tau2OneProngsSize==3) && (TauMProngEnergy>=0.55 && TauPProngEnergy>=0.44)) || (((OneProngChargedPart1PdgId==11 || OneProngChargedPart1PdgId==13) && OneProngChargedPart2PdgId==211) && (Tau1OneProngsSize==3 && Tau2OneProngsSize==2) && (TauMProngEnergy>=0.44 && TauPProngEnergy>=0.55))"
	#whh_SM_gen="(OneProngChargedPart1PdgId==-211 && OneProngChargedPart2PdgId==211) && (Tau1OneProngsSize==2 && Tau2OneProngsSize==2) && (TauMProngEnergy>=0.55 && TauPProngEnergy>=0.55)"
	wll_SM_gen="(OneProngChargedPart2PdgId==11 || OneProngChargedPart2PdgId==13) && (OneProngChargedPart1PdgId==-11 || OneProngChargedPart1PdgId==-13) && (Tau1OneProngsSize==3 && Tau2OneProngsSize==3) && (TauMProngEnergy>=0.44 && TauPProngEnergy>=0.44)"
	whl_SM_gen="((OneProngChargedPart2PdgId==-211 && (OneProngChargedPart1PdgId==-11 || OneProngChargedPart1PdgId==-13)) && (Tau1OneProngsSize==3 && Tau2OneProngsSize==2) && (TauMProngEnergy>=0.55 && TauPProngEnergy>=0.44)) || (((OneProngChargedPart2PdgId==11 || OneProngChargedPart2PdgId==13) && OneProngChargedPart1PdgId==211) && (Tau1OneProngsSize==2 && Tau2OneProngsSize==3) && (TauMProngEnergy>=0.44 && TauPProngEnergy>=0.55))"
	whh_SM_gen="(OneProngChargedPart2PdgId==-211 && OneProngChargedPart1PdgId==211) && (Tau1OneProngsSize==2 && Tau2OneProngsSize==2) && (TauMProngEnergy>=0.55 && TauPProngEnergy>=0.55)"

	wll_DYandSUSY_gen="(OneProngChargedPart2PdgId==11 || OneProngChargedPart2PdgId==13) && (OneProngChargedPart1PdgId==-11 || OneProngChargedPart1PdgId==-13) && (Tau1OneProngsSize==3 && Tau2OneProngsSize==3) && (TauMProngEnergy>=0.44 && TauPProngEnergy>=0.44)"
	whl_DYandSUSY_gen="((OneProngChargedPart2PdgId==-211 && (OneProngChargedPart1PdgId==-11 || OneProngChargedPart1PdgId==-13)) && (Tau1OneProngsSize==3 && Tau2OneProngsSize==2) && (TauMProngEnergy>=0.55 && TauPProngEnergy>=0.44)) || (((OneProngChargedPart2PdgId==11 || OneProngChargedPart2PdgId==13) && OneProngChargedPart1PdgId==211) && (Tau1OneProngsSize==2 && Tau2OneProngsSize==3) && (TauMProngEnergy>=0.44 && TauPProngEnergy>=0.55))"
	whh_DYandSUSY_gen="(OneProngChargedPart2PdgId==-211 && OneProngChargedPart1PdgId==211) && (Tau1OneProngsSize==2 && Tau2OneProngsSize==2) && (TauMProngEnergy>=0.55 && TauPProngEnergy>=0.55)"

	# reco weights
	wll_reco="1"
	whl_reco="decayMode_1==0 || decayMode_2==0"
	whh_reco="decayMode_1==0 && decayMode_2==0"

	w_SM_gen=[wll_SM_gen, whl_SM_gen, whh_SM_gen]
	w_DYandSUSY_gen=[wll_DYandSUSY_gen, whl_DYandSUSY_gen, whh_DYandSUSY_gen]
	w_reco=[wll_reco, whl_reco, whh_reco]

	plot_configs = []
	
	#comparing gen and reco
	for i in xrange(3):
		config = jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/reco_CP/recogenPhiStarCP.json"))
		config["files"] = files[i]
		for j in xrange(3):
			config["filename"] = "recogenPhiStarCP_"+samples[i]+"_"+channels[j]
			config["directories"] = args.input
			config["folders"] = [folders_gen, folders_reco[j]]
			config["texts"] = texts[j]
			if (samples[i]=="SM"):
				config["weights"] = [w_SM_gen[j], w_reco[j]]
			else:
				config["weights"] = [w_DYandSUSY_gen[j], w_reco[j]]
			plot_configs.append(config.copy())

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

