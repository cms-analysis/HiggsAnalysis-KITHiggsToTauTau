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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.labels as labels
import ROOT
import glob
import itertools
import ROOT
import matplotlib.pyplot as plt
from matplotlib import cm
ROOT.PyConfig.IgnoreCommandLineOptions = True

def plot_correlations(parameters, correlation_dict, dir_path, channel, category, sample, dimension=7):
	if isinstance(channel, list):
		channel = channel[0]
	corr_vars = {}
	ws = correlation_dict["weight_sum"]
	labeldict = labels.LabelsDict()
	for varxy in correlation_dict.iterkeys():
		try:
			varx, vary = map(str, varxy.split("+-+"))
		except ValueError:
			continue
		corr_vars["var_%s"%varx] = (correlation_dict["var_%s"%varx] - (correlation_dict[varx]**2.)/ws)/ws
		corr_vars["var_%s"%vary] = (correlation_dict["var_%s"%vary] - (correlation_dict[vary]**2.)/ws)/ws
		try:
			corr_vars[varxy] = (correlation_dict[varxy]-correlation_dict[varx]*correlation_dict[vary]/ws)/ws/(
				corr_vars["var_%s"%varx])**0.5/(corr_vars["var_%s"%vary])**0.5
		except ZeroDivisionError:
			log.error("ZeroDivisonError: %s" %varxy)
			corr_vars[varxy] = 0
		except ValueError:
			log.error("ValueError: %s" %varxy)
			corr_vars[varxy] = 0
	jsonTools.JsonDict(corr_vars).save(os.path.join(dir_path, channel, category_string, sample, "FinalCorrelation.json"), indent=4)
	whole = len(parameters)/dimension
	whole = max(whole, 1)
	max_iterate = min(dimension, len(parameters))

	param_lists = []
	for i in range(whole):
		param_lists.append([])
		for j in range(max_iterate):
			param_lists[i].append(parameters[max_iterate*i+j])
	param_lists.append(parameters[max_iterate*whole:])
	if param_lists[-1] == []:
		param_lists.pop(-1)
	param_lists.append(parameters)
	for i in range(len(param_lists)):
		for j in range(i,len(param_lists)):
			if j == len(param_lists)-1 and j != i:
				continue
			x_params = param_lists[i]
			y_params = param_lists[j]
			x_vals = []
			y_vals = []
			weights = []
			for pairs in itertools.product(x_params, y_params):
				x_vals.append(x_params.index(pairs[0])+0.5)
				y_vals.append(y_params.index(pairs[1])+0.5)
				try:
					weights.append(corr_vars["+-+".join(pairs)])
				except KeyError:
					weights.append(corr_vars["+-+".join((pairs[1],pairs[0]))])
			fig = plt.figure()
			ax = fig.add_subplot(111)
			counts, xedges, yedges, cax = ax.hist2d(x_vals, y_vals, weights=weights, bins=[len(x_params), len(y_params)], range=[(0,len(x_params)),(0,len(y_params))], cmap=cm.coolwarm, vmin=-1.0, vmax=1.0)
			title_string = "Correlation Matrix: %s $\\rightarrow$ %s"%(labeldict.get_nice_label(sample) ,labeldict.get_nice_label("channel_%s"%channel ))
			#title_string = title_string.replace("$", "")
			#title_string = "$"+title_string+"$"
			ax.set_title(title_string)
			ax.set_xticks([x+0.5 for x in range(len(x_params))])
			ax.set_yticks([x+0.5 for x in range(len(y_params))])
			ax.set_xticks([x for x in range(len(x_params))], minor = True)
			ax.set_yticks([x for x in range(len(y_params))], minor = True)
			if j == len(param_lists)-1:
				ax.set_xticklabels([labeldict.get_nice_label(channel+"_"+x).replace(" / \\mathrm{GeV}", "") for x in x_params], rotation = 45, size='medium', va='center', ha='right', rotation_mode='anchor')
				ax.set_yticklabels([labeldict.get_nice_label(channel+"_"+x).replace(" / \\mathrm{GeV}", "") for x in y_params], rotation = 45, size='medium', va='center', ha='right', rotation_mode='anchor')
				for triples in zip(x_vals, y_vals, weights):
					ax.annotate(s="%1.2f"%triples[2], xy=(triples[0],triples[1]), ha = "center", va = "center", fontsize='xx-small')
			else:
				ax.set_xticklabels([labeldict.get_nice_label(channel+"_"+x).replace(" / \\mathrm{GeV}", "") for x in x_params], rotation = 45, size='x-large', va='center', ha='right', rotation_mode='anchor')
				ax.set_yticklabels([labeldict.get_nice_label(channel+"_"+x).replace(" / \\mathrm{GeV}", "") for x in y_params], rotation = 45, size='x-large', va='center', ha='right', rotation_mode='anchor')
				for triples in zip(x_vals, y_vals, weights):
					ax.annotate(s="%1.2f"%triples[2], xy=(triples[0],triples[1]), ha = "center", va = "center", size='large')
			# Add colorbar, make sure to specify tick locations to match desired ticklabels
			cbar = fig.colorbar(cax, ticks=[-1.0, 0, 1.0])
			cbar.ax.set_yticklabels(['-1.0', '0', '1.0'])  # vertically oriented colorbar
			ax.grid(True, which="minor", linewidth = 1.5)
			ax.tick_params(axis='both', which='major', pad=5)
			plt.tight_layout()
			outname = "CorrelationPlot"
			plt.savefig(os.path.join(dir_path, channel, category_string, sample, "%s-%i-%i_corM.png"%(outname,i,j)))
			log.info("create plot %s" %os.path.join(dir_path, channel, category_string, sample, "%s-%i-%i_corM.png"%(outname,i,j)))
			plt.savefig(os.path.join(dir_path, channel, category_string, sample, "%s-%i-%i_corM.png"%(outname,i,j)))
			log.info("create plot %s" %os.path.join(dir_path, channel, category_string, sample, "%s-%i-%i_corM.png"%(outname,i,j)))
			plt.savefig(os.path.join(dir_path, channel, category_string, sample, "%s-%i-%i_corM.png"%(outname,i,j)))
			log.info("create plot %s" %os.path.join(dir_path, channel, category_string, sample, "%s-%i-%i_corM.png"%(outname,i,j)))
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
	parameters_list = []
	for channel in args.channels:
		for category in args.categories:
			sample_list = []
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
				log.debug("sample: %s; channel: %s; dir: %s"%(sample, channel, dir_path))
				info_path = os.path.join(dir_path, channel, category_string, sample, "Correlations.json")
				info_path = glob.glob(info_path)
				if len(info_path) > 1:
					log.critical("More than one file per channel-category-sample matched your discriprion --- aborting")
					sys.exit()
				info_path = info_path[0]
				config_list.append(jsonTools.JsonDict(info_path))
				config = config_list[-1]
				if len(parameters_list) == 0:
					if "all" in args.plot_vars:
						parameters_list = config["parameters_list"]
					else:
						for var in args.plot_vars:
							if var in config["parameters_list"]:
								parameters_list.append(var)
							else:
								log.error("You requested to plot correlation for variable {var}, which is not present in the calculated correlation values".format(var=var))
								sys.exit()
					log.debug("parameters: %s" %str(parameters_list))
					plot_correlations(parameters_list, copy.copy(config["correlations"]), out_path, channel, category_string, sample, args.dimension)
				else:
					log.debug("parameters: %s" %str(parameters_list))
					plot_correlations(parameters_list, copy.copy(config["correlations"]), out_path, channel, category_string, sample, args.dimension)
				if sample == "data":
					continue
				if overall_correlations is None:
					overall_correlations = copy.copy(config["correlations"])
				else:
					for varxy in overall_correlations.iterkeys():
						overall_correlations[varxy] += config["correlations"][varxy]
				sample_list.append(sample)
			if not os.path.exists(os.path.join(out_path, "combination", channel, category_string, "_".join(sample_list))):
				os.makedirs(os.path.join(out_path, "combination", channel, category_string, "_".join(sample_list)))
			plot_correlations(parameters_list, overall_correlations, os.path.join(out_path, "combination"), channel, category_string, "_".join(sample_list), args.dimension)