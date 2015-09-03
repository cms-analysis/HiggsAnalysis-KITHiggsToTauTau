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

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: identification efficiencies (EM channel, muon, Data2012ABCD)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="identificationEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Data2012ABCD_em_muon.root",
	                    help="Output ROOT file. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)

	root_file = ROOT.TFile(args.output, "RECREATE")
	
	pt_bins = array.array("d", [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 1000.0])
	eta_bins = array.array("d", [-2.1, -1.6, -1.2, -0.8, 0.0, 0.8, 1.2, 1.6, 2.1])
	histogram = ROOT.TH2F(args.histogram_name, args.histogram_name,
	                      len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	
	# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Muon_ID_Isolation_EMu_Channel
	# cat test.txt; sed -e "s@\([0-9]\+\.[0-9]\+\).*\([0-9]\+\.[0-9]\+\).*abs.eta.*+/-.*\([0-9]\+\.[0-9]\+\).*+/-.*+/-.*@\thistogram.SetBinContent(histogram.FindBin(\1, \2), \3)@" test.txt
	histogram.SetBinContent(histogram.FindBin(10.0, 0.0), 0.5981)
	histogram.SetBinContent(histogram.FindBin(10.0, 0.8), 0.6578)
	histogram.SetBinContent(histogram.FindBin(10.0, 1.2), 0.6738)
	histogram.SetBinContent(histogram.FindBin(10.0, 1.6), 0.6246)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.0), 0.6740)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.8), 0.7309)
	histogram.SetBinContent(histogram.FindBin(15.0, 1.2), 0.7416)
	histogram.SetBinContent(histogram.FindBin(15.0, 1.6), 0.6954)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.0), 0.7533)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.8), 0.7915)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.2), 0.7997)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.6), 0.7567)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.0), 0.8141)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.8), 0.8364)
	histogram.SetBinContent(histogram.FindBin(25.0, 1.2), 0.8462)
	histogram.SetBinContent(histogram.FindBin(25.0, 1.6), 0.8051)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.0), 0.8606)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.8), 0.8680)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.2), 0.8745)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.6), 0.8399)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.0), 0.9255)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.8), 0.9249)
	histogram.SetBinContent(histogram.FindBin(35.0, 1.2), 0.9291)
	histogram.SetBinContent(histogram.FindBin(35.0, 1.6), 0.9025)
	
	# cat test.txt; sed -e "s@\([0-9]\+\.[0-9]\+\).*\([0-9]\+\.[0-9]\+\).*abs.eta.*+/-.*+/- \([0-9]\+\.[0-9]\+\).*+/-.*@\thistogram.SetBinError(histogram.FindBin(\1, \2), \3)@" test.txt
	histogram.SetBinError(histogram.FindBin(10.0, 0.0), 0.0045)
	histogram.SetBinError(histogram.FindBin(10.0, 0.8), 0.0041)
	histogram.SetBinError(histogram.FindBin(10.0, 1.2), 0.0037)
	histogram.SetBinError(histogram.FindBin(10.0, 1.6), 0.0032)
	histogram.SetBinError(histogram.FindBin(15.0, 0.0), 0.0022)
	histogram.SetBinError(histogram.FindBin(15.0, 0.8), 0.0025)
	histogram.SetBinError(histogram.FindBin(15.0, 1.2), 0.0025)
	histogram.SetBinError(histogram.FindBin(15.0, 1.6), 0.0022)
	histogram.SetBinError(histogram.FindBin(20.0, 0.0), 0.0012)
	histogram.SetBinError(histogram.FindBin(20.0, 0.8), 0.0016)
	histogram.SetBinError(histogram.FindBin(20.0, 1.2), 0.0016)
	histogram.SetBinError(histogram.FindBin(20.0, 1.6), 0.0014)
	histogram.SetBinError(histogram.FindBin(25.0, 0.0), 0.0007)
	histogram.SetBinError(histogram.FindBin(25.0, 0.8), 0.0010)
	histogram.SetBinError(histogram.FindBin(25.0, 1.2), 0.0009)
	histogram.SetBinError(histogram.FindBin(25.0, 1.6), 0.0009)
	histogram.SetBinError(histogram.FindBin(30.0, 0.0), 0.0004)
	histogram.SetBinError(histogram.FindBin(30.0, 0.8), 0.0007)
	histogram.SetBinError(histogram.FindBin(30.0, 1.2), 0.0007)
	histogram.SetBinError(histogram.FindBin(30.0, 1.6), 0.0010)
	histogram.SetBinError(histogram.FindBin(35.0, 0.0), 0.0004)
	histogram.SetBinError(histogram.FindBin(35.0, 0.8), 0.0002)
	histogram.SetBinError(histogram.FindBin(35.0, 1.2), 0.0002)
	histogram.SetBinError(histogram.FindBin(35.0, 1.6), 0.0002)
	
	# fill histograms symmetrically in eta
	for pt_bin in xrange(1, len(pt_bins)+1):
		for eta_bin in xrange(1, (len(pt_bins)/2)+2):
			histogram.SetBinContent(pt_bin, eta_bin, histogram.GetBinContent(pt_bin, len(eta_bins)-eta_bin))
			histogram.SetBinError(pt_bin, eta_bin, histogram.GetBinError(pt_bin, len(eta_bins)-eta_bin))
	
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

