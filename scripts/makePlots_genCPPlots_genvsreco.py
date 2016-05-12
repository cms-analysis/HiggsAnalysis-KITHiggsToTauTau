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

	w_reco_dy1=["((OneProngChargedPart1PdgId == -11 && OneProngChargedPart2PdgId == 13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
	w_reco_dy4=["((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
	w_reco_dy3=["(abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 13 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
	w_reco_dy2=["(abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]


	w_em=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId == 13 && OneProngChargedPart2PdgId == -11) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
	w_et=[" tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       " tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       " tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       " tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       " tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
	w_mt=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44)))"]
	w_tt=["( tauSpinnerWeight000 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight025 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight050 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight075 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))",
       "( tauSpinnerWeight100 * tauSpinnerWeightInvSample * ((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55)))"]
	
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
	
	
	w_gen_dy1=["((OneProngChargedPart1PdgId == 211 && OneProngChargedPart2PdgId == -211) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
	w_gen_dy2=["((OneProngChargedPart1PdgId != -999 && OneProngChargedPart1PdgId != 11 && OneProngChargedPart1PdgId != 13 && OneProngChargedPart2PdgId != -999 && OneProngChargedPart2PdgId != 11 && OneProngChargedPart2PdgId != 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 2) && (TauMProngEnergy >= 0.55 && TauPProngEnergy >= 0.55))"]
	w_gen_dy3=["((abs(OneProngChargedPart1PdgId) != 999 && abs(OneProngChargedPart1PdgId) != 11 && abs(OneProngChargedPart1PdgId) != 13 && abs(OneProngChargedPart2PdgId) == 11 || abs(OneProngChargedPart2PdgId) == 13) && (Tau1OneProngsSize == 2 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
	w_gen_dy4=["((OneProngChargedPart1PdgId == -11 || OneProngChargedPart1PdgId == -13 && OneProngChargedPart2PdgId == 11 || OneProngChargedPart2PdgId == 13) && (Tau1OneProngsSize == 3 && Tau2OneProngsSize == 3) && (TauMProngEnergy >= 0.44 && TauPProngEnergy >= 0.44))"]
	
	
	
	w_evenandodd_gen=[[w_ll[0],w_gen_dy4],[w_hl[0],w_gen_dy3],[w_hl[0],w_gen_dy3],[w_hh[0],w_gen_dy2]]
	
	w_evenandodd_reco=[[w_em[0],w_reco_dy1],[w_et[0],w_reco_dy2],[w_mt[0],w_reco_dy3],[w_tt[0],w_reco_dy4]]
	
	w_onlychannels=[w_em,w_et,w_mt,w_tt]
	names=["_genvsreco_em","_genvsreco_et","_genvsreco_mt","_genvsreco_tt"]
	names_dy=["_dypipi","_dyhh","_dyhl","_dyll"]
	nicks=["alpha000","alpha025","alpha050","alpha075","alpha100"]
	colors=[ "#ff2400","#0020c2","#4cc417","#a74ac7","#3bb9ff"]	
	colors_evenandodd1=["#ff2400","#3bb9ff","#4cc417"]
	colors_evenandodd2=["#a74ac7","#0020c2","#000000"]
	nicks_evenandodd=["alpha000","alpha100","DYbkg"]
	
	plot_configs = []
	f_reco=["em_jecUncNom/ntuple", "et_jecUncNom_tauEsNom/ntuple", "mt_jecUncNom_tauEsNom/ntuple", "tt_jecUncNom_tauEsNom/ntuple"]
	f_gen=["gen/ntuple","gen/ntuple","gen/ntuple","gen/ntuple"]
	
	#only CP-even and CP-odd in 1 plot with SUSY
	for j in xrange(4):	
		config2=jsonTools.JsonDict(os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/gen_CP/phiCPevenandodd_genvsreco.json"))		
		config2["folders"]= [f_gen[j],f_gen[j],f_reco[j],f_reco[j]]	
		config2["colors"]=[colors_evenandodd1,colors_evenandodd2]
		config2["filename"]= "genPhiCPonlyevenandodd" + names[j]
		config2["nicks"]=["alpha000gen","alpha100gen","alpha000reco","alpha100reco"]
		config2["weights"]=[w_evenandodd_gen[j],w_evenandodd_reco[j]]
		config2["directories"] = args.input
		config2["files"]=["GluGluHToTauTauM*/*.root VBFH*/*.root W*HToTauTauM*/*.root ZH*/*.root","SUSY*/*.root","GluGluHToTauTauM*/*.root VBFH*/*.root W*HToTauTauM*/*.root ZH*/*.root","SUSY*/*.root"]
		plot_configs.append(config2)
	
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
