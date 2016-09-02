#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import itertools
import os
import sys

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Compare different inputs for control plots, e.g. different Artus outputs, different channels or different quantities.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dirs", required=True, nargs="+",
	                    help="Input directories.")
	parser.add_argument("-s", "--samples", required=True, nargs="+",
	                    help="Samples. If multiple samples should be added before the comparison, put them in a single argument separated by whitespaces.")
	parser.add_argument("-c", "--channels", required=True, nargs="+",
	                    choices=["tt", "mt", "et", "em", "mm", "ee"],
	                    help="Channels.")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", required=True, nargs="+",
	                    help="Quantities.")
	parser.add_argument("-w", "--weights", nargs="+", default=["1.0"],
	                    help="Additional weight (cut) expressions. [Default: %(default)s]")
	parser.add_argument("--run1", default=False, action="store_true",
	                    help="Use Run1 samples. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="",
	                    help="Publish plots. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)

	if not args.run1:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples
	sample_settings = samples.Samples()
	
	compare_two_qantities = ((len(args.input_dirs)*len(args.samples)*len(args.channels)*len(args.categories)*len(args.weights) == 1) and (len(args.quantities) == 2))
	
	# expand comparisons
	input_dirs, sample_strings, channels, categories, quantities, weights = zip(*itertools.product(
			args.input_dirs,
			args.samples,
			args.channels,
			args.categories,
			args.quantities,
			args.weights
	))
	
	plot_configs = []
	plot_config = {}
	
	log.debug("Compare %d different control plot inputs:" % len(input_dirs))
	for index, (input_dir, sample_string, channel, category, quantity, weight) in enumerate(zip(input_dirs, sample_strings, channels, categories, quantities, weights)):
		log.debug("Input %d: -i %s -s %s -c %s --category %s -x %s -w %s" % (index+1, input_dir, sample_string, channel, category, quantity, weight))
	
		tmp_sample_strings = sample_string.split()
		list_of_samples = [getattr(samples.Samples, tmp_sample_string) for tmp_sample_string in tmp_sample_strings]
		multiple_samples = (len(tmp_sample_strings) > 1)
		nick_suffix = "_"+str(index)+("_noplot" if multiple_samples else "")
		
		config = sample_settings.get_config(
				samples=list_of_samples,
				channel=channel,
				category=category,
				higgs_masses=args.higgs_masses,
				normalise_signal_to_one_pb=False,
				weight=weight,
				lumi = args.lumi * 1000,
				exclude_cuts=args.exclude_cuts,
				nick_suffix=nick_suffix
		)
		config["directories"] = [input_dir for nick in config["nicks"]]
		config["x_expressions"] = [quantity for nick in config["nicks"]]
		
		for key in ["colors", "labels", "markers", "legend_markers", "stacks"]:
			if key in config:
				config.pop(key)
		
		if multiple_samples:
			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("add_nicks", []).append(" ".join([tmp_sample_string+nick_suffix for tmp_sample_string in tmp_sample_strings]))
			config.setdefault("add_result_nicks", []).append("_".join(tmp_sample_strings+[str(index)]))
		
		if (index == 0) and compare_two_qantities:
			plot_2d_config = copy.deepcopy(config)
			plot_2d_config["y_expressions"] = quantities[index+1]
			plot_configs.append(plot_2d_config)
	
		plot_config = samples.Samples.merge_configs(plot_config, config)
	plot_configs.append(plot_config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

