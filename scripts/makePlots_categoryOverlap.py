#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse, copy, os, re, sys
import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.expressions as expressions
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Plot overlapping signal events.",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir",
						help="Path to ArtusOutput")
	parser.add_argument("-m", "--higgs-masses",nargs="+", default = ["125"],
						help="higgs mass [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-f", "--first-category", nargs="+", default=[],
	                    help="First Categories, can be specified multiple times. Several categories specified at once will be concatenated with or [Default: %(default)s]")
	parser.add_argument("-s", "--second-category", nargs="+", default=[],
						help="Second Categories, can be specified multiple times. Several categories specified at once will be concatenated with or[Default: %(default)s]")
	parser.add_argument("-S", "--Samples", nargs="+", default=["ggh", "qqh"],
	                    help="Samples to be compared [Default: %(default)s]")
	parser.add_argument("-o", "--output-file",
						default="Overlap",
						help="Output file. [Default: %(default)s]")
	parser.add_argument("-T", "--Ticklabels", nargs="+", default=["Category1", "Category2", "Overlap"],
	                    help="Ticklabels, replace by first name in first and second [Default: %(default)s]")
	parser.add_argument("-c", "--channel",
						default="mt",
						help="Channel. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
						help="Exclude (default) selection cuts. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	exp_dict = expressions.ExpressionsDict()
	plot_configs = []
	list_of_samples = [getattr(samples.Samples, sample) for sample in args.Samples]
	sample_settings = samples.Samples()

	config = sample_settings.get_config(
	samples=list_of_samples,
	channel=args.channel,
	category="",
	weight="1.0",
	higgs_masses=args.higgs_masses,
	normalise_signal_to_one_pb=False,
	exclude_cuts=args.exclude_cuts
	)
	firsts = [exp_dict.replace_expressions(s) for s in args.first_category]
	seconds = [exp_dict.replace_expressions(s) for s in args.second_category]
	config["x_expressions"] = "1*({first})+2*({second})".format(first=" || ".join(firsts), second=" || ".join(seconds))
	config["x_ticks"] = [1,2,3]
	config["x_bins"] = "3,0.5,3.5"
	config["x_tick_labels"] = args.Ticklabels
	config["filename"] = args.output_file
	config["directories"] = [args.input_dir]
	print config
	higgsplot.HiggsPlotter(list_of_config_dicts=[config],
							list_of_args_strings=[args.args])

