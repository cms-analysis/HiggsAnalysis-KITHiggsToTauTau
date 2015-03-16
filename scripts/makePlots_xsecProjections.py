#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
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
	
	plot_configs = []
	
	backgrounds = [
		["QCD", 1.0, 1.0*3.0], # TODO: 1.0 is just a dummy value
		["tt", 245.2585, 245.2585*5.59001/1.42982],
		["DY", 3503.7, 3503.7*2.02904/1.14951],
		["W", 36257, 36257*2.09545/1.15786],
		["WW", 57.0, 57.0*2.62549/1.21510],
		["WZ", 32.0, 32.0*2.79381/1.23344],
		["ZZ", 8.3, 8.3*2.64949/1.21944],
	]
	signals = [
		["ggH", 15.13, 43.92],
		["qqH", 1.578, 3.748],
		["ZH", 0.4153, 0.8696],
		["WH", 0.7046, 1.380],
	]
	
	plot_configs.append({
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
		"markers" : ["bar", "line", "line"],
		"legend" : [0.7, 0.7],
		"filename" : "xsecs_8TeV_13TeV_1",
	})
	
	histograms = [
			ROOT.TH1F("histogram_8", "8 TeV", len(backgrounds+signals), 0.0, len(backgrounds+signals)),
			ROOT.TH1F("histogram_13", "13 TeV", len(backgrounds+signals), 0.0, len(backgrounds+signals)),
	]
	for index_h, histogram in enumerate(histograms):
		plot_configs[-1].setdefault("nicks", []).append(histogram.GetName())
		plot_configs[-1].setdefault("x_expressions", []).append(histogram.GetName())
		plot_configs[-1].setdefault("labels", []).append(histogram.GetTitle())
	
		for index_p, process in enumerate(backgrounds+signals):
			histogram.SetBinContent(index_p+1, process[index_h+1])
			histogram.SetBinError(index_p+1, 0.0)
			
			if index_h == 0:
				plot_configs[-1].setdefault("x_tick_labels", []).append(process[0])
	plot_configs[-1].setdefault("labels", []).append("")
	
	# only ratio
	plot_configs.append(copy.deepcopy(plot_configs[-1]))
	plot_configs[-1]["subplot_nicks"] = []
	plot_configs[-1]["nicks_blacklist"] = ["histogram"]
	plot_configs[-1]["filename"] = "xsecs_13TeV_over_8TeV_1"
	plot_configs[-1]["y_log"] = False
	plot_configs[-1]["y_lims"] = [1.4, 4.4]
	plot_configs[-1]["legend"] = None
	plot_configs[-1]["markers"] = ["bar"]
	plot_configs[-1]["y_label"] = "#sigma_{13 TeV} / #sigma_{8 TeV}"
	
	
	plot_configs.append(copy.deepcopy(plot_configs[-2]))
	plot_configs[-1]["nicks"] = []
	plot_configs[-1]["x_expressions"] = []
	plot_configs[-1]["labels"] = []
	plot_configs[-1]["x_tick_labels"] = []
	plot_configs[-1]["filename"] = "xsecs_8TeV_13TeV_2"
	plot_configs[-1]["divide_numerator_nicks"] = ["backgrounds_13"]
	plot_configs[-1]["divide_denominator_nicks"] = ["backgrounds_8"]
	
	background_histograms = [
			ROOT.TH1F("backgrounds_8", "8 TeV", len(backgrounds), 0.0, len(backgrounds)),
			ROOT.TH1F("backgrounds_13", "13 TeV", len(backgrounds), 0.0, len(backgrounds)),
	]
	for index_h, histogram in enumerate(background_histograms):
		plot_configs[-1].setdefault("nicks", []).append(histogram.GetName())
		plot_configs[-1].setdefault("x_expressions", []).append(histogram.GetName())
		plot_configs[-1].setdefault("labels", []).append(histogram.GetTitle())
	
		for index_p, process in enumerate(backgrounds):
			histogram.SetBinContent(index_p+1, process[index_h+1])
			histogram.SetBinError(index_p+1, 0.0)
			
			if index_h == 0:
				plot_configs[-1].setdefault("x_tick_labels", []).append(process[0])
	plot_configs[-1].setdefault("labels", []).append("")
	
	# only ratio
	plot_configs.append(copy.deepcopy(plot_configs[-1]))
	plot_configs[-1]["subplot_nicks"] = []
	plot_configs[-1]["nicks_blacklist"] = ["background"]
	plot_configs[-1]["nicks_whitelist"] = ["divide"]
	plot_configs[-1]["filename"] = "xsecs_13TeV_over_8TeV_2"
	plot_configs[-1]["y_log"] = False
	plot_configs[-1]["y_lims"] = [1.0, 4.4]
	plot_configs[-1]["legend"] = None
	plot_configs[-1]["markers"] = ["bar"]
	plot_configs[-1]["y_label"] = "#sigma_{13 TeV} / #sigma_{8 TeV}"
	plot_configs[-1]["labels"] = [""]
	plot_configs[-1]["legend"] = [0.75, 0.7]
	plot_configs[-1]["title"] = "m_{H} = 125 GeV"
	plot_configs[-1]["colors"] = [
		"kBlack",
		"#00a88f",
		"#4372c1",
		"#f69110",
		"#bf2229",
	]
	
	#plot_configs[-1]["analysis_modules"] = ["AddLine"]
	#plot_configs[-1]["x_lines"] = ["0.0 {x}".format(x=len(backgrounds))]
	signal_histograms = []
	for signal in signals:
		name = signal[0].replace(" ", "").replace("(", "").replace(")", "")
		signal_histograms.append(ROOT.TH1F(name, signal[0], 1, 0.0, len(backgrounds)))
		signal_histograms[-1].SetBinContent(1, signal[2]/signal[1])
		signal_histograms[-1].SetBinError(1, 0.0)
		plot_configs[-1].setdefault("nicks", []).append(name)
		plot_configs[-1].setdefault("nicks_whitelist", []).append(name)
		plot_configs[-1].setdefault("x_expressions", []).append(name)
		plot_configs[-1].setdefault("markers", []).append("line][")
		plot_configs[-1].setdefault("labels", []).append(signal[0])
		#plot_configs[-1].setdefault("y_lines", []).append("{y} {y}".format(y=ratio))
		#plot_configs[-1].setdefault("line-nicks", []).append(signal[0])
		#plot_configs[-1].setdefault("labels", []).append(signal[0])
	
	root_file.Write()
	root_file.Close()
	
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes)
	
	if os.path.exists:
		os.remove(root_filename)

