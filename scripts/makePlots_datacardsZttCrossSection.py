#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import combineharvester as ch

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.datacards.zttxsecdatacards as zttxsecdatacards


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create ROOT inputs and datacards for ZTT cross section measurement.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-c", "--channel", action="append",
	                    default=["all"],
	                    choices=["tt", "mt", "et", "em", "mm", "ee"],
	                    help="Channel. This agument can be set multiple times. [Default: %(default)s]")
	parser.add_argument("--categories", action="append", nargs="+",
	                    default=[["all"]] * len(parser.get_default("channel")),
	                    choices=["all", "inclusive", "0jet", "1jet", "2jet"],
	                    help="Categories per channel. This agument needs to be set as often as --channels. [Default: %(default)s]")
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
	
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	args.output_dir = os.path.expandvars(args.output_dir)
	
	# initialisations for plotting
	sample_settings = samples.Samples()
	plot_configs = []
	
	# initialise datacards
	input_root_filename_template = "${ANALYSIS}_${CHANNEL}_${BIN}.input_${ERA}.root"
	output_root_filename_template = "${ANALYSIS}_${CHANNEL}.input_${ERA}.root"
	histogram_name_template = "${BIN}/${PROCESS}"
	syst_histogram_name_template = "${BIN}/${PROCESS}_${SYSTEMATIC}"
	datacard_filename_template = "${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt"
	datacards = zttxsecdatacards.ZttXsecDatacards()
	
	# prepare channel settings based on args and datacards
	if args.channel != parser.get_default("channel"):
		args.channel = args.channel[1:]
	if (len(args.channel) == 1) and (args.channel[0] == "all"):
		args.channel = datacards.cb.channel_set()
	else:
		args.channel = list(set(args.channel).intersection(set(datacards.cb.channel_set())))
	
	if args.categories != parser.get_default("categories"):
		args.categories = args.categories[1:]
	args.categories = (args.categories * len(args.channel))[:len(args.channel)]
	for index, (channel, categories) in enumerate(zip(args.channel, args.categories)):
		
		# prepare category settings based on args and datacards
		if (len(categories) == 1) and (categories[0] == "all"):
			categories = datacards.cb.bin_set()
		else:
			categories = list(set(categories).intersection(set(datacards.cb.bin_set())))
		args.categories[index] = categories
		
		for category in categories:
			list_of_samples = ["data"] + [datacards.configs.process2sample(process) for process in datacards.cb.cp().channel([channel]).process_set()]
			log.debug("Create inputs for samples = (\"{samples}\"), (channel, category) = ({channel}, {category}).".format(
					samples="\", \"".join(list_of_samples),
					channel=channel,
					category=category
			))
			
			# TODO: restrict datacards.cb to configured channels and categories
			
			# prepare plotting configs for retrieving the input histograms
			config = sample_settings.get_config(
					samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
					channel=channel,
					category="catZtt13TeV_"+channel+"_"+category,
					weight=args.weight
			)
			
			config["x_expressions"] = args.quantity
			
			config["directories"] = [args.input_dir]
			
			config["labels"] = [histogram_name_template.replace("$", "").format(
					PROCESS=datacards.configs.sample2process(sample),
					BIN=category
			) for sample in list_of_samples]
			
			config["output_dir"] = args.output_dir
			config["filename"] = os.path.splitext(input_root_filename_template.replace("$", "").format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					BIN=category,
					ERA="13TeV"
			))[0]
			config["plot_modules"] = ["ExportRoot"]
			config["file_mode"] = "UPDATE"
			
			if "legend_markers" in config:
				config.pop("legend_markers")
			
			plot_configs.append(config)

	#if log.isEnabledFor(logging.DEBUG):
	#	import pprint
	#	pprint.pprint(plot_configs)
	
	# delete existing output files
	output_files = list(set([os.path.join(config["output_dir"], config["filename"]+".root") for config in plot_configs[:args.n_plots]]))
	for output_file in output_files:
		if os.path.exists(output_file):
			os.remove(output_file)
			log.debug("Removed file \""+output_file+"\" before it is recreated again.")
	
	# create input histograms with HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(
			os.path.join(args.output_dir, input_root_filename_template.replace("$", "")),
			histogram_name_template.replace("{", "").replace("}", ""),
			syst_histogram_name_template.replace("{", "").replace("}", "")
	)
	
	# write datacards
	datacards.write_datacards(
			datacard_filename_template.replace("{", "").replace("}", ""),
			os.path.join("common", output_root_filename_template.replace("{", "").replace("}", "")),
			args.output_dir
	)

