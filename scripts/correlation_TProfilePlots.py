#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import sys
import os
import re

import Artus.Utility.jsonTools as jsonTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels
import ROOT
import glob
import itertools
import ROOT
import matplotlib.pyplot as plt
from matplotlib import cm
ROOT.PyConfig.IgnoreCommandLineOptions = True

def makePlots(variables, samples, data, dir_path, channel, category, sample_str):
	tProfiles = {}
	tProfiles_data = {}
	nice_channel = {
		"em": "$e\\mathrm{\\mu}$",
		"mt": "$\\mathrm{\\mu\\tau}$",
		"et": "$e\\mathrm{\\tau}$",
		"tt": "$\\mathrm{\\tau\\tau}$"}
	for var in variables:
		for var2 in variables:
			name = var+"+-+"+var2
			if name not in tProfiles.keys():
				tProfiles[name] = None
				tProfiles_data[name] = None
	var_pairs = []
	infiles = []
	for i, sample in enumerate(samples):
		infiles.append(ROOT.TFile(sample, "READ"))
		infile = infiles[-1]
		if i == 0:
			var_pairs_temp = []
			for keys in infile.GetListOfKeys():
				name = keys.GetName()
				var_pairs_temp.append(name)
			for name in tProfiles.keys():
				if name in var_pairs_temp:
					var_pairs.append(name)
					log.debug("add %s"%name)
					tProfiles[name] = infile.Get(name)
		else:
			for name in var_pairs:
				print name, tProfiles[name]
				tProfiles[name].Add(infile.Get(name))
	infile = ROOT.TFile(data)
	for name in var_pairs:
		tProfiles_data[name] = infile.Get(name)

	for name in var_pairs:
		mc_prof = tProfiles[name]
		data_prof = tProfiles_data[name]
		x_vals = [mc_prof.GetBinCenter(i) for i in range(1, mc_prof.GetNbinsX()+1, 1)]
		y_vals = [mc_prof.GetBinContent(i) for i in range(1, mc_prof.GetNbinsX()+1, 1)]
		y_vals_data = [data_prof.GetBinContent(i) for i in range(1, data_prof.GetNbinsX()+1, 1)]
		y_errs = [mc_prof.GetBinError(i) for i in range(1, mc_prof.GetNbinsX()+1, 1)]
		y_errs_data = [data_prof.GetBinError(i) for i in range(1, data_prof.GetNbinsX()+1, 1)]
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_xlabel(name.split("+-+")[0], size="x-large")
		ax.set_ylabel(name.split("+-+")[1], size="x-large")
		ax.errorbar(x_vals, y_vals, yerr=y_errs, label="MC", ls="None")
		ax.errorbar(x_vals, y_vals_data, yerr=y_errs_data, label="data", ls="None")
		lgd = ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0., numpoints=1)
		ans = ax.set_title("{channel}\t{category}".format(channel=nice_channel[channel], category=category), ha='left', x=0.01, y=1.01, size="x-large")
		if not os.path.exists(os.path.join(out_path, "combination", channel, category_string, sample_str)):
			os.makedirs(os.path.join(out_path, "combination", channel, category_string, sample_str))
		log.debug("save plot as: " + os.path.join(out_path, "combination", channel, category_string, sample_str, "%s.png"%name))
		fig.savefig(os.path.join(out_path, "combination", channel, category_string, sample_str, "%s.png"%name), bbox_extra_artists=(lgd, ans), bbox_inches='tight')
	infile.Close()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use directory of output from correlation_SampleProducer.py")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=["inclusive"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--higgs-masses", nargs="+", default=["125"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
							default="SameAsInput",
							help="Output dir. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	parser.add_argument("--plot-vars", nargs="+", default=["all"],
						help = "plot correlation for those variables. [Default: %(default)s]")
	parser.add_argument("--dimension", type = int, default = 5,
						help="dimension of the output matrices. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	dir_path = os.path.expandvars(args.input_dir)
	out_path = ""
	if args.output_dir == "SameAsInput":
		out_path = dir_path
	config_list = []
	parameters_list = args
	for channel in args.channels:
		for category in args.categories:
			sample_list = []
			sample_strings = []
			data_sample = ""
			overall_correlations = None
			category_string = ""
			if category != None:
				if(args.mssm):
					category_string = "catHttMSSM13TeV"
				if args.mva:
					category_string = "catMVAStudies"
				else:
					category_string = "catHtt13TeV"
				category_string = (category_string + "_{channel}_{category}").format(channel=channel, category=category)
			for sample in args.samples:
				log.debug("sample: %s; channel: %s; dir: %s; category: %s"%(sample, channel, dir_path, category_string))
				info_path = os.path.join(dir_path, channel, category_string, sample, "*.root")
				info_path = glob.glob(info_path)
				if len(info_path) > 1:
					log.critical("More than one file per channel-category-sample matched your discriprion --- aborting")
					sys.exit()
				info_path = info_path[0]
				if sample != "data":
					sample_list.append(info_path)
					sample_strings.append(sample)
				else:
					data_sample = info_path
			makePlots(args.plot_vars, sample_list, data_sample, out_path, channel, category_string, "_".join(sample_strings))
