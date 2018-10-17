#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import ROOT

import Artus.HarryPlotter.utility.roottools as roottools
import Artus.Utility.tfilecontextmanager as tfilecontextmanager
import Artus.Utility.tools as tools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot



if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="Plot shape uncertainties.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("input_files", nargs="+",
	                    help="Limit input ROOT files.")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir", default=None,
	                    help="Output directory. [Default: relative to datacards]")
	parser.add_argument("--www", nargs="?", default=None, const="shape_uncertainties",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	inputs_base = tools.longest_common_substring_from_list([os.path.dirname(input_file) for input_file in args.input_files])
	if not inputs_base.endswith("/"):
		inputs_base += "/"
	
	plot_configs = []
	for input_file in args.input_files:
		root_file_content = []
		with tfilecontextmanager.TFileContextManager(input_file, "READ") as root_file:
			root_file_content = roottools.RootTools.walk_root_directory(root_file)
		
		parsed_root_file_content = {}
		for key, path in root_file_content:
			folder = os.path.dirname(path)
			histogram = os.path.basename(path)
			if (not histogram.endswith("Up")) and (not histogram.endswith("Down")):
				parsed_root_file_content.setdefault(folder, {})[histogram] = {}
		
		for key, path in root_file_content:
			folder = os.path.dirname(path)
			histogram = os.path.basename(path)
			if (histogram.endswith("Up")) or (histogram.endswith("Down")):
				for process in sorted(parsed_root_file_content.get(folder, {}).keys())[::-1]:
					if histogram.startswith(process+"_"):
						uncertainty = histogram.replace(process+"_", "")
		
						index = None
						shift_up = uncertainty.endswith("Up")
						if shift_up:
							uncertainty = uncertainty[:-2]
							index = 0
						shift_down = uncertainty.endswith("Down")
						if shift_down:
							uncertainty = uncertainty[:-4]
							index = 1
						if shift_up or shift_down:
							parsed_root_file_content.setdefault(folder, {}).setdefault(process, {}).setdefault(uncertainty, [None, None])[index] = histogram
						
						break
		
		for folder, folder_content in parsed_root_file_content.iteritems():
			for process, process_content in folder_content.iteritems():
				for uncertainty, histograms in process_content.iteritems():
				
					config = {}
					config["files"] = [input_file]
					config["folders"] = [folder]
					config["x_expressions"] = ([process]+histograms)
					config["nicks"] = ([process]+histograms)
				
					config["colors"] = ["kBlack", "kRed", "kBlue"]
					config["markers"] = ["E", "LINE", "LINE"]
					config["legend_markers"] = ["ELP", "L", "L"]
					config["labels"] = ["nominal", "#plus1#sigma shift", "#minus1#sigma shift"]
				
					config["legend"] = [0.65, 0.7, 0.9, 0.88]
					config["title"] = uncertainty+" ("+process+")"
					config["x_label"] = "Disciminator"
				
					if args.ratio:
						if not "Ratio" in config.get("analysis_modules", []):
							config.setdefault("analysis_modules", []).append("Ratio")
						config.setdefault("ratio_numerator_nicks", []).extend(histograms)
						config.setdefault("ratio_denominator_nicks", []).extend([process] * 2)
						config.setdefault("ratio_result_nicks", []).extend(["ratio_up", "ratio_down"])
					
						config["colors"].extend(config["colors"][1:])
						config["markers"].extend(["LINE", "LINE"])
						config["legend_markers"].extend(config["legend_markers"][1:])
						config["labels"].extend([""] * 2)
					
						config["legend"] = [0.65, 0.65, 0.95, 0.83]
				
					output_dir = args.output_dir
					if output_dir is None:
						output_dir = os.path.join(os.path.splitext(input_file)[0], folder, uncertainty)
					config["output_dir"] = output_dir
					if args.www:
						config["www"] = os.path.join(args.www, os.path.splitext(input_file)[0].replace(inputs_base, ""), folder, uncertainty)
					config["filename"] = process
				
					plot_configs.append(config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(configs)
	
	higgs_plotter = higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

