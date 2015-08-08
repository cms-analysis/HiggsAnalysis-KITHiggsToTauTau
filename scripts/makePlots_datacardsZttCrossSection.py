#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT cross section measurement.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zl", "zj", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "data"], 
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")
	parser.add_argument("--channels", nargs="*",
	                    default=["mt", "et"],
	                    choices=["tt", "mt", "et", "em", "mm", "ee"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantity",
	                    help="Quantity. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")	
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/datacards/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Sample, sample)]
	list_of_samples = [getattr(samples.Sample, sample) for sample in args.samples]
	sample_settings = samples.Sample()
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "htt"]

	args.categories = [None if category == "None" else category for category in args.categories]

	plot_configs = []
	for channel in args.channels:
		for category in args.categories:
			
			config = sample_settings.get_config(
					samples=list_of_samples,
					channel=channel,
					category=category,
					ztt_from_mc=args.ztt_from_mc
			)
			
			config["x_expressions"] = args.quantity
			config["x_bins"] = [channel+"_"+args.quantity]
			config["x_label"] = channel+"_"+args.quantity
			
			config["directories"] = [args.input_dir]
			
			if args.weight != parser.get_default("weight"):
				if "weights" in config:
					newWeights = []
					for weight in config["weights"]:
						newWeights.append(weight + '*' + args.weight)
					config["weights"] = newWeights
				else:
					config["weights"] = args.weight
			
			config["output_dir"] = os.path.expandvars(os.path.join(
					args.output_dir,
					channel if len(args.channels) > 1 else "",
					category if len(args.categories) > 1 else ""
			))
			if not args.www is None:
				config["www"] = os.path.expandvars(os.path.join(
						args.www,
						channel if len(args.channels) > 1 else "",
						category if len(args.categories) > 1 else ""
				))
			
			config["plot_modules"] = ["ExportRoot"]
			
			if "legend_markers" in config:
				config.pop("legend_markers")
			
			plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

