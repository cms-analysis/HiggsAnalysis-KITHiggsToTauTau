#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import glob
import os

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


def get_quantities(input_filename, folder):
	input_file = ROOT.TFile(glob.glob(input_filename.split()[0])[0])
	tree = input_file.Get(folder)
	
	quantities = []
	for leaf in sorted(tree.GetListOfLeaves(), key=lambda leaf: leaf.GetName()):
		quantity = leaf.GetName()
		if leaf.GetBranch().GetMother().GetName() != leaf.GetName():
			quantity = leaf.GetBranch().GetMother().GetName()+"."+quantity
		quantities.append(quantity)
	
	input_file.Close()
	return quantities


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make sync plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("--input-1", help="Input files 1.", required=True)
	parser.add_argument("--input-2", help="Input files 2.", required=True)
	parser.add_argument("--folder-1", help="Folder for input 1.", required=True)
	parser.add_argument("--folder-2", help="Folder for input 2.", required=True)
	parser.add_argument("-e", "--event-matching", action="store_true", default=False,
	                    help="Show four histograms per plot using the output of eventmatching.py. [Default: %(default)s]")
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
	
	quantities1 = get_quantities(args.input_1, args.folder_1)
	quantities2 = get_quantities(args.input_2, args.folder_2)
	common_quantities = list(set(quantities1).intersection(set(quantities2)))
	
	plot_configs = []
	event_matching_output = "eventmatching.root"
	for index, quantity in enumerate(common_quantities):
		plot_config = {}
		
		if args.event_matching:
			if index == 0:
				command = "eventmatching.py {input1} {input2} -t {folder1} {folder2} -f {output}".format(
					input1=args.input_1,
					input2=args.input_2,
					folder1=args.folder_1,
					folder2=args.folder_2,
					output=event_matching_output
				)
				log.info(command)
				logger.subprocessCall(command, shell=True)
			
			plot_config["files"] = [event_matching_output]
			plot_config["folders"] = ["common1", "common2", "only1", "only2"]
			plot_config["x_expressions"] = [quantity]
		
		else:
			plot_config["files"] = [args.input_1, args.input_2]
			plot_config["folders"] = [args.folder_1, args.folder_2]
			plot_config["x_expressions"] = [quantity]
		
		plot_config["output_dir"] = os.path.expandvars(args.output_dir)
		plot_configs.append(plot_config)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	if os.path.exists(event_matching_output):
		os.remove(event_matching_output)

