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
import numpy as np
import ROOT
import glob
import itertools
import ROOT
import matplotlib.pyplot as plt
from matplotlib import cm
ROOT.PyConfig.IgnoreCommandLineOptions = True

def makePlots(variables, samples, data, dir_path, channel, category, sample_str, corr_dicts, red_plot):
	tProfiles = {}
	tProfiles_data = {}
	nice_channel = {
		"em": "$e\\mathrm{\\mu}$",
		"mt": "$\\mathrm{\\mu\\tau}$",
		"et": "$e\\mathrm{\\tau}$",
		"tt": "$\\mathrm{\\tau\\tau}$"}
	corrs = []
	for correlation_dict_full in corr_dicts:
		corrs.append({})
		if correlation_dict_full is None:
			continue
		correlation_dict = correlation_dict_full["correlations"]
		ws = correlation_dict["weight_sum"]
		for varxy in correlation_dict.iterkeys():
			try:
				varx, vary = map(str, varxy.split("+-+"))
			except ValueError:
				continue
			corrs[-1]["var_%s"%varx] = (correlation_dict["var_%s"%varx] - (correlation_dict[varx]**2.)/ws)/ws
			corrs[-1]["var_%s"%vary] = (correlation_dict["var_%s"%vary] - (correlation_dict[vary]**2.)/ws)/ws
			try:
				#corrs[-1][varxy] = (correlation_dict[varxy]-correlation_dict[varx]*correlation_dict[vary]/ws)/ws/(
					#corrs[-1]["var_%s"%varx])**0.5/(corrs[-1]["var_%s"%vary])**0.5
				corrs[-1][varxy] = (correlation_dict[varxy]-correlation_dict[varx]*correlation_dict[vary]/ws)/ws
			except ZeroDivisionError:
				log.error("ZeroDivisonError: %s - Sample: %s - Category: %s" %(varxy,correlation_dict_full["request_nick"],correlation_dict_full["category"]))
				corrs[-1][varxy] = 0
			except ValueError:
				log.error("ValueError: %s - Sample: %s - Category: %s" %(varxy,correlation_dict_full["request_nick"],correlation_dict_full["category"]))
				corrs[-1][varxy] = 0


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
				#print name, tProfiles[name]
				tProfiles[name].Add(infile.Get(name))
	infile = ROOT.TFile(data)
	for name in var_pairs:
		tProfiles_data[name] = infile.Get(name)

	for name in var_pairs:
		x_var, y_var = name.split("+-+")
		mc_prof = tProfiles[name]
		data_prof = tProfiles_data[name]
		x_vals = np.array([mc_prof.GetBinCenter(i) for i in range(1, mc_prof.GetNbinsX()+1, 1)])
		y_vals = np.array([mc_prof.GetBinContent(i) for i in range(1, mc_prof.GetNbinsX()+1, 1)])
		y_vals_data = np.array([data_prof.GetBinContent(i) for i in range(1, data_prof.GetNbinsX()+1, 1)])
		y_errs = np.array([mc_prof.GetBinError(i) for i in range(1, mc_prof.GetNbinsX()+1, 1)])
		y_errs_data = np.array([data_prof.GetBinError(i) for i in range(1, data_prof.GetNbinsX()+1, 1)])

		cov_data = 0
		korr_data = 0
		cov_mc = 0
		korr_mc = 0

		try:
			cov_data = corrs[1][name] if name in corrs[1].keys() else float(corrs[1].get("+-+".join(name.split("+-+")[-1::-1]), "NaN"))
			korr_data = cov_data/(corrs[1]["var_%s"%x_var])**0.5/(corrs[1]["var_%s"%y_var])**0.5
			cov_mc = corrs[0][name] if name in corrs[0].keys() else float(corrs[0].get("+-+".join(name.split("+-+")[-1::-1]), "NaN"))
			korr_mc = cov_mc/(corrs[0]["var_%s"%x_var])**0.5/(corrs[0]["var_%s"%y_var])**0.5
		except ZeroDivisionError:
			log.error("ZeroDivisonError: %s - Channel: %s - Category: %s" %(name,channel,category))
			cov_data = corrs[1][name] if name in corrs[1].keys() else float(corrs[1].get("+-+".join(name.split("+-+")[-1::-1]), "NaN"))
			korr_data = 0
			cov_mc = corrs[0][name] if name in corrs[0].keys() else float(corrs[0].get("+-+".join(name.split("+-+")[-1::-1]), "NaN"))
			korr_mc = 0

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
		if not red_plot:
			y_min, y_max = ax.get_ylim()
			y_max = y_max + 0.2 * (y_max-y_min)
			ax.set_ylim(y_min, y_max)
			ax.annotate(s="Data Correlation: %1.2f"%(korr_data), xy=(x_vals[0],0.99*y_max-0.05*(y_max-y_min)), ha = "left", va = "center", fontsize='large')
			ax.annotate(s="MC Correlation: %1.2f"%(korr_mc), xy=(x_vals[0],0.99*y_max-0.15*(y_max-y_min)), ha = "left", va = "center", fontsize='large')
			fig.savefig(os.path.join(out_path, "combination", channel, category_string, sample_str, "%s.png"%name), bbox_extra_artists=(lgd, ans), bbox_inches='tight')
			log.debug("save plot as: " + os.path.join(out_path, "combination", channel, category_string, sample_str, "%s.png"%name))
		elif abs(korr_data-korr_mc) > 0.05:
			y_min, y_max = ax.get_ylim()
			y_max = y_max + 0.3 * (y_max-y_min)
			ax.set_ylim(y_min, y_max)
			ax.annotate(s="Data: Cor., Cov., sig(%s), sig(%s)"%(x_var, y_var), xy=(x_vals[0],0.99*y_max-0.05*(y_max-y_min)), ha = "left", va = "center", fontsize='large')
			ax.annotate(s="Data: %1.2f, %1.2f, %1.2f, %1.2f"%(korr_data, cov_data, corrs[1]["var_%s"%x_var]**0.5, corrs[1]["var_%s"%y_var]**0.5), xy=(x_vals[0],0.99*y_max-0.15*(y_max-y_min)), ha = "left", va = "center", fontsize='large')
			ax.annotate(s="MC: %1.2f, %1.2f, %1.2f, %1.2f"%(korr_mc, cov_mc, corrs[0]["var_%s"%x_var]**0.5, corrs[0]["var_%s"%y_var]**0.5), xy=(x_vals[0],0.99*y_max-0.25*(y_max-y_min)), ha = "left", va = "center", fontsize='large')
			fig.savefig(os.path.join(out_path, "combination", channel, category_string, sample_str, "%s.png"%name), bbox_extra_artists=(lgd, ans), bbox_inches='tight')
			log.debug("save plot as: " + os.path.join(out_path, "combination", channel, category_string, sample_str, "%s.png"%name))
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
	parser.add_argument("--use-corr-dict", action="store_true",
							default=False,
							help="Use Json files instead of calculating correlation from profile. [Default: %(default)s]")
	parser.add_argument("--corr-dict-name", default = "Correlations.json", help="Name of json file. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	parser.add_argument("--plot-vars", nargs="+", default=["all"],
						help = "plot correlation for those variables. [Default: %(default)s]")
	parser.add_argument("--dimension", type = int, default = 5,
						help="dimension of the output matrices. [Default: %(default)s]")
	parser.add_argument("--plot-critical", default = False, action="store_true", help="Plot ONLY histograms with a critical level of differences. [Default: %(default)s]")
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
			mc_corr = None
			data_corr = None
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
					if args.use_corr_dict:
						if mc_corr is None:
							mc_corr = jsonTools.JsonDict(info_path.replace("Histograms.root", args.corr_dict_name))
						else:
							for namexy, varxy  in jsonTools.JsonDict(info_path.replace("Histograms.root", args.corr_dict_name))["correlations"].iteritems():
								mc_corr["correlations"][namexy] = mc_corr["correlations"].get(namexy, 0) + varxy
				else:
					data_sample = info_path
					if args.use_corr_dict:
						data_corr = jsonTools.JsonDict(info_path.replace("Histograms.root", args.corr_dict_name))
			#print mc_corr["correlations"], data_corr["correlations"]
			#sys.exit()
			makePlots(args.plot_vars, sample_list, data_sample, out_path, channel, category_string, "_".join(sample_strings), [mc_corr, data_corr], args.plot_critical)
