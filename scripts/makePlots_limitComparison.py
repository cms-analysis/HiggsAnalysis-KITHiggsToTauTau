#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import itertools
import os
import tempfile

import Artus.Utility.jsonTools as jsonTools
import Artus.HarryPlotter.utility.roottools as roottools
import Artus.HarryPlotter.utility.tfilecontextmanager as tfilecontextmanager

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Plot comparisons of combine outputs.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("-j", "--json-config", default="$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/combine/exp_limit_over_mass_without_band.json",
	                    help="JSON config specifying the type of plot. [Default: %(default)s]")
	parser.add_argument("-i", "--input-dirs", nargs="+", required=True,
	                    help="Input directories containing files <mass>/higgsCombine-<exp|obs>.Asymptotic.mH<mass>.root.")
	parser.add_argument("--nicks", nargs="+",
	                    help="Nicks from single plots to put into the comparison plot. [Ddefault: all]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir", default="$CMSSW_BASE/plots/",
	                    help="Output directory. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	json_config = jsonTools.JsonDict(os.path.expandvars(args.json_config))
	
	# produce temp. ROOT files
	tmp_plot_configs = []
	for input_dir in args.input_dirs:
		tmp_plot_config = copy.deepcopy(json_config)
		
		tmp_plot_config["directories"] = [input_dir]
		for key in ["x_expressions", "z_expressions", "z_expressions"]:
			if not tmp_plot_config.get(key, None) is None:
				tmp_plot_config[key] = [expression.replace("lumi", "(lumi/1000.0)") for expression in tmp_plot_config[key]]
		
		tmp_plot_config["plot_modules"] = ["ExportRoot"]
		tmp_plot_config["nicks_instead_labels"] = True
		output_filename = tempfile.mkstemp(prefix="limit", suffix=".root")[-1]
		tmp_plot_config["output_dir"] = os.path.dirname(output_filename)
		tmp_plot_config["filename"] = os.path.splitext(os.path.basename(output_filename))[0]
		
		tmp_plot_configs.append(tmp_plot_config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	higgsplot.HiggsPlotter(list_of_config_dicts=tmp_plot_configs, list_of_args_strings=[""], n_processes=args.n_processes, n_plots=args.n_plots)
	
	# produce combined plots
	plot_config = {}
	tmp_input_files = [os.path.join(tmp_plot_config["output_dir"], tmp_plot_config["filename"]+".root") for tmp_plot_config  in tmp_plot_configs]
	
	root_object_paths = []
	with tfilecontextmanager.TFileContextManager(tmp_input_files[0], "READ") as root_file:
		root_object_paths = zip(*roottools.RootTools.walk_root_directory(root_file))[-1]
	plot_indices = range(len(root_object_paths))
	if not args.nicks is None:
		root_object_paths, plot_indices = zip(*[(nick, root_object_paths.index(nick)) for nick in args.nicks if nick in root_object_paths])
	
	plot_config["files"] = tmp_input_files * len(root_object_paths)
	plot_config["x_expressions"] = list(itertools.chain(*[[root_object_path] * len(tmp_input_files) for root_object_path in root_object_paths]))
	plot_config["nicks"] = ["_".join(str(part) for part in nick_parts) for nick_parts in itertools.product(root_object_paths, range(len(tmp_input_files)))]
	
	for key in ["markers", "legend_markers", "labels", "line_widths", "fill_styles"]:
		if key in json_config:
			if len(json_config[key]) > 1:
				plot_config[key] = list(itertools.chain(*[[item] * len(tmp_input_files) for item in [json_config[key][index] for index in plot_indices]]))
			else:
				plot_config[key] = json_config[key]
	
	for key in ["x_label", "y_label", "legend"]:
		if key in json_config:
			plot_config[key] = json_config[key]
	
	for analysis_module in args.analysis_modules:
		if not analysis_module in plot_config.get("analysis_modules", []):
			plot_config.setdefault("analysis_modules", []).append(analysis_module)
	
	plot_config["output_dir"] = os.path.expandvars(args.output_dir)
	plot_config["filename"] = json_config["filename"]
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_config)
	higgsplot.HiggsPlotter(list_of_config_dicts=[plot_config], list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	# remove temp. ROOT files
	for tmp_input_file in tmp_input_files:
		os.remove(tmp_input_file)
		os.remove(tmp_input_file.replace(".root", ".json"))
	log.info("Removed temporary files.")

