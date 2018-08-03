#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import Artus.Utility.tools as tools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT file with inputs for getCalibrationCurve.py script.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action = "append",
	                    default=["mt", "et", "tt", "em"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["a1", "rho", "oneprong"], ["a1", "rho", "oneprong"], ["rho", "combined_a1_a1", "combined_a1_oneprong", "combined_oneprong_oneprong"], ["combined_oneprong_oneprong"]],
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/TauPolSoftware/CalibrationCurve/data",
	                    help="Output directory. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[len(parser.get_default("channel")):]

	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[len(parser.get_default("categories")):]
	args.categories = (args.categories * len(args.channel))[:len(args.channel)]
	
	args.output_dir = os.path.expandvars(args.output_dir)
	
	sample_settings = samples.Samples()
	
	weights = {
		"up" : "(lheZfromUUbar+lheZfromCCbar)",
        "down" : "(lheZfromDDbar+lheZfromSSbar+lheZfromBBbar)",
	}
	
	plot_configs = []
	for channel, categories in zip(args.channel, args.categories):
		for category in categories:
			channel_category = channel+"_"+category
			
			for quark_type in ["up", "down"]:
			
				config = sample_settings.get_config(
						samples=[getattr(samples.Samples, sample) for sample in ["ztt"]],
						no_ewkz_as_dy=True,
						channel=channel,
						category="catZttPol13TeV_"+channel_category,
						weight=weights[quark_type],
						cut_type="low_mvis_smhtt2016",
						lumi = args.lumi * 1000,
						exclude_cuts=[],
						estimationMethod="new",
				)
				
				for key in ["stacks", "legend_markers"]:
					if key in config:
						config.pop(key)
				
				config["directories"] = [args.input_dir]
				
				config["x_expressions"] = ["genBosonLV.mass()"]
				config["x_bins"] = ["150,50,200"]
				
				config["plot_modules"] = ["ExportRoot"]
				config["labels"] = [os.path.join(channel_category, quark_type)] * len(config["labels"])
				config["output_dir"] = os.path.join(args.output_dir, channel, category, quark_type)
				config["filename"] = "energy_distribution"
				
				plot_configs.append(config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	plot_results = higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	root_filenames = tools.flattenList(plot_results.output_filenames)
	merged_output = os.path.join(args.output_dir, "energy_distributions.root")
	tools.hadd(target_file=merged_output, source_files=root_filenames, hadd_args="-f")
	log.info("Merged outputs in "+merged_output)

