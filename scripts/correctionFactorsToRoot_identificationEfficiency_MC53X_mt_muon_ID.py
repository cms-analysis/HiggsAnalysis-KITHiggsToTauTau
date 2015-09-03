#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import argparse
import os

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: identification efficiencies (MT channel, muon ID, MC53X)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="identificationEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC53X_mt_muon_ID.root",
	                    help="Output ROOT file. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)

	root_file = ROOT.TFile(args.output, "RECREATE")
	
	pt_bins = array.array("d", [20.0, 30.0, 1000.0])
	eta_bins = array.array("d", [-2.1, -1.2, -0.8, 0.0, 0.8, 1.2, 2.1])
	histogram = ROOT.TH2F(args.histogram_name, args.histogram_name,
	                      len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	
	# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Muon_ID_Isolation_MuTau_Channel
	histogram.SetBinContent(histogram.FindBin(20.0, 0.0), 0.9647)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.8), 0.9586)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.2), 0.9511)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.0), 0.9631)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.8), 0.9578)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.2), 0.9490)
	
	histogram.SetBinError(histogram.FindBin(20.0, 0.0), 0.0004)
	histogram.SetBinError(histogram.FindBin(20.0, 0.8), 0.0006)
	histogram.SetBinError(histogram.FindBin(20.0, 1.2), 0.0005)
	histogram.SetBinError(histogram.FindBin(30.0, 0.0), 0.0001)
	histogram.SetBinError(histogram.FindBin(30.0, 0.8), 0.0001)
	histogram.SetBinError(histogram.FindBin(30.0, 1.2), 0.0001)
	
	# fill histograms symmetrically in eta
	for pt_bin in xrange(1, len(pt_bins)+1):
		for eta_bin in xrange(1, (len(pt_bins)/2)+2):
			histogram.SetBinContent(pt_bin, eta_bin, histogram.GetBinContent(pt_bin, len(eta_bins)-eta_bin))
			histogram.SetBinError(pt_bin, eta_bin, histogram.GetBinError(pt_bin, len(eta_bins)-eta_bin))
	
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

