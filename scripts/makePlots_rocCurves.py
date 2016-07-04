#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import fnmatch
import sys
import re
import ROOT
import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as import_binnings
import matplotlib.pyplot as plt


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Make overtraining control plots.",
											parents=[logger.loggingParser])
	parser.add_argument("-i", "--input_dirs", nargs="*", required= True,
						help="Input dirs")
	parser.add_argument("-m", "--matching", default="*.root", required = True,
						help="Match this string as input root files. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*", default = [],
						help="Additional Quantities")
	parser.add_argument("-b", "--bins", type=int, default=100,
						help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-l", "--labels", nargs="*",required = True,
						default = [], help="labels")
	parser.add_argument("-c", "--colors", nargs="*", required = True,
						default = [], help="colors")
	parser.add_argument("-o", "--output-dir",
						default="$CMSSW_BASE/src/plots/",
						help="Output directory. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
						help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
						help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-p", "--n-plots", type=int,
							help="Number of plots. [Default: all]")
	#parser.add_argument("--calculate-separation", action="store_true", default =False,
							#help="calculate separation using TestSample")
	#parser.add_argument("--no-plot", action="store_true", default =False,
							#help="skip plotting")
	args = parser.parse_args()
	logger.initLogger(args)
	nice_channel = {
		"em": "#scale[1.5]{e#mu ",
		"mt": "#scale[1.5]{#mu#tau_{h} ",
		"et": "#scale[1.5]{e#tau_{h} ",
		"tt": "#scale[1.5]{#tau_{h}#tau_{h} "}
	binnings_dict = import_binnings.BinningsDict()
	input_bdts = {}
	for i,in_dir in enumerate(args.input_dirs):
		input_files = [(dirpath, f) for dirpath, dirnames, files in os.walk(in_dir) for f in fnmatch.filter(files, args.matching)]
		for path, file_name in input_files:
			bdt_name = file_name[:-7] #cut away TX.root
			if not bdt_name in input_bdts.keys():
				input_bdts[bdt_name] = {in_dir: [os.path.join(path, file_name)]}
			elif in_dir not in input_bdts[bdt_name].keys():
				input_bdts[bdt_name][in_dir] = [os.path.join(path, file_name)]
			else:
				input_bdts[bdt_name][in_dir].append(os.path.join(path, file_name))
	configs_list = []
	jsonTools.JsonDict(input_bdts).save("testPlot.json", indent=4)
	for name, plot in input_bdts.iteritems():
		bdt_var = "BDT_"+name
		split_parts = name.split("_")
		channel = split_parts[0]
		title = nice_channel[channel] + split_parts[1].replace("Jets", " Jet") + " %s"%split_parts[2] + "}"
		config = {
		"analysis_modules": [
			"NormalizeToUnity",
			"CutEfficiency"
			],
		"filename": "ROC_"+name,
		"files": [],
		"output_dir": args.output_dir,
		"folders": [
			"TestTree"
				],
		"legend_markers": [
			"PE"
				],
		"title": title,
		"x_label": "Background Rejection",
		"y_label": "Signal Efficiency",
		"legend": [
			0.2,
			0.18,
			0.65,
			0.45
				],
		"markers": [
			"P"
				],
		"labels": [],
		"colors": [],
		"x_bins": [],
		"formats": ["pdf", "png"],
		"x_expressions": [],
		"weights": [
			"weight*(classID==1)",
			"weight*(classID==0)"
				],
		"nicks": [],
		"cut_efficiency_bkg_nicks": [],
		"cut_efficiency_modes": ["sigEffVsBkgRej"],
		"cut_efficiency_nicks": [],
		"cut_efficiency_sig_nicks": []
			}
		first = True
		accepted_counter = 0
		for count,indir in enumerate(args.input_dirs):
			if not indir in plot.keys():
				continue
			c_file = " ".join(plot[indir])
			if first:
				first = False
				for add_var in args.quantities:
					config["files"] += [c_file, c_file]
					bins = binnings_dict.get_binning(channel+"_"+add_var)
					if " " in bins:
						tmp_bins = bins.split(" ")
						bins = str(args.bins)+","+tmp_bins[0]+","+tmp_bins[-1]
					elif "," in bins:
						tmp_bins = bins.split(",")
						bins = str(args.bins)+","+tmp_bins[1]+","+tmp_bins[-1]
					config["x_expressions"] += [add_var, add_var]
					config["x_bins"] += [bins, bins]
					config["nicks"] += ["noplot_sig_{var}_{count}".format(var=add_var, count=count),
										"noplot_bkg_{var}_{count}".format(var=add_var, count=count)]
					config["cut_efficiency_sig_nicks"] += ["noplot_sig_{var}_{count}".format(var=add_var, count=count)]
					config["cut_efficiency_bkg_nicks"] += ["noplot_bkg_{var}_{count}".format(var=add_var, count=count)]
					config["cut_efficiency_nicks"] += ["roc_{var}_{count}".format(var=add_var, count=count)]
					config["colors"] += [args.colors[accepted_counter]]
					config["labels"] += [args.labels[accepted_counter]]
					accepted_counter += 1

			config["files"] += [c_file, c_file]
			bins = str(args.bins)+",-1,1"
			config["x_expressions"] += [bdt_var, bdt_var]
			config["x_bins"] += [bins, bins]
			config["nicks"] += ["noplot_sig_{var}_{count}".format(var=accepted_counter, count=count),
								"noplot_bkg_{var}_{count}".format(var=accepted_counter, count=count)]
			config["cut_efficiency_sig_nicks"] += ["noplot_sig_{var}_{count}".format(var=accepted_counter, count=count)]
			config["cut_efficiency_bkg_nicks"] += ["noplot_bkg_{var}_{count}".format(var=accepted_counter, count=count)]
			config["cut_efficiency_nicks"] += ["roc_{var}_{count}".format(var=accepted_counter, count=count)]
			config["colors"] += [args.colors[accepted_counter]]
			config["labels"] += [args.labels[accepted_counter]]
			accepted_counter += 1
		configs_list.append(config)
	higgsplot.HiggsPlotter(list_of_config_dicts=configs_list,
								list_of_args_strings=[args.args],
								n_processes=args.n_processes, n_plots=args.n_plots)



