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

	parser = argparse.ArgumentParser(description="Store anti-electron discriminator correction factors in ROOT histograms.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/antiElectronDiscrMVA6FakeRateWeights.root",
	                    help="Output ROOT file. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)

	root_file = ROOT.TFile(args.output, "RECREATE")
	eta_bins = array.array("d", [0.0, 1.5, 2.3])
	
	histoVLooseWP = ROOT.TH1F("antiEVLoose", "antiEVLoose", len(eta_bins)-1, eta_bins)
	histoVLooseWP.SetBinContent(1, 1.05)  # barrel
	histoVLooseWP.SetBinContent(2, 1.05) # endcap
	
	histoLooseWP = ROOT.TH1F("antiELoose", "antiELoose", len(eta_bins)-1, eta_bins)
	histoLooseWP.SetBinContent(1, 1.14)  # barrel
	histoLooseWP.SetBinContent(2, 1.08)  # endcap
	
	histoMediumWP = ROOT.TH1F("antiEMedium", "antiEMedium", len(eta_bins)-1, eta_bins)
	histoMediumWP.SetBinContent(1, 1.50)  # barrel
	histoMediumWP.SetBinContent(2, 1.06) # endcap
	
	histoTightWP = ROOT.TH1F("antiETight", "antiETight", len(eta_bins)-1, eta_bins)
	histoTightWP.SetBinContent(1, 1.80)  # barrel
	histoTightWP.SetBinContent(2, 1.30)  # endcap
	
	histoVTightWP = ROOT.TH1F("antiEVTight", "antiEVTight", len(eta_bins)-1, eta_bins)
	histoVTightWP.SetBinContent(1, 1.89) # barrel
	histoVTightWP.SetBinContent(2, 1.69) # endcap
	
	root_file.Write()
	root_file.Close()
	
	log.info("Correction factors have been stored in file \"%s\"." % (args.output))
