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
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: identification weights (MT channel, Medium muon ID, Data2015D, MC 	Spring15DR74)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-n", "--histogram-name", default="identificationEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationWeights_Data2015D_Spring15DR74Simulation_muon_MediumID.root",
	                    help="Output ROOT file. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	input_file = os.path.join(args.input_dir,"MuonID_Z_RunD_Reco74X_Nov20.root")
	input_path = "NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1/pt_abseta_ratio"

	with tfilecontextmanager.TFileContextManager(input_file, "READ") as root_file:
		elements = roottools.RootTools.walk_root_directory(root_file)
		for key, path in elements:
			if path == input_path:
				temp_th2f = root_file.Get(path).Clone()

				root_file = ROOT.TFile(args.output, "RECREATE")
				pt_bins = array.array("d", [20.0, 25.0, 30.0, 40.0, 50.0, 60.0, 1000.0])
				eta_bins = array.array("d", [-2.4, -2.1, -1.2, -0.9, 0.0, 0.9, 1.2, 2.1, 2.4])
				histogram = ROOT.TH2F(args.histogram_name, args.histogram_name,
	                      len(pt_bins)-1, pt_bins, len(eta_bins)-1, eta_bins)
	
				# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonReferenceEffsRun2
				histogram.SetBinContent(histogram.FindBin(20.0, 0.0), temp_th2f.GetBinContent(temp_th2f.FindBin(20.0, 0.0)))	
				histogram.SetBinContent(histogram.FindBin(25.0, 0.0), temp_th2f.GetBinContent(temp_th2f.FindBin(25.0, 0.0)))
				histogram.SetBinContent(histogram.FindBin(30.0, 0.0), temp_th2f.GetBinContent(temp_th2f.FindBin(30.0, 0.0)))
				histogram.SetBinContent(histogram.FindBin(40.0, 0.0), temp_th2f.GetBinContent(temp_th2f.FindBin(40.0, 0.0)))
				histogram.SetBinContent(histogram.FindBin(50.0, 0.0), temp_th2f.GetBinContent(temp_th2f.FindBin(50.0, 0.0)))
				histogram.SetBinContent(histogram.FindBin(60.0, 0.0), temp_th2f.GetBinContent(temp_th2f.FindBin(60.0, 0.0)))
				
				histogram.SetBinContent(histogram.FindBin(20.0, 0.9), temp_th2f.GetBinContent(temp_th2f.FindBin(20.0, 0.9)))	
				histogram.SetBinContent(histogram.FindBin(25.0, 0.9), temp_th2f.GetBinContent(temp_th2f.FindBin(25.0, 0.9)))
				histogram.SetBinContent(histogram.FindBin(30.0, 0.9), temp_th2f.GetBinContent(temp_th2f.FindBin(30.0, 0.9)))
				histogram.SetBinContent(histogram.FindBin(40.0, 0.9), temp_th2f.GetBinContent(temp_th2f.FindBin(40.0, 0.9)))
				histogram.SetBinContent(histogram.FindBin(50.0, 0.9), temp_th2f.GetBinContent(temp_th2f.FindBin(50.0, 0.9)))
				histogram.SetBinContent(histogram.FindBin(60.0, 0.9), temp_th2f.GetBinContent(temp_th2f.FindBin(60.0, 0.9)))

				histogram.SetBinContent(histogram.FindBin(20.0, 1.2), temp_th2f.GetBinContent(temp_th2f.FindBin(20.0, 1.2)))	
				histogram.SetBinContent(histogram.FindBin(25.0, 1.2), temp_th2f.GetBinContent(temp_th2f.FindBin(25.0, 1.2)))
				histogram.SetBinContent(histogram.FindBin(30.0, 1.2), temp_th2f.GetBinContent(temp_th2f.FindBin(30.0, 1.2)))
				histogram.SetBinContent(histogram.FindBin(40.0, 1.2), temp_th2f.GetBinContent(temp_th2f.FindBin(40.0, 1.2)))
				histogram.SetBinContent(histogram.FindBin(50.0, 1.2), temp_th2f.GetBinContent(temp_th2f.FindBin(50.0, 1.2)))
				histogram.SetBinContent(histogram.FindBin(60.0, 1.2), temp_th2f.GetBinContent(temp_th2f.FindBin(60.0, 1.2)))
				
				histogram.SetBinContent(histogram.FindBin(20.0, 2.1), temp_th2f.GetBinContent(temp_th2f.FindBin(20.0, 2.1)))	
				histogram.SetBinContent(histogram.FindBin(25.0, 2.1), temp_th2f.GetBinContent(temp_th2f.FindBin(25.0, 2.1)))
				histogram.SetBinContent(histogram.FindBin(30.0, 2.1), temp_th2f.GetBinContent(temp_th2f.FindBin(30.0, 2.1)))
				histogram.SetBinContent(histogram.FindBin(40.0, 2.1), temp_th2f.GetBinContent(temp_th2f.FindBin(40.0, 2.1)))
				histogram.SetBinContent(histogram.FindBin(50.0, 2.1), temp_th2f.GetBinContent(temp_th2f.FindBin(50.0, 2.1)))
				histogram.SetBinContent(histogram.FindBin(60.0, 2.1), temp_th2f.GetBinContent(temp_th2f.FindBin(60.0, 2.1)))


				histogram.SetBinError(histogram.FindBin(20.0, 0.0), temp_th2f.GetBinError(temp_th2f.FindBin(20.0, 0.0)))	
				histogram.SetBinError(histogram.FindBin(25.0, 0.0), temp_th2f.GetBinError(temp_th2f.FindBin(25.0, 0.0)))
				histogram.SetBinError(histogram.FindBin(30.0, 0.0), temp_th2f.GetBinError(temp_th2f.FindBin(30.0, 0.0)))
				histogram.SetBinError(histogram.FindBin(40.0, 0.0), temp_th2f.GetBinError(temp_th2f.FindBin(40.0, 0.0)))
				histogram.SetBinError(histogram.FindBin(50.0, 0.0), temp_th2f.GetBinError(temp_th2f.FindBin(50.0, 0.0)))
				histogram.SetBinError(histogram.FindBin(60.0, 0.0), temp_th2f.GetBinError(temp_th2f.FindBin(60.0, 0.0)))
				
				histogram.SetBinError(histogram.FindBin(20.0, 0.9), temp_th2f.GetBinError(temp_th2f.FindBin(20.0, 0.9)))	
				histogram.SetBinError(histogram.FindBin(25.0, 0.9), temp_th2f.GetBinError(temp_th2f.FindBin(25.0, 0.9)))
				histogram.SetBinError(histogram.FindBin(30.0, 0.9), temp_th2f.GetBinError(temp_th2f.FindBin(30.0, 0.9)))
				histogram.SetBinError(histogram.FindBin(40.0, 0.9), temp_th2f.GetBinError(temp_th2f.FindBin(40.0, 0.9)))
				histogram.SetBinError(histogram.FindBin(50.0, 0.9), temp_th2f.GetBinError(temp_th2f.FindBin(50.0, 0.9)))
				histogram.SetBinError(histogram.FindBin(60.0, 0.9), temp_th2f.GetBinError(temp_th2f.FindBin(60.0, 0.9)))

				histogram.SetBinError(histogram.FindBin(20.0, 1.2), temp_th2f.GetBinError(temp_th2f.FindBin(20.0, 1.2)))	
				histogram.SetBinError(histogram.FindBin(25.0, 1.2), temp_th2f.GetBinError(temp_th2f.FindBin(25.0, 1.2)))
				histogram.SetBinError(histogram.FindBin(30.0, 1.2), temp_th2f.GetBinError(temp_th2f.FindBin(30.0, 1.2)))
				histogram.SetBinError(histogram.FindBin(40.0, 1.2), temp_th2f.GetBinError(temp_th2f.FindBin(40.0, 1.2)))
				histogram.SetBinError(histogram.FindBin(50.0, 1.2), temp_th2f.GetBinError(temp_th2f.FindBin(50.0, 1.2)))
				histogram.SetBinError(histogram.FindBin(60.0, 1.2), temp_th2f.GetBinError(temp_th2f.FindBin(60.0, 1.2)))
				
				histogram.SetBinError(histogram.FindBin(20.0, 2.1), temp_th2f.GetBinError(temp_th2f.FindBin(20.0, 2.1)))	
				histogram.SetBinError(histogram.FindBin(25.0, 2.1), temp_th2f.GetBinError(temp_th2f.FindBin(25.0, 2.1)))
				histogram.SetBinError(histogram.FindBin(30.0, 2.1), temp_th2f.GetBinError(temp_th2f.FindBin(30.0, 2.1)))
				histogram.SetBinError(histogram.FindBin(40.0, 2.1), temp_th2f.GetBinError(temp_th2f.FindBin(40.0, 2.1)))
				histogram.SetBinError(histogram.FindBin(50.0, 2.1), temp_th2f.GetBinError(temp_th2f.FindBin(50.0, 2.1)))
				histogram.SetBinError(histogram.FindBin(60.0, 2.1), temp_th2f.GetBinError(temp_th2f.FindBin(60.0, 2.1)))
				
				# fill histograms symmetrically in eta
				for pt_bin in xrange(1, len(pt_bins)+1):
					for eta_bin in xrange(1, (len(pt_bins)/2)+2):
						histogram.SetBinContent(pt_bin, eta_bin, histogram.GetBinContent(pt_bin, len(eta_bins)-eta_bin))
						histogram.SetBinError(pt_bin, eta_bin, histogram.GetBinError(pt_bin, len(eta_bins)-eta_bin))

	args.output = os.path.expandvars(args.output)
	dirname = os.path.dirname(args.output)
	if dirname != "" and not os.path.exists(dirname):
		os.makedirs(dirname)

	
	#histogram.Write()
	root_file.Write()
	root_file.Close()
	log.info("Correction factors have been stored in histogram \"%s/%s\"." % (args.output, args.histogram_name))

