#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make VBF Htt 125 sync plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-1", nargs="*",
	                    default=["$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/SyncNtuples_KIT/SYNCFILE_VBF_HToTauTau_M-125_2012.root"],
	                    help="KIT input file. [Default: %(default)s]")
	parser.add_argument("--input-2-em",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/SyncNtuples_IC/SYNCFILE_VBF_HToTauTau_M-125_em_2012.root",
	                    help="IC input file (EM channel). [Default: %(default)s]")
	parser.add_argument("--input-2-et",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/SyncNtuples_IC/SYNCFILE_VBF_HToTauTau_M-125_et_2012.root",
	                    help="IC input file (ET channel). [Default: %(default)s]")
	parser.add_argument("--input-2-mt",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/SyncNtuples_IC/SYNCFILE_VBF_HToTauTau_M-125_mt_2012.root",
	                    help="IC input file (MT channel). [Default: %(default)s]")
	parser.add_argument("--input-2-tt",
	                    default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/auxiliaries/SyncNtuples_MIT/htt_vbf_tt_sm_125_select.root",
	                    help="MIT input file (MT channel). [Default: %(default)s]")
	parser.add_argument("--channels", nargs="*",
	                    default=["em", "et", "mt", "tt"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
	                    default=["inclusive", "eventsoverlap",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2",
	                             "mvis", "pt_sv", "eta_sv", "phi_sv", "m_sv",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njets", "mjj", "jdeta",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	                    
	
	args = vars(parser.parse_args())
	logger.initLogger(args)
	
	failed_plots = []
	for channel in args["channels"]:
		for quantity in args["quantities"]:
			json_exists = True
			json_config = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/sync_exercise/%s_%s.json" % (channel, quantity))
			if not os.path.exists(json_config):
				json_exists = False
				json_config = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/sync_exercise/%s_default.json" % (channel))
			
			plot_args = "--json-defaults %s -i %s %s %s --formats png --plot-modules PlotRootHtt %s" % (json_config, " ".join(args["input_1"]), args["input_2_%s" % channel], ("" if json_exists else ("-x %s" % quantity)), ("" if quantity != "eventsoverlap" else ("--analysis-modules EventSelectionOverlap")))
			plot_args = os.path.expandvars(plot_args)
			
			log.info("\nhiggsplot.py %s" % plot_args)
			
			try:
				higgsplot.higgs_plot(plot_args)
			except Exception, e:
				log.info(str(e))
				failed_plots.append(plot_args)
	
	if len(failed_plots) > 0:
		log.error("%d failed plots:\n\thiggsplot.py %s" % (len(failed_plots), "\n\thiggsplot.py ".join(failed_plots)))

