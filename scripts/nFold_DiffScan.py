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
import glob
import itertools
import ROOT
import matplotlib.pyplot as plt
#import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples

def calculate_diff(filename, htt_name, sigma_value=0.50):
	tfile = ROOT.TFile(filename, "READ")
	ztt = tfile.Get("ztt")
	zll = tfile.Get("zll")
	wj = tfile.Get("wj")
	qcd = tfile.Get("qcd")
	vv = tfile.Get("vv")
	data = tfile.Get("data")
	ttj = tfile.Get("ttj")
	sig_hist = tfile.Get(htt_name)
	mc_hist = ROOT.TH1F("mc_events", "mc_events", 1000,0,2)
	#Probably add signal_only histogram at some point
	for hist in [ztt, zll, wj, qcd, vv, ttj]:
		mc_hist.Add(hist)
	mc_sum = 0
	data_sum = 0
	sig_sum = 0
	mc_tot = mc_hist.Integral()
	data_tot = data.Integral()
	sig_tot = sig_hist.Integral()
	data_point = False
	mc_point = False
	sig_point = False
	mc_value = 0
	data_value = 0
	sig_value = 0
	for j in range(1,1001,1):
		sig_sum += sig_hist.GetBinContent(j)
		mc_sum += mc_hist.GetBinContent(j)
		data_sum += data.GetBinContent(j)
		if (not mc_point) and (abs(mc_sum/mc_tot - sigma_value)<0.001 or mc_sum/mc_tot>sigma_value):
			mc_point = True
			lower = mc_hist.GetBinLowEdge(j)
			width = mc_hist.GetBinWidth(j)
			mc_value = lower+width
		if (not sig_point) and (abs(sig_sum/sig_tot - sigma_value)<0.001 or sig_sum/sig_tot>sigma_value):
			sig_point = True
			lower = sig_hist.GetBinLowEdge(j)
			width = sig_hist.GetBinWidth(j)
			sig_value = lower+width
			#break
		if (not data_point) and (abs(data_sum/data_tot - sigma_value)<0.001 or data_sum/data_tot>sigma_value):
			data_point = True
			lower = data.GetBinLowEdge(j)
			width = data.GetBinWidth(j)
			data_value = lower+width
	tfile.Close()
	del tfile
	return sig_value + abs(mc_value-sig_value), mc_value, sig_value, data_value

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use dir with all bdt plot subdirs")
	parser.add_argument("-m", "--higgs-mass", required=True,
						help="higgs mass")
	parser.add_argument("--legend", default="upper left",
						help="position of legend, use 'matplotlib position' as argument[Default:%(default)s]")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000.0,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("-o", "--output-file",
							default="nFoldDiffScan",
							help="Output file. [Default: %(default)s]")
	#parser.add_argument("-e", "--exclude-log", nargs="+",
						#default=[],
						#help="exclude training log files from collection. [Default: %(default)s]")
	#parser.add_argument("-c", "--combine-log", nargs="+",
						#default=["*_TrainingLog.json"],
						#help="include training log files into collectionm [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)

	list_of_roots = glob.glob(os.path.join(args.input_dir, "*/sqrt_diff.root"))
	x_names = [] #store names of BDTs
	x_values = [] #store dummy x-value for plotting
	y_shift_values = []
	y_sig_values = []
	y_mc_values = [] #store diff-value for mc
	#y_data_values = [] #store diff-value for data

	for i,root_file in  enumerate(list_of_roots):
		shift, mc_value, sig_value, data_value = calculate_diff(root_file, "htt%s"%args.higgs_mass, sigma_value=0.50)
		x_values.append(i)
		dirpath, filename = os.path.split(root_file)
		dirpath, filename = os.path.split(dirpath)
		x_names.append(filename)
		y_shift_values.append(shift)
		y_mc_values.append(mc_value)
		y_sig_values.append(sig_value)
		#y_data_values.append(data_value)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	print x_names, y_shift_values, y_sig_values, y_mc_values, y_data_values
	ax.plot(x_values, y_shift_values, label="shifts", color="red", marker="x", markersize = 12.5, ls = "None", markeredgewidth=2)
	ax.plot(x_values, y_sig_values, label="signal", color="blue", marker="o", markersize = 12.5, ls = "None", markeredgewidth=2)
	ax.plot(x_values, y_mc_values, label="bkg", color="green", marker="+", markersize = 12.5, ls = "None", markeredgewidth=2)
	#ax.plot(x_values, y_data_values, label="data", color="orange", marker=".", markersize = 12.5, ls = "None", markeredgewidth=2)
	ax.set_xticks(x_values)
	ax.set_xlim(-1, len(x_values))
	ax.set_ylim(0.9*min(y_data_values+y_mc_values+y_shift_values+y_sig_values), 1.1*max(y_data_values+y_mc_values+y_shift_values+y_sig_values))
	ax.set_xticklabels(x_names, rotation = 90, size='x-large', va='center', ha='right', rotation_mode='anchor')
	lgd = ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
	ax.set_ylabel("$50\\%\\mathrm{\\,of}\\mathrm{\\,events}<\\sqrt{\\sum((\\mathrm{T}(i)-\\mathrm{Fin})/(\\mathrm{N}-1))^2}$")
	#plt.tight_layout()
	plt.savefig("%s.png"%args.output_file, bbox_extra_artists=(lgd,), bbox_inches='tight')
	log.info("create plot %s.png"%args.output_file)
	plt.savefig("%s.pdf"%args.output_file, bbox_extra_artists=(lgd,), bbox_inches='tight')
	log.info("create plot %s.pdf"%args.output_file)
	plt.savefig("%s.eps"%args.output_file, bbox_extra_artists=(lgd,), bbox_inches='tight')
	log.info("create plot %s.eps"%args.output_file)
