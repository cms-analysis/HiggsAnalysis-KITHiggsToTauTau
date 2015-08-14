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
	                    choices=["all", "inclusive"],
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
	root_filename_template = "${ANALYSIS}_${CHANNEL}.input_${ERA}.root"
	datacard_filename_template = "${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt"
	datacards = zttxsecdatacards.ZttXsecDatacards()
	
	# prepare channel settings based on args and datacards
	if (len(args.channel) == 1) and (args.channel[0] == "all"):
		args.channel = datacards.cb.channel_set()
	else:
		args.channel = list(set(args.channel).intersection(set(datacards.cb.channel_set())))
	
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
			
			# prepare plotting configs for retrieving the input histograms
			config = sample_settings.get_config(
					samples=[getattr(samples.Samples, sample) for sample in list_of_samples],
					channel=channel,
					category=None # TODO: category
			)
			
			config["x_expressions"] = args.quantity
			
			config["directories"] = [args.input_dir]
			
			if args.weight != parser.get_default("weight"):
				if "weights" in config:
					newWeights = []
					for weight in config["weights"]:
						newWeights.append(weight + '*' + args.weight)
					config["weights"] = newWeights
				else:
					config["weights"] = args.weight
			
			config["labels"] = [datacards.configs.sample2process(sample) for sample in list_of_samples]
			
			config["output_dir"] = args.output_dir
			config["filename"] = os.path.splitext(root_filename_template.format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					ERA="13TeV"
			).replace("$", ""))[0]
			config["plot_modules"] = ["ExportRoot"]
			#config["file_mode"] = ["UPDATE"] # TODO delete files at first run
			
			if "legend_markers" in config:
				config.pop("legend_markers")
			
			plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
	
	# create input histograms with HarryPlotter
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	# update CombineHarvester with the yields and shapes
	datacards.extract_shapes(os.path.join(args.output_dir, root_filename_template.replace("$", "")), "$PROCESS", "$PROCESS_$SYSTEMATIC")
	
	# write datacards
	datacards.write_datacards(
			datacard_filename_template.replace("{", "").replace("}", ""),
			os.path.join("common", root_filename_template.replace("{", "").replace("}", "")),
			args.output_dir
	)

