#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import HiggsAnalysis.KITHiggsToTauTau.triggerTurnOnParametrisation as triggerTurnOnParametrisation


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: trigger efficiencies (Tau Trigger for ET channel, Data2012ABCD)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="triggerEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_IsoMu18_SimulationSpring15MiniAOD_Asympt25ns.root",
	                    help="Output ROOT file. [Default: %(default)s]")
	
	parser.add_argument("--n-bins-pt", type=int, default=300,
	                    help="Number of pt bins. [Default: %(default)s]")
	parser.add_argument("--min-pt", type=float, default=0.0,
	                    help="Minium pt. [Default: %(default)s]")
	parser.add_argument("--max-pt", type=float, default=300.0,
	                    help="Maxium pt. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_Muon_Tau_Trigger
	# http://benitezj.web.cern.ch/benitezj/Summer13Studies/TauTrigger/eTauABCD_June28/results.txt
	# http://benitezj.web.cern.ch/benitezj/Summer13Studies/TauTrigger/eTauABCD_June30/results.txt
	# https://github.com/ajgilbert/ICHiggsTauTau/blob/cdfcbf79abd54d53f4751a71efb0b4807ed34bdc/Analysis/HiggsTauTau/src/HTTWeights.cc#L282-L372
	# 2015: Parameterization by Michal Bluj (Oct 2015)
	eta_border_barrel = 0.8
	eta_border_endcap = 1.2
	eta_bins_with_parameters = [
		[
			-2.1,
			-eta_border_endcap,
			[9.78, 7.59, 8.67, 5.72, 0.9481],
		],
		[
			-eta_border_endcap,
			-eta_border_barrel,
			[8.81, 6.18, 4.19, 133.46, 0.9155],
		],
		[
			-eta_border_barrel,
			eta_border_barrel,
			[10.20, 9.14, 9.35, 142.99, 0.9553],
		],
		[
			eta_border_barrel,
			eta_border_endcap,
			[8.81, 6.18, 4.19, 133.46, 0.9155],
		],
		[
			eta_border_endcap,
			2.1,
			[9.78, 7.59, 8.67, 5.72, 0.9481],
		],
	]
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)
	
	root_file = ROOT.TFile(args.output, "RECREATE")
	histogram = triggerTurnOnParametrisation.fill_root_histogram(args.n_bins_pt, args.min_pt, args.max_pt,
	                                                             eta_bins_with_parameters, args.histogram_name)
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

