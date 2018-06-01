#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys
import re

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2017 as samples

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=False,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zll", "ttj", "vv", "wj", "qcd", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity", default=["genBosonTau1VisibleLV.Pt()", "genBosonTau2VisibleLV.Pt()"],
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["et"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-w", "--weights", default=["1.0"], nargs="+",
	                    help="Additional weight (cut) expressions. The list of weigths is repeated until it matches the number of quantities [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("--smhtt", default=False, action="store_true",
	                    help="Produce the plots for the SM HTT analysis. [Default: %(default)s]")
	parser.add_argument("--cp", default=False, action="store_true",
	                    help="Produce the plots for the CP analysis. [Default: %(default)s]")  #TODO instead of 3 different boolean flag, change to option with 3 possible values
	parser.add_argument("--input-files", required=False,
	                    help="Input directory.")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("--ratio-subplot", default=False, action="store_true",
	                    help="Add a subplot showing the relative fraction of the processes per bin. [Default: %(default)s]")						
	parser.add_argument("--shapes", default=False, action="store_true",
	                    help="Show shape comparisons. [Default: %(default)s]")
	parser.add_argument("--channel-comparison", default=False, action="store_true",
	                    help="Show channel comparisons. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-b", "--batch", default=None, const="rwthcondor", nargs="?",
	                    help="Run with grid-control. Optionally select backend. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/trigger/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--filename",
	                    default=None,
	                    help="Output filename. [Default: x_expression]")
	parser.add_argument("--www", nargs="?", default=None,
	                    help="Publish plots. [Default: %(default)s]")
	parser.add_argument("--labels", default=["no trigger cuts"], nargs="+",
	                    help="Additional weight (cut) expressions. The list of weigths is repeated until it matches the number of quantities [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	plot_configs = []

	if args.input_dir == None and args.input_files == None:
		log.abort("no input file")

	print args.labels
	for category in args.categories:
		for quantity in args.quantity:
			if args.input_files != None:
				if args.input_dir != None:
					log.warning("you cant use --input-file, and --input-dir together!!!")

				for channel in args.channels:
					print channel
					print quantity
					config= {}
					if category !=None:
						directory = args.output_dir + category +"/" + channel +"/"
					else:
						directory =  args.output_dir + channel +"/"
					
					print directory
					weights = []
		
					config["output_dir"] = directory
					if channel == "et":
						hltweights = [
							"(1)", 
							"(HLT_Ele32_WPTight_Gsf==1)", 
							"(HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1==1)", 
							"((HLT_Ele32_WPTight_Gsf==1)||(HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1==1))"
							]
						labels = ['all_events', 'Ele32_WPTight_Gsf', 'Ele24_LooseChargedIsoPFTau30', 'any_of_them']
						config["colors"] = ["kBlack", "kRed", "kGreen", "kBlue", "kRed", "kGreen", "kBlue"]
						if quantity  == "genBosonTau1VisibleLV.Pt()":
							config["x_expressions"] = ["(genBosonTau1VisibleLV.Pt()) * ((genBosonTau1DecayMode== -1)*(genBosonTau2DecayMode >= 0)) + (genBosonTau2VisibleLV.Pt()) * ((genBosonTau2DecayMode == -1)*(genBosonTau1DecayMode >= 0))"]

						elif quantity == "genBosonTau2VisibleLV.Pt()":
							config["x_expressions"] = ["(genBosonTau1VisibleLV.Pt()) * ((genBosonTau2DecayMode == -1)*(genBosonTau1DecayMode >= 0)) + (genBosonTau2VisibleLV.Pt()) * ((genBosonTau1DecayMode== -1)*(genBosonTau2DecayMode >= 0))"]
						else:
							config["x_expressions"] = quantity
					elif channel == "mt":
						hltweights = [
							"(1)", 
							"(HLT_IsoMu24==1)", 
							"(HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1==1)", 
							"((HLT_IsoMu24==1)||(HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1==1))"
							]
						labels = ['all_events', 'IsoMu24', 'IsoMu20_eta2p1_MediumChargedIsoPFTau27', 'any_of_them']
						config["colors"] = ["kBlack", "kRed", "kGreen", "kBlue", "kRed", "kGreen", "kBlue"]

						if quantity  == "genBosonTau1VisibleLV.Pt()":
							config["x_expressions"] = ["(genBosonTau1VisibleLV.Pt()) * ((genBosonTau1DecayMode== -2)*(genBosonTau2DecayMode >= 0)) + (genBosonTau2VisibleLV.Pt()) * ((genBosonTau2DecayMode == -2)*(genBosonTau1DecayMode >= 0))"]

						elif quantity == "genBosonTau2VisibleLV.Pt()":
							config["x_expressions"] = ["(genBosonTau1VisibleLV.Pt()) * ((genBosonTau2DecayMode == -2)*(genBosonTau1DecayMode >= 0)) + (genBosonTau2VisibleLV.Pt()) * ((genBosonTau1DecayMode== -2)*(genBosonTau2DecayMode >= 0))"]
						else:
							config["x_expressions"] = quantity

					elif channel == "tt":
						hltweights = [
							"(1)", 
							"(HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg==1)", 
							"(HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg==1)", 
							"(HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg==1)",
							"((HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg==1)||(HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg==1)||(HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg==1))"
							]
						labels = ['all_events', 'DoubleTightChargedIsoPFTau35_Trk1_TightID', 'DoubleMediumChargedIsoPFTau40_Trk1_TightID', 'DoubleTightChargedIsoPFTau40', 'any_of_them']
						config["colors"] = ["kBlack", "kRed", "kGreen", "kBlue", "kViolet", "kRed", "kGreen", "kBlue", "kViolet"]
						if quantity  == "genBosonTau1VisibleLV.Pt()":
							config["x_expressions"] = ["(genBosonTau1VisibleLV.Pt()) * ((genBosonTau1DecayMode>= 0)*(genBosonTau2DecayMode >= 0))"]

						elif quantity == "genBosonTau2VisibleLV.Pt()":
							config["x_expressions"] = ["(genBosonTau2VisibleLV.Pt()) * ((genBosonTau1DecayMode>= 0)*(genBosonTau2DecayMode >= 0))"]
						else:
							config["x_expressions"] = quantity

					for weight in hltweights:
						if quantity.startswith("HLT"):
							pass						
						else:
							if args.weights:
								for x in args.weights:
									weight = weight + " *"+ x
									weights.append(weight)
							else:
								weights.append(weight) 
					
					config["weights"] = weights
					config["markers"] = "P" 
					config["legend"] = [0.6, 0.1, 0.9, 0.45]
					
					config["x_label"] = quantity
					config["y_label"] = "events"
					config["files"] = args.input_files
					config["filename"] = channel + "_trigger_eff_" + quantity
					config["labels"] = labels
					config["nicks"] = labels
					config["stacks"] = labels
					config["folders"] = "gen/ntuple"
					config["analysis_modules"] = ["Ratio"]
					config["ratio_numerator_nicks"] = labels[1:]
					config["ratio_denominator_nicks"] = labels[0]
					if channel == "et":
						config["x_bins"] = "40,20,50"
					elif channel == "mt":
						config["x_bins"] = "40,15,45"
					elif channel == "tt":
						config["x_bins"] = "40,30,60"
					config["y_log"] = True	
					config["www"] = "ratioplot"
					plot_configs.append(config)

	higgsplot.HiggsPlotter(
		list_of_config_dicts=plot_configs, list_of_args_strings=[args.args],
		n_processes=args.n_processes, n_plots=args.n_plots, batch=args.batch
	)			






