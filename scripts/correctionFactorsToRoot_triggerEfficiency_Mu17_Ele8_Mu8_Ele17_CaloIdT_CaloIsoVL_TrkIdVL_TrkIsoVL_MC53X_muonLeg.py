#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import array
import argparse
import os

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: trigger efficiencies (Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL / Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL, MC53X)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="triggerEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Mu17_Ele8_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_MC53X_muonLeg.root",
	                    help="Output ROOT file. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)

	root_file = ROOT.TFile(args.output, "RECREATE")
	
	# https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorkingSummer2013#Electron_Muon_Trigger
	# https://svnweb.cern.ch/cern/wsvn/desycmshiggs/HiggsToTauTau/trunk/DesyHTauTau/HTauTauElecMuonAnalysis/bin/FillTriggerEfficiencyMap.C
	pt_bins = array.array("d", [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 1000.0])
	eta_bins = array.array("d", [-2.1, -1.6, -1.2, -0.8, 0.0, 0.8, 1.2, 1.6, 2.1])
	histogram = ROOT.TH2F(args.histogram_name, args.histogram_name,
	                      len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	
	histogram.SetBinContent(histogram.FindBin(10.0, 0.0), 0.9870)
	histogram.SetBinContent(histogram.FindBin(10.0, 0.8), 0.9666)
	histogram.SetBinContent(histogram.FindBin(10.0, 1.2), 0.9357)
	histogram.SetBinContent(histogram.FindBin(10.0, 1.6), 0.9415)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.0), 0.9868)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.8), 0.9445)
	histogram.SetBinContent(histogram.FindBin(15.0, 1.2), 0.9512)
	histogram.SetBinContent(histogram.FindBin(15.0, 1.6), 0.9638)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.0), 0.9812)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.8), 0.9822)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.2), 0.9640)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.6), 0.9657)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.0), 0.9853)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.8), 0.9618)
	histogram.SetBinContent(histogram.FindBin(25.0, 1.2), 0.9538)
	histogram.SetBinContent(histogram.FindBin(25.0, 1.6), 0.9287)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.0), 0.9826)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.8), 0.9454)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.2), 0.9247)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.6), 0.9573)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.0), 0.9692)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.8), 0.9759)
	histogram.SetBinContent(histogram.FindBin(35.0, 1.2), 0.9522)
	histogram.SetBinContent(histogram.FindBin(35.0, 1.6), 0.9606)
	
	histogram.SetBinError(histogram.FindBin(10.0, 0.0), 0.0048)
	histogram.SetBinError(histogram.FindBin(10.0, 0.8), 0.0104)
	histogram.SetBinError(histogram.FindBin(10.0, 1.2), 0.0136)
	histogram.SetBinError(histogram.FindBin(10.0, 1.6), 0.0140)
	histogram.SetBinError(histogram.FindBin(15.0, 0.0), 0.0046)
	histogram.SetBinError(histogram.FindBin(15.0, 0.8), 0.0149)
	histogram.SetBinError(histogram.FindBin(15.0, 1.2), 0.0155)
	histogram.SetBinError(histogram.FindBin(15.0, 1.6), 0.0133)
	histogram.SetBinError(histogram.FindBin(20.0, 0.0), 0.0053)
	histogram.SetBinError(histogram.FindBin(20.0, 0.8), 0.0097)
	histogram.SetBinError(histogram.FindBin(20.0, 1.2), 0.0123)
	histogram.SetBinError(histogram.FindBin(20.0, 1.6), 0.0131)
	histogram.SetBinError(histogram.FindBin(25.0, 0.0), 0.0067)
	histogram.SetBinError(histogram.FindBin(25.0, 0.8), 0.0170)
	histogram.SetBinError(histogram.FindBin(25.0, 1.2), 0.0163)
	histogram.SetBinError(histogram.FindBin(25.0, 1.6), 0.0214)
	histogram.SetBinError(histogram.FindBin(30.0, 0.0), 0.0078)
	histogram.SetBinError(histogram.FindBin(30.0, 0.8), 0.0202)
	histogram.SetBinError(histogram.FindBin(30.0, 1.2), 0.0234)
	histogram.SetBinError(histogram.FindBin(30.0, 1.6), 0.0289)
	histogram.SetBinError(histogram.FindBin(35.0, 0.0), 0.0083)
	histogram.SetBinError(histogram.FindBin(35.0, 0.8), 0.0166)
	histogram.SetBinError(histogram.FindBin(35.0, 1.2), 0.0206)
	histogram.SetBinError(histogram.FindBin(35.0, 1.6), 0.0208)
	
	# fill histograms symmetrically in eta
	for pt_bin in xrange(1, len(pt_bins)+1):
		for eta_bin in xrange(1, (len(pt_bins)/2)+2):
			histogram.SetBinContent(pt_bin, eta_bin, histogram.GetBinContent(pt_bin, len(eta_bins)-eta_bin))
			histogram.SetBinError(pt_bin, eta_bin, histogram.GetBinError(pt_bin, len(eta_bins)-eta_bin))
	
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

