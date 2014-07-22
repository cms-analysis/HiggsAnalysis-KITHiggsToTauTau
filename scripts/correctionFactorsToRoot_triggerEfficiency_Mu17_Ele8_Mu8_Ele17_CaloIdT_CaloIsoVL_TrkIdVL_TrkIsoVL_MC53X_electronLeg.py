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

import HiggsAnalysis.KITHiggsToTauTau.triggerTurnOnParametrisation as triggerTurnOnParametrisation


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: trigger efficiencies (Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL / Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL, MC53X)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="triggerEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Mu17_Ele8_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_MC53X_electronLeg.root",
	                    help="Output ROOT file. [Default: %(default)s]")
	
	parser.add_argument("--n-bins-pt", type=int, default=300,
	                    help="Number of pt bins. [Default: %(default)s]")
	parser.add_argument("--min-pt", type=float, default=0.0,
	                    help="Minium pt. [Default: %(default)s]")
	parser.add_argument("--max-pt", type=float, default=300.0,
	                    help="Maxium pt. [Default: %(default)s]")

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
	eta_bins = array.array("d", [-2.3, -1.5, -0.8, 0.0, 0.8, 1.5, 2.3])
	histogram = ROOT.TH2F(args.histogram_name, args.histogram_name,
	                      len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	
	histogram.SetBinContent(histogram.FindBin(10.0, 0.0), 0.7615)
	histogram.SetBinContent(histogram.FindBin(10.0, 0.8), 0.8186)
	histogram.SetBinContent(histogram.FindBin(10.0, 1.5), 0.7652)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.0), 0.8903)
	histogram.SetBinContent(histogram.FindBin(15.0, 0.8), 0.9367)
	histogram.SetBinContent(histogram.FindBin(15.0, 1.5), 0.9126)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.0), 0.9419)
	histogram.SetBinContent(histogram.FindBin(20.0, 0.8), 0.9746)
	histogram.SetBinContent(histogram.FindBin(20.0, 1.5), 0.9654)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.0), 0.9591)
	histogram.SetBinContent(histogram.FindBin(25.0, 0.8), 0.9757)
	histogram.SetBinContent(histogram.FindBin(25.0, 1.5), 0.9732)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.0), 0.9454)
	histogram.SetBinContent(histogram.FindBin(30.0, 0.8), 0.9748)
	histogram.SetBinContent(histogram.FindBin(30.0, 1.5), 0.9875)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.0), 0.9629)
	histogram.SetBinContent(histogram.FindBin(35.0, 0.8), 0.9763)
	histogram.SetBinContent(histogram.FindBin(35.0, 1.5), 0.9787)
	
	histogram.SetBinError(histogram.FindBin(10.0, 0.0), 0.0128)
	histogram.SetBinError(histogram.FindBin(10.0, 0.8), 0.0150)
	histogram.SetBinError(histogram.FindBin(10.0, 1.5), 0.0312)
	histogram.SetBinError(histogram.FindBin(15.0, 0.0), 0.0090)
	histogram.SetBinError(histogram.FindBin(15.0, 0.8), 0.0091)
	histogram.SetBinError(histogram.FindBin(15.0, 1.5), 0.0162)
	histogram.SetBinError(histogram.FindBin(20.0, 0.0), 0.0072)
	histogram.SetBinError(histogram.FindBin(20.0, 0.8), 0.0069)
	histogram.SetBinError(histogram.FindBin(20.0, 1.5), 0.0120)
	histogram.SetBinError(histogram.FindBin(25.0, 0.0), 0.0072)
	histogram.SetBinError(histogram.FindBin(25.0, 0.8), 0.0071)
	histogram.SetBinError(histogram.FindBin(25.0, 1.5), 0.0140)
	histogram.SetBinError(histogram.FindBin(30.0, 0.0), 0.0088)
	histogram.SetBinError(histogram.FindBin(30.0, 0.8), 0.0100)
	histogram.SetBinError(histogram.FindBin(30.0, 1.5), 0.0095)
	histogram.SetBinError(histogram.FindBin(35.0, 0.0), 0.0073)
	histogram.SetBinError(histogram.FindBin(35.0, 0.8), 0.0069)
	histogram.SetBinError(histogram.FindBin(35.0, 1.5), 0.0131)
	
	# fill histograms symmetrically in eta
	for pt_bin in xrange(1, len(pt_bins)+1):
		for eta_bin in xrange(1, (len(pt_bins)/2)+2):
			histogram.SetBinContent(pt_bin, eta_bin, histogram.GetBinContent(pt_bin, len(eta_bins)-eta_bin))
			histogram.SetBinError(pt_bin, eta_bin, histogram.GetBinError(pt_bin, len(eta_bins)-eta_bin))
	
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

