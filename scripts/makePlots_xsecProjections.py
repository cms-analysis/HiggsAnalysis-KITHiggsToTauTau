#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import tempfile

import ROOT

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make plots of projected cross sections.",
	                                 parents=[logger.loggingParser])
	
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	root_filename = tempfile.mktemp(suffix=".root")
	root_file = ROOT.TFile(root_filename, "RECREATE")
	
	plot_config = {
		"files" : [root_filename],
		"x_label" : "",
		"y_label" : "#sigma_{SM} / pb",
		"y_log" : True,
		"markers" : "LINE",
		"title" : "",
		"subplot_nicks" : ["divide"],
		"analysis_modules" : ["Divide"],
		"divide_numerator_nicks" : ["histogram_13"],
		"divide_denominator_nicks" : ["histogram_8"],
		"divide_result_nicks" : ["divide"],
		"colors" : ["kBlack", "kRed", "kRed"],
		"legend" : [0.7, 0.7],
		"filename" : "xsecs_8TeV_13TeV",
	}
	
	processes = [
		["  DY", 3503.7, 3503.7*2.02904/1.14951],
		["  t#bar{t}", 245.2585, 245.2585*5.59001/1.42982],
		["  W", 36257, 36257*2.09545/1.15786],
		["  WW", 57.0, 57.0*2.62549/1.21510],
		["  WZ", 32.0, 32.0*2.79381/1.23344],
		["  ZZ", 8.3, 8.3*2.64949/1.21944],
		["  QCD", 1.0, 1.0*3.0],
		["  ggH (125)", 15.13, 43.92],
		["  qqH (125)", 1.578, 3.748],
		["  WH (125)", 0.7046, 1.380],
		["  ZH (125)", 0.4153, 0.8696],
	]
	
	histograms = [
			ROOT.TH1F("histogram_8", "8 TeV", len(processes), 0.0, 1.0),
			ROOT.TH1F("histogram_13", "13 TeV", len(processes), 0.0, 1.0),
	]
	
	for index_h, histogram in enumerate(histograms):
		plot_config.setdefault("nicks", []).append(histogram.GetName())
		plot_config.setdefault("x_expressions", []).append(histogram.GetName())
		plot_config.setdefault("labels", []).append(histogram.GetTitle())
	
		for index_p, process in enumerate(processes):
			histogram.SetBinContent(index_p+1, process[index_h+1])
			histogram.SetBinError(index_p+1, 0.0)
			
			if index_h == 0:
				plot_config.setdefault("x_tick_labels", []).append(process[0])
	
	root_file.Write()
	root_file.Close()
	
	plot_config.setdefault("labels", []).append("")
	
	higgsplot.HiggsPlotter(list_of_config_dicts=[plot_config], list_of_args_strings=[args.args], n_processes=args.n_processes)
	
	if os.path.exists:
		os.remove(root_filename)

