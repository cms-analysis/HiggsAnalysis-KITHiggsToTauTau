#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gErrorIgnoreLevel = ROOT.kError

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import Artus.HarryPlotter.utility.roottools as roottools
from Artus.Utility.tfilecontextmanager import TFileContextManager


def get_histogram_names(input_filename):
	# find get paths to the histograms in the file.
	with TFileContextManager(input_filename, "READ") as root_file:
		elements = roottools.RootTools.walk_root_directory(root_file)
		histograms = []
		for index, (key, path) in enumerate(elements):
			histograms.append(path)
	
	return histograms

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make sync plots of two root-files containing shapes used as input for CombineHarvester.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("--input-1", help="Input files 1.", required=True)
	parser.add_argument("--input-2", help="Input files 2.", required=True)
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/sync_plots/",
	                    help="Output directory. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	#get common histograms 
	
	histograms1 = get_histogram_names(args.input_1)
	histograms2 = get_histogram_names(args.input_2)
	common_histograms = list(set(histograms1).intersection(set(histograms2)))

	plot_configs = []
	for index, histogram in enumerate(common_histograms):
		plot_config = {}
	
		plot_config["files"] = [args.input_1, args.input_2]
		plot_config["folders"] = ["", ""]
		plot_config["nicks"] = ["events1", "events2"]
		plot_config["x_expressions"] = [histogram]
		plot_config["weights"] = ["("+histogram+"> -990)"]

		plot_config.setdefault("analysis_modules", []).append("Ratio")
		plot_config["ratio_numerator_nicks"] = plot_config["nicks"][0]
		plot_config["ratio_denominator_nicks"] = plot_config["nicks"][1]

		plot_config["labels"] = ["events in 1", "events in 2", ""]
		plot_config["legend_markers"] = ["LP", "F", ""]
		plot_config["legend"] = [0.7, 0.55, 0.9, 0.85]
		plot_config["y_label"] = "Events"
		plot_config["fill_styles"] = [0]
		plot_config["colors"] = ["kBlack", "kRed", "kBlack"]
		plot_config["markers"] = ["P", "HIST", "P"]
		plot_config["y_subplot_lims"] = [0.95, 1.05]
	
		plot_config["output_dir"] = os.path.expandvars(args.output_dir)
		plot_configs.append(plot_config)
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	if os.path.exists(event_matching_output) and not args.keep_eventmatching_output:
		os.remove(event_matching_output)
