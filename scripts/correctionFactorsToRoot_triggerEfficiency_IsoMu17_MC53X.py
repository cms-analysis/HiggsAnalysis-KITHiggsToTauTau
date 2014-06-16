#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import HiggsAnalysis.KITHiggsToTauTau.triggerTurnOnParametrisation as triggerTurnOnParametrisation


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: trigger efficiencies (IsoMu17, MC53X)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="triggerEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_IsoMu17_MC53X.root",
	                    help="Output ROOT file. [Default: %(default)s]")
	
	parser.add_argument("--n-bins-pt", type=int, default=200,
	                    help="Number of pt bins. [Default: %(default)s]")
	parser.add_argument("--min-pt", type=float, default=0.0,
	                    help="Minium pt. [Default: %(default)s]")
	parser.add_argument("--max-pt", type=float, default=200.0,
	                    help="Maxium pt. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	eta_bins_with_parameters = [
		{
			"low" : -10.0,
			"high" : -1.2,
			"parameters" : [16.0051, 2.45144e-05, 4.3335e-09, 1.66134, 0.87045],
		},
		{
			"low" : -1.2,
			"high" : -0.8,
			"parameters" : [17.3135, 0.747636, 1.21803, 1.40611, 0.934983],
		},
		{
			"low" : -0.8,
			"high" : 0.0,
			"parameters" : [15.9556, 0.0236127, 0.00589832, 1.75409, 0.981338],
		},
		{
			"low" : 0.0,
			"high" : 0.8,
			"parameters" : [15.9289, 0.0271317, 0.00448573, 1.92101, 0.978625],
		},
		{
			"low" : 0.8,
			"high" : 1.2,
			"parameters" : [16.5678, 0.328333, 0.354533, 1.67085, 0.916992],
		},
		{
			"low" : 1.2,
			"high" : 10.0,
			"parameters" : [15.997, 7.90069e-05, 4.40036e-08, 1.66272, 0.884502],
		},
	]
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)
	
	root_file = ROOT.TFile(args.output, "RECREATE")
	histogram = triggerTurnOnParametrisation.fill_root_histogram(args.n_bins_pt, args.min_pt, args.max_pt,
	                                                             eta_bins_with_parameters, args.histogram_name)
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

