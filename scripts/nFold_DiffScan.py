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

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Collect and Combine Correlation Information",
									 parents=[logger.loggingParser])
	parser.add_argument("-i", "--input-dir", required=True,
						help="Input directory. Use dir with all bdt plot subdirs")
	parser.add_argument("-m", "--higgs-mass", required=True,
						help="higgs mass")
	parser.add_argument("--legend", default="upper left",
						help="position of legend, use 'matplotlib position' as argument[Default:%(default)s]")
	parser.add_argument("--lumi", type=float, default=2.301,
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
	y_mc_values = [] #store diff-value for mc
	y_data_values = [] #store diff-value for data

	for i,root_file in  enumerate(list_of_roots):
		tfile = ROOT.TFile(root_file, "READ")
		x_values.append(i)
		dirpath, filename = os.path.split(root_file)
		dirpath, filename = os.path.split(dirpath)
		x_names.append(filename)
		ztt = tfile.Get("ztt")
		zll = tfile.Get("zll")
		wj = tfile.Get("wj")
		qcd = tfile.Get("qcd")
		vv = tfile.Get("vv")
		data = tfile.Get("data")
		ttj = tfile.Get("ttj")
		htt = tfile.Get("htt%s"%args.higgs_mass)
		mc_hist = ROOT.TH1F("mc_events", "mc_events", 1000,0,2)
		for hist in [ztt, zll, wj, qcd, vv, ttj, htt]:
			mc_hist.Add(hist)
		mc_sum = 0
		data_sum = 0
		mc_tot = mc_hist.Integral()
		data_tot = data.Integral()
		data_point = False
		mc_point = False
		print mc_tot
		print data_tot
		for j in range(1,1001,1):
			if j%100 == 1:
				print mc_hist.GetBinContent(j)
				print data.GetBinContent(j)
			mc_sum += mc_hist.GetBinContent(j)
			data_sum += data.GetBinContent(j)
			if (not mc_point) and (abs(mc_sum/mc_tot - 0.95)<0.01 or mc_sum/mc_tot>0.95):
				mc_point = True
				y_mc_values.append(mc_hist.GetBinCenter(j))

			if (not data_point) and (abs(data_sum/data_tot - 0.95)<0.01 or data_sum/data_tot>0.95):
				data_point = True
				y_data_values.append(data.GetBinCenter(j))

	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.plot(x_values, y_mc_values, label="MC", color="blue", marker="x", markersize = 12.5, ls = "None", markeredgewidth=2)
	ax.plot(x_values, y_data_values, label="Data", color="red", marker=".", markersize = 12.5, ls = "None",)
	ax.set_xticks(x_values)
	ax.set_xlim(-1, len(x_values))
	ax.set_ylim(0.9*min(y_data_values+y_mc_values), 1.1*max(y_data_values+y_mc_values))
	ax.set_xticklabels(x_names, rotation = 90, size='x-large', va='center', ha='right', rotation_mode='anchor')
	ax.legend(loc=args.legend)
	ax.set_ylabel("$95\\%\\mathrm{\\,of}\\mathrm{\\,events}<\\sqrt{\\sum((\\mathrm{T}(i)-\\mathrm{Fin})/(\\mathrm{N}-1))^2}$")
	plt.tight_layout()
	plt.savefig("%s.png"%args.output_file)
	log.info("create plot %s.png"%args.output_file)
	plt.savefig("%s.pdf"%args.output_file)
	log.info("create plot %s.pdf"%args.output_file)
	plt.savefig("%s.eps"%args.output_file)
	log.info("create plot %s.eps"%args.output_file)