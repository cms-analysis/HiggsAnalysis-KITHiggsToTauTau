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

	parser = argparse.ArgumentParser(description="Store correction factors in ROOT histograms. Here: trigger efficiencies (Tau Trigger for ET channel (without ES correction), MC53X)",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-n", "--histogram-name", default="triggerEfficiency",
	                    help="Histogram name. [Default: %(default)s]")
	parser.add_argument("-o", "--output",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_CaloIdVT_CaloIsoRhoT_TrkIdT_TrkIsoT_LooseIsoPFTau20_MC53X_et_withoutES.root",
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
	# http://benitezj.web.cern.ch/benitezj/Summer13Studies/TauTrigger/eTauABCD_June30/results.txt
	# https://github.com/ajgilbert/ICHiggsTauTau/blob/cdfcbf79abd54d53f4751a71efb0b4807ed34bdc/Analysis/HiggsTauTau/src/HTTWeights.cc#L282-L372
	eta_border_eb_ee = 1.5
	eta_bins_with_parameters = [
		[
			-10.0,
			-eta_border_eb_ee,
			[18.557810, 0.280908, 0.119282, 17.749043, 0.865756],
		],
		[
			-eta_border_eb_ee,
			eta_border_eb_ee,
			[18.605055, 0.264062, 0.139561, 4.792849, 0.915035],
		],
		[
			eta_border_eb_ee,
			10.0,
			[18.557810, 0.280908, 0.119282, 17.749043, 0.865756],
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

