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

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: identification efficiencies (EM channel, electron, Data2012ABCD)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="identificationEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Data2012ABCD_em_electron.root",
	                    help="Output ROOT file. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)

	root_file = ROOT.TFile(args.output, "RECREATE")
	
	pt_bins = array.array("d", [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 1000.0])
	eta_bins = array.array("d", [-2.3, -1.5, -0.8, 0.0, 0.8, 1.5, 2.3])
	histogram = ROOT.TH2F(args.histogram_name, args.histogram_name,
	                      len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	
	# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_ID_Isolation_EMu_Channe
	# cat test.txt; sed -e "s@\([0-9]\+\.[0-9]\+\).*\([0-9]\+\.[0-9]\+\).*abs.eta.*+/-.*\([0-9]\+\.[0-9]\+\).*+/-.*+/-.*@\thistogram.SetBinContent(histogram.FindBin(\1, \2), \3)@" test.txt
	histogram.SetBinContent(histogram.FindBin(10.0, 0.0), 0.3436)
	histogram.SetBinContent(histogram.FindBin(10.0, 0.8), 0.3481)
	histogram.SetBinContent(histogram.FindBin(10.0, 1.5), 0.1104)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.0), 0.5196)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.8), 0.5235)
	histogram.SetBinContent(histogram.FindBin(15.0, 1.5), 0.2431)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.0), 0.6442)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.8), 0.5535)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.5), 0.2888)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.0), 0.7191)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.8), 0.6472)
	histogram.SetBinContent(histogram.FindBin(25.0, 1.5), 0.3746)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.0), 0.7819)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.8), 0.7224)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.5), 0.4527)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.0), 0.8650)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.8), 0.8201)
	histogram.SetBinContent(histogram.FindBin(35.0, 1.5), 0.6015)
	
	# cat test.txt; sed -e "s@\([0-9]\+\.[0-9]\+\).*\([0-9]\+\.[0-9]\+\).*abs.eta.*+/-.*+/- \([0-9]\+\.[0-9]\+\).*+/-.*@\thistogram.SetBinError(histogram.FindBin(\1, \2), \3)@" test.txt
	histogram.SetBinError(histogram.FindBin(10.0, 0.0), 0.0057)
	histogram.SetBinError(histogram.FindBin(10.0, 0.8), 0.0068)
	histogram.SetBinError(histogram.FindBin(10.0, 1.5), 0.0020)
	histogram.SetBinError(histogram.FindBin(15.0, 0.0), 0.0017)
	histogram.SetBinError(histogram.FindBin(15.0, 0.8), 0.0032)
	histogram.SetBinError(histogram.FindBin(15.0, 1.5), 0.0021)
	histogram.SetBinError(histogram.FindBin(20.0, 0.0), 0.0010)
	histogram.SetBinError(histogram.FindBin(20.0, 0.8), 0.0022)
	histogram.SetBinError(histogram.FindBin(20.0, 1.5), 0.0019)
	histogram.SetBinError(histogram.FindBin(25.0, 0.0), 0.0011)
	histogram.SetBinError(histogram.FindBin(25.0, 0.8), 0.0007)
	histogram.SetBinError(histogram.FindBin(25.0, 1.5), 0.0003)
	histogram.SetBinError(histogram.FindBin(30.0, 0.0), 0.0001)
	histogram.SetBinError(histogram.FindBin(30.0, 0.8), 0.0001)
	histogram.SetBinError(histogram.FindBin(30.0, 1.5), 0.0011)
	histogram.SetBinError(histogram.FindBin(35.0, 0.0), 0.0000)
	histogram.SetBinError(histogram.FindBin(35.0, 0.8), 0.0000)
	histogram.SetBinError(histogram.FindBin(35.0, 1.5), 0.0001)
	
	# fill histograms symmetrically in eta
	for pt_bin in xrange(1, len(pt_bins)+1):
		for eta_bin in xrange(1, (len(pt_bins)/2)+2):
			histogram.SetBinContent(pt_bin, eta_bin, histogram.GetBinContent(pt_bin, len(eta_bins)-eta_bin))
			histogram.SetBinError(pt_bin, eta_bin, histogram.GetBinError(pt_bin, len(eta_bins)-eta_bin))
	
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

