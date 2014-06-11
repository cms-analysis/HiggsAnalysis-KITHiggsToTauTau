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

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: trigger efficiencies (IsoMu17, Data2012ABCD)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="triggerEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerEfficiency_IsoMu17_Data2012ABCD.root",
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
			"parameters" : [15.9977, 7.64004e-05, 6.4951e-08, 1.57403, 0.865325],
		},
		{
			"low" : -1.2,
			"high" : -0.8,
			"parameters" : [17.3974, 0.804001, 1.47145, 1.24295, 0.928198],
		},
		{
			"low" : -0.8,
			"high" : 0.0,
			"parameters" : [16.4307, 0.226312, 0.265553, 1.55756, 0.974462],
		},
		{
			"low" : 0.0,
			"high" : 0.8,
			"parameters" : [17.313, 0.662731, 1.3412, 1.05778, 1.26624],
		},
		{
			"low" : 0.8,
			"high" : 1.2,
			"parameters" : [16.9966, 0.550532, 0.807863, 1.55402, 0.885134],
		},
		{
			"low" : 1.2,
			"high" : 10.0,
			"parameters" : [15.9962, 0.000106195, 4.95058e-08, 1.9991, 0.851294],
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

