#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os
import shlex

import ROOT

from HiggsAnalysis.HiggsToTauTau.utils import parseArgs

import Artus.Utility.jsonTools as jsonTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make prefit/postfit plots based on datacards and max. likelihood fit results.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-d", "--datacards", nargs="+", required=True,
	                    help="Datacards.")
	parser.add_argument("-f", "--fit-results", nargs="+", default=[None],
	                    help="ROOT outputs of the RooFit max. likelihood fit. [Default: <datacard directory>/out/mlfit.root]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--data-processes", nargs="+",
	                    default=["data_obs"],
	                    help="Data processes. [Default: %(default)s]")
	parser.add_argument("--background-processes", nargs="+",
	                    default=["ZTT", "ZL", "ZJ", "TT", "W", "VV", "QCD"],
	                    help="Background processes. [Default: %(default)s]")
	parser.add_argument("--signal-processes", nargs="+",
	                    default=["TotalSig"],
	                    help="Signal processes. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dirs", nargs="+", default=[None],
	                    help="Output directories. [Default: <datacard directory>/shapes]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	# preparation of arguments
	args.higgs_masses = parseArgs(args.higgs_masses)
	
	if len(args.fit_results) > 1 and len(args.fit_results) != len(args.datacards):
		log.warning("%d fit results need to be expanded/truncated to %d datacards!" % (len(args.fit_results), len(args.datacards)))
	args.fit_results = (args.fit_results*len(args.datacards))[:len(args.datacards)]
	
	if len(args.output_dirs) > 1 and len(args.output_dirs) != len(args.datacards):
		log.warning("%d output directories need to be expanded/truncated to %d datacards!" % (len(args.output_dirs), len(args.datacards)))
	args.output_dirs = (args.output_dirs*len(args.datacards))[:len(args.datacards)]
	
	# preparation of plots
	plot_configs = []
	for datacard, fit_result, output_dir in zip(args.datacards, args.fit_results, args.output_dirs):
		if fit_result is None:
			fit_result = os.path.join(os.path.dirname(datacard), "out", "mlfit.root")
		if output_dir is None:
			output_dir = os.path.join(os.path.dirname(datacard), "shapes")
		
		for mass in args.higgs_masses:
			mass = str(mass)
			
			mass_output_dir = os.path.join(output_dir, mass)
			if not os.path.exists(mass_output_dir):
				os.makedirs(mass_output_dir)
			
			for index_fit_type, fit_type in enumerate(["fit_s", "fit_b"]):
				shapes_root_file = os.path.join(mass_output_dir, os.path.splitext(os.path.basename(datacard))[0]+"_"+fit_type+".root")
				command = "$CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/CombineHarvester/CombineTools/bin/PostFitShapes" + \
				          " --datacard " + datacard + \
				          " --fitresult " + fit_result + ":" + fit_type + \
				          " --mass " + mass + \
				          " --postfit --sampling" + \
				          " --output " + shapes_root_file
				command = os.path.expandvars(command)
				logger.subprocessCall(shlex.split(command))
				log.info("Created shapes \"%s\"." % shapes_root_file)
	
				root_file = ROOT.TFile(shapes_root_file, "READ")
				keys = root_file.GetListOfKeys()
				
				directories = [keys.At(index).GetName() for index in range(keys.GetSize()) if keys.At(index).GetClassName() == "TDirectoryFile"]
				histograms = {}
				
				for directory in directories:
					root_dir = root_file.Get(directory)
					keys = root_dir.GetListOfKeys()
					histograms[directory] = [keys.At(index).GetName() for index in range(keys.GetSize()) if keys.At(index).GetClassName().startswith("TH")]
		
					# remove shape histograms
					histograms[directory] = [h for h in histograms[directory] if not ("_" in h and (h.endswith("Up") or h.endswith("Down")))]
				
				root_file.Close()
				
				datas = {directory : [h for h in histos if h in args.data_processes] for directory, histos in histograms.items()}
				backgrounds = {directory : [h for h in histos if h in args.background_processes] for directory, histos in histograms.items()}
				signals = {directory : [h for h in histos if h in args.signal_processes] for directory, histos in histograms.items()}
				
				colors = {
					"data_obs" : "#000000",
					"ZTT" : "#FFCC66",
					"ZL" : "#4496C8",
					"ZJ" : "#64B6E8",
					"TT" : "#9999CC",
					"VV" : "#DE5A6A",
					"W" : "#FE7A8A",
					"QCD" : "#FFCCFF",
					"TotalSig" : "#000000",
				}
				
				for directory in list(set(datas.keys()+backgrounds.keys()+signals.keys())):
					if "prefit" in directory and index_fit_type > 0:
						continue
					
					data = datas.get(directory, [])
					background = backgrounds.get(directory, [])
					signal = signals.get(directory, [])
					
					plot_configs.append(jsonTools.JsonDict())
		
					plot_configs[-1]["files"] = [shapes_root_file]
					plot_configs[-1]["folders"] = [directory]
					plot_configs[-1]["x_expressions"] = data + background + signal
					plot_configs[-1]["nicks"] = (["data"]*len(data)) + background + (["sig"]*len(signal))
					plot_configs[-1]["stacks"] = ["data"] + (["bkg"]*len(background)) + (["sig"]*(1 if len(signal) > 0 else 0))
					plot_configs[-1]["ratio"] = args.ratio
					plot_configs[-1]["markers"] = ["E"] + (["HIST"]*len(background)) + (["L"]*(1 if len(signal) > 0 else 0))
					plot_configs[-1]["colors"] = [colors.get(x, "#000000") for index, x in enumerate(plot_configs[-1]["x_expressions"])]
					plot_configs[-1]["labels"] = ["Data"] + background + (["Signal (%s)" % mass]*(1 if len(signal) > 0 else 0))
					plot_configs[-1]["legend"] = [0.75, 0.6]
					plot_configs[-1]["x_label"] = ""
					plot_configs[-1]["y_label"] = "Events"
					plot_configs[-1]["output_dir"] = os.path.join(mass_output_dir)
					plot_configs[-1]["filename"] = directory + ("_"+fit_type if "postfit" in directory else "")
	
	# plotting
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes)

