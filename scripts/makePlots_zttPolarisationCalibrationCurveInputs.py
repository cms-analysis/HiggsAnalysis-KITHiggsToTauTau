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
	parser.add_argument("-c", "--channels", action="append",
	                    default=["tt", "mt", "et"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+",
	                    default=["a1", "a1_1", "a1_2",
	                             "rho", "rho_1", "rho_2",
	                             "oneprong", "oneprong_1", "oneprong_2",
	                             "combined_a1_a1", "combined_a1_rho", "combined_a1_oneprong",
	                             "combined_rho_rho", "combined_rho_oneprong",
	                             "oneprong_oneprong"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/ztt_polarisation_calibration_curve/",
	                    help="Output directory. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.expandvars(args.output_dir)
	
	sample_settings = samples.Samples()
	
	weights = {
		"up" : "(lheZfromUUbar+lheZfromCCbar)",
        "down" : "(lheZfromDDbar+lheZfromSSbar+lheZfromBBbar)",
	}
	
	plot_configs = []
	for channel in args.channels:
		for category in args.categories:
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

