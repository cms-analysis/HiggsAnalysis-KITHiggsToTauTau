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
import Artus.HarryPlotter.utility.roottools as roottools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


def multi_rename(input_string, renamings):
	output_string = input_string
	for key, value in renamings.iteritems():
		output_string = output_string.replace(key, value)
	return output_string


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make prefit plots from limit inputs.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--inputs", required=True, nargs=2,
	                    help="Input ROOT files containing limit input histograms.")
	parser.add_argument("-l", "--labels", nargs=2, default=["1", "2"],
	                    help="Labels. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="limi_inputs",
	                    help="Publish plots. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	                    
	args = parser.parse_args()
	logger.initLogger(args)
	
	root_files = [ROOT.TFile(filename, "READ") for filename in args.inputs]
	histogram_paths = [[path for key, path in roottools.RootTools.walk_root_directory(root_file) if key.GetClassName().startswith("TH")] for root_file in root_files]
	root_files = [root_file.Close() for root_file in root_files]
	
	renamings = {
	}
	
	renamed_histogram_paths = [[multi_rename(path, renamings) for path in paths] for paths in histogram_paths]
	sorted_renamed_histogram_paths = sorted(renamed_histogram_paths, key=lambda sublist: len(sublist))
	common_histogram_paths = [[histogram_paths[input_index][renamed_histogram_paths[input_index].index(path)] for path in sorted_renamed_histogram_paths[0] if path in sorted_renamed_histogram_paths[1]] for input_index in range(len(histogram_paths))]
	
	plot_configs = []
	for histogram_paths_1, histogram_path_2 in zip(*common_histogram_paths):
		plot_configs.append(
				{
					"files" : args.inputs,
					"folders" : [os.path.dirname(histogram_paths_1), os.path.dirname(histogram_path_2)],
					"x_expressions" : [os.path.basename(histogram_paths_1), os.path.basename(histogram_path_2)],
					"title" : os.path.join(os.path.basename(args.inputs[0]), os.path.dirname(histogram_paths_1)),
					"labels" : args.labels+[""],
					"legend" : [0.6, 0.65, 0.9, 0.85],
					"colors" : ["kBlack", "kRed", "kBlack"],
					"markers" : ["E", "LINE", "E"],
					"legend_markers" : ["ELP", "L", "ELP"],
					"output_dir" : os.path.join("plots", "comparison", os.path.dirname(histogram_paths_1)),
					"filename" : os.path.basename(histogram_paths_1),
					"nicks" : ["1", "2"],
					"analysis_modules" : ["Ratio"],
					"ratio_numerator_nicks" : ["1"],
					"ratio_denominator_nicks" : ["2"],
					"ratio_result_nicks" : ["ratio"],
				}
		)
		if args.www:
			plot_configs[-1]["www"] = os.path.join(args.www, os.path.basename(args.inputs[0]), os.path.dirname(histogram_paths_1))
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

