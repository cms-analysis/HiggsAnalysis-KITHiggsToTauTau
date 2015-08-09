#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import combineharvester as ch

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
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Sample, sample)]
	list_of_samples = [getattr(samples.Sample, sample) for sample in args.samples]
	sample_settings = samples.Sample()
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "ztt"]

	args.categories = [None if category == "None" else category for category in args.categories]
	
	args.output_dir = os.path.expandvars(args.output_dir)
	
	plot_configs = []
	root_filename_template = "${ANALYSIS}_${CHANNEL}.input_${ERA}.root"
	datacard_filename_template = "${ANALYSIS}_${CHANNEL}_${BINID}_${ERA}.txt"
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
			
			config["labels"] = [sample.replace("data", "data_obs") for sample in args.samples]
			
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
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
	
	args.categories = ["None" if category is None else category for category in args.categories]
	
	# http://cms-analysis.github.io/HiggsAnalysis-HiggsToTauTau/python-interface.html
	cb = ch.CombineHarvester()
	
	cb.AddObservations(mass=['*'], analysis=['ztt'], era=['13TeV'], channel=args.channels, bin=list(enumerate(args.categories)))
	cb.AddProcesses(mass=['*'], analysis=['ztt'], era=['13TeV'], channel=args.channels, bin=list(enumerate(args.categories)), procs=bkg_samples, signal=False)
	cb.AddProcesses(mass=['*'], analysis=['ztt'], era=['13TeV'], channel=args.channels, bin=list(enumerate(args.categories)), procs=["ztt"], signal=True)
	
	for channel in args.channels:
		root_filename = os.path.join(args.output_dir, root_filename_template.format(
				ANALYSIS="ztt",
				CHANNEL=channel,
				ERA="13TeV"
		).replace("$", ""))
		cb.cp().ExtractShapes(root_filename, "$PROCESS", "$PROCESS_$SYSTEMATIC")
		
		for index, category in enumerate(args.categories):
			datacard_filename = os.path.join(args.output_dir, datacard_filename_template.format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					BINID=index,
					ERA="13TeV"
			).replace("$", ""))
			root_filename = os.path.join(args.output_dir, "common", root_filename_template.format(
					ANALYSIS="ztt",
					CHANNEL=channel,
					ERA="13TeV"
			).replace("$", ""))
			
			if not os.path.exists(os.path.dirname(root_filename)):
				os.makedirs(os.path.dirname(root_filename))
			cb.cp().channel([channel]).WriteDatacard(datacard_filename, root_filename)
	
	#cb.PrintAll()
	
	"""
	writer = ch.CardWriter(datacard_filename_template.replace("{", "").replace("}", ""),
	                       os.path.join("common", root_filename_template.replace("{", "").replace("}", "")))
	writer.WriteCards(args.output_dir, cb)
	"""

