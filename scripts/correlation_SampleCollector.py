#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
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

def plot_correlations(parameters, correlation_dict, sample, channel, dir_path, outname):
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
			corr_vars[varxy] = None
		except ValueError:
			log.error("ValueError: %s" %varxy)
			corr_vars[varxy] = None
	jsonTools.JsonDict(corr_vars).save(os.path.join(dir_path,"%s_correlations.json"%channel),indent=4)
	whole = len(parameters)/5
	param_lists = []
	for i in range(whole):
		param_lists.append([])
		for j in range(5):
			param_lists[i].append(parameters[5*i+j])
	param_lists.append(parameters[5*whole:])
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
			counts, xedges, yedges, cax = ax.hist2d(x_vals, y_vals, weights=weights, bins=[len(x_params), len(y_params)], range=[(0,len(x_params)),(0,len(y_params))], cmap=cm.coolwarm, vmin=-0.5, vmax=0.5)
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
			cbar = fig.colorbar(cax, ticks=[-0.5, 0, 0.5])
			cbar.ax.set_yticklabels(['<-0.5', '0', '>0.5'])  # vertically oriented colorbar
			ax.grid(True, which="minor", linewidth = 1.5)
			ax.tick_params(axis='both', which='major', pad=5)
			plt.tight_layout()
			plt.savefig(os.path.join(dir_path,"%s-%i-%i_corM.png"%(outname,i,j)))
			plt.savefig(os.path.join(dir_path,"%s-%i-%i_corM.pdf"%(outname,i,j)))
			plt.savefig(os.path.join(dir_path,"%s-%i-%i_corM.eps"%(outname,i,j)))



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use directory of ooutput from correlation_SampleProducer.py")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						choices=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("-o", "--output-file",
							default="combination",
							help="Output file. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	dir_path = os.path.expandvars(args.input_dir)
	config_list = []
	for sample in args.samples:
		file_dir = os.path.join(dir_path, sample)
		if os.path.exists(file_dir):
			for channel in args.channels:
				config_list.append(jsonTools.JsonDict(os.path.join(file_dir, "%s_corr-config.json"%channel)))
				config = config_list[-1]
				log.debug("sample: %s; channel: %s; dir: %s"%(sample, channel, file_dir))
				log.debug("parameters: %s" %str(config["parameters_list"]))
				plot_correlations(copy.copy(config["parameters_list"]), config["correlations"], sample, channel, file_dir, channel)
	overall_correlations = None
	for i,config in enumerate(config_list):
		if config["request_nick"] == "data":
			continue
		if overall_correlations is None:
			overall_correlations = copy.copy(config["correlations"])
		else:
			for varxy in overall_correlations.iterkeys():
				overall_correlations[varxy] += config["correlations"][varxy]
	if not os.path.exists(os.path.join(dir_path, "combination")):
		os.makedirs(os.path.join(dir_path, "combination"))

	plot_correlations(config_list[0]["parameters_list"], overall_correlations, "Combination" ,config_list[0]["channel"], os.path.join(dir_path, "combination"), args.output_file)
	#calculate variances and correlations -> moved to collector_script