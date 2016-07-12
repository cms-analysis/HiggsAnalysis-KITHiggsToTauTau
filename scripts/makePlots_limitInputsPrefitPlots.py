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

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make prefit plots from limit inputs.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input", required=True,
	                    help="Input ROOT file containing limit input histograms.")
	parser.add_argument("-d", "--data-processes", nargs="+",
	                    default=["data_obs"],
	                    help="Data processes. [Default: %(default)s]")
	parser.add_argument("-b", "--background-processes", nargs="+",
	                    default=["ZTT", "ZL", "ZJ", "TT", "W", "VV", "QCD"],
	                    help="Background processes. [Default: %(default)s]")
	parser.add_argument("-s", "--signal-processes", nargs="+",
	                    default=[], #["ggH", "qqH", "WH", "ZH", "VH"],
	                    help="Signal processes. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	                    
	
	args = vars(parser.parse_args())
	logger.initLogger(args)
	
	root_file = ROOT.TFile(args["input"], "READ")
	keys = root_file.GetListOfKeys()
	
	directories = [keys.At(index).GetName() for index in range(keys.GetSize()) if keys.At(index).GetClassName() == "TDirectoryFile"]
	histograms = {}
	
	for directory in directories:
		root_dir = root_file.Get(directory)
		keys = root_dir.GetListOfKeys()
		histograms[directory] = [keys.At(index).GetName() for index in range(keys.GetSize()) if keys.At(index).GetClassName().startswith("TH")]
		
		# remove shape histograms
		histograms[directory] = [h for h in histograms[directory] if not ("_" in h and (h.endswith("Up") or h.endswith("Down")))]
	
	root_file.Close()
	
	datas = {directory : [h for h in histos if h in args["data_processes"]] for directory, histos in histograms.items()}
	backgrounds = {directory : [h for h in histos if h in args["background_processes"]] for directory, histos in histograms.items()}
	masses_signals = {m : {directory : [h for h in histos if h.replace(str(m), "") in args["signal_processes"]] for directory, histos in histograms.items()} for m in args["higgs_masses"]}
	
	colors = {
		"data_obs" : "#000000",
		"ZTT" : "#FFCC66",
		"ZL" : "#4496C8",
		"ZJ" : "#64B6E8",
		"TT" : "#9999CC",
		"VV" : "#DE5A6A",
		"W" : "#FE7A8A",
		"QCD" : "#FFCCFF",
	}
	
	plot_configs = []
	for mass, signals in masses_signals.iteritems():
		for directory, data in datas.items():
			background = backgrounds[directory]
			signal = signals[directory]
			
			plot_configs.append(jsonTools.JsonDict())
			
			plot_configs[-1]["files"] = [args["input"]]
			plot_configs[-1]["folders"] = [directory]
			plot_configs[-1]["x_expressions"] = background + signal + data
			plot_configs[-1]["nicks"] = background + (["sig"]*len(signal)) + (["data"]*len(data))
			plot_configs[-1]["stacks"] = (["bkg"]*len(background)) + (["sig"]*(1 if len(signal) > 0 else 0)) + ["data"]
			plot_configs[-1]["markers"] = (["hist"]*len(background)) + (["line"]*(1 if len(signal) > 0 else 0)) + ["E"]
			plot_configs[-1]["ratio"] = args["ratio"]
			plot_configs[-1]["colors"] = [colors.get(x, "#000000") for index, x in enumerate(plot_configs[-1]["x_expressions"])]
			plot_configs[-1]["labels"] = background + (["Signal (%d)" % mass]*(1 if len(signal) > 0 else 0)) + ["Data"]
			plot_configs[-1]["legend"] = [0.75, 0.6]
			plot_configs[-1]["x_label"] = ""
			plot_configs[-1]["y_label"] = "Events"
			plot_configs[-1]["output_dir"] = os.path.join("plots", "prefit", os.path.splitext(os.path.basename(args["input"]))[0])
			plot_configs[-1]["filename"] = directory + "_mH" + str(mass)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args["args"]], n_processes=args["n_processes"], n_plots=args["n_plots"])

