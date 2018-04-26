#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import sys

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make (additional) plots for ZTT polarisation analysis.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["zttpospol", "zttnegpol"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--era", default="2016",
	                    help="Era of samples to be used. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", action="append",
	                    default=["tt", "mt", "et"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+", default=[["a1_1", "a1_2", "rho_1", "rho_2", "oneprong_1", "oneprong_2"], ["a1_2", "rho_2", "oneprong_2"], ["a1_2", "rho_2", "oneprong_2"]],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/ztt_polarisation/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="ztt_polarisation",
	                    help="Publish plots. [Default: %(default)s]")

	args = parser.parse_args()
	logger.initLogger(args)
	
	if (args.era == "2015") or (args.era == "2015new"):
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
	elif args.era == "2016":
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
		if args.lumi == parser.get_default("lumi"):
			args.lumi = samples.default_lumi/1000.0
	else:
		log.critical("Invalid era string selected: " + args.era)
		sys.exit(1)

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	bkg_samples = [sample for sample in args.samples if sample not in ["data", "htt", "ggh", "qqh", "vh"]]
	
	labels_settings = labels.LabelsDict(latex_version="root")

	if len(args.channels) > len(parser.get_default("channels")):
		args.channels = args.channels[len(parser.get_default("channels")):]
	if len(args.categories) > len(parser.get_default("categories")):
		args.categories = args.categories[len(parser.get_default("categories")):]

	plot_configs = []
	for channel, categories in zip(args.channels, args.categories):
		for category in categories:
			if category == "None":
				category = None
			
			for polarisation_bias_correction in [False, True]:
				config = sample_settings.get_config(
						samples=list_of_samples,
						no_ewkz_as_dy=True,
						channel=channel,
						category="catZttPol13TeV_{channel}_{category}".format(channel=channel, category=category) if category else None,
						cut_type="smhtt2016", # baseline_low_mvis2016
						weight="isZTT",
						lumi = args.lumi * 1000,
						exclude_cuts=[],
						estimationMethod="new",
						polarisation_bias_correction=polarisation_bias_correction,
						polarisation_gen_ztt_plots=True,
						nick_suffix="_noplot",
						no_plot=True
				)
				
				if "stacks" in config:
					config.pop("stacks")
				
				config["x_expressions"] = "tauSpinnerPolarisation"
				config["x_bins"] = "2,-2,2"
				config["x_label"] = ""
				config["x_ticks"] = [-1.0, 1.0]
				config["x_tick_labels"] = ["zttnegpol_large", "zttpospol_large"]
				
				if not "SumOfHistograms" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("SumOfHistograms")
				config.setdefault("sum_nicks", []).extend(["zttpospol_noplot zttnegpol_noplot", "gen_zttpospol_noplot gen_zttnegpol_noplot"])
				config.setdefault("sum_result_nicks", []).extend(["ztt", "ztt_gen"])
				
				if not "NormalizeToUnity" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("NormalizeToUnity")
							
				config["labels"] = ["Reconstruction", "Generator"]
				config["colors"] = ["1", "2"]
				config["markers"] = ["E", "LINE]["]
				config["legend_markers"] = ["ELP", "L"]
				config["legend"] = [0.25, 0.8, 0.85, 0.9]
				config["legend_cols"] = 2
				
				config["y_label"] = "Relative Fraction of Z#rightarrow#tau#tau"
				config["y_lims"] = [0.0, 1.0]

				config["title"] = "channel_"+channel

				config["directories"] = [args.input_dir]
				config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, category))
				config["filename"] = "tauSpinnerPolarisation_"+("after" if polarisation_bias_correction else "before")+"_bias_correction"
				if args.www:
					config["www"] = os.path.expandvars(os.path.join(args.www, channel, category))

				if log.isEnabledFor(logging.DEBUG) and (not "PrintInfos" in config.get("analysis_modules", [])):
					config.setdefault("analysis_modules", []).append("PrintInfos")
				
				plot_configs.append(config)
	
	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

