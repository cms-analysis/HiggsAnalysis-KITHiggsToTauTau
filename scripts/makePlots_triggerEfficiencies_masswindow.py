#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import itertools
import os

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015 as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make trigger efficiency plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["zll", "data"],
	                    choices=["zll", "data"], 
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", action="append", required=True,
	                    choices=["mm", "ee", "mt", "et"],
	                    help="Channels.")
	parser.add_argument("-p", "--probe-triggers", nargs="+", action="append", required=True,
	                    help="Probe triggers per channel.")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")	
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
	parser.add_argument("-r", "--ratio", default=False, action="store_true",
	                    help="Add ratio subplot. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
	                    help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-f", "--n-plots", type=int,
	                    help="Number of plots. [Default: all]")
	parser.add_argument("-o", "--output-dir",
	                    default="$CMSSW_BASE/src/plots/trigger_efficiencyfits/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="trigger_efficiencyfits",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	offline_selections = "tagMatched*puWeight*(tagIsoOverPt<0.1)*(tagCharge != probeCharge)*(std::abs(tagProbeMass - 91)<5)"
	# sensible eta_regions differ for electrons and muons.for muons stick to michal's, electrons only in abs(eta)><1.48
	eta_weights_mm = ["*(std::abs(probeEta)<0.9)","*(std::abs(probeEta)>0.9)*(std::abs(probeEta)<1.2)","*(std::abs(probeEta)>1.2)"]
	eta_weights_ee = ["*(std::abs(probeEta)<1.48)","*(std::abs(probeEta)>1.48)"]

	plot_configs = []
	for channel, probe_triggers in zip(args.channels, args.probe_triggers):
		for probe_trigger in probe_triggers:
			for eta_range in range(3):
				if channel == "ee" and eta_range == 2:
					break	
				config = {}
				if not "Efficiency" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("Efficiency")
				config["directories"] = [args.input_dir]
				config["folders"] = [channel+"_"+probe_trigger+"/"+"ntuple"]
				if channel == "mm":
					config["files"] = [
					"DYJetsToLLM50_RunIISpring15MiniAODv2_74X_13TeV_MINIAOD_madgraph-pythia8/*.root",
					"DYJetsToLLM50_RunIISpring15MiniAODv2_74X_13TeV_MINIAOD_madgraph-pythia8/*.root",
					"SingleMuon_*/*.root",
					"SingleMuon_*/*.root"]
				if channel == "ee":
					config["files"] = [
					"DYJetsToLLM50_RunIISpring15MiniAODv2_74X_13TeV_MINIAOD_madgraph-pythia8/*.root",
					"DYJetsToLLM50_RunIISpring15MiniAODv2_74X_13TeV_MINIAOD_madgraph-pythia8/*.root",
					"SingleElectron_*/*.root",
					"SingleElectron_*/*.root"]
				config["nicks"] = [
					"noplot_mc_all",
					"noplot_mc_pass",
					"noplot_data_all",
					"noplot_data_pass"
				]
				config.setdefault("efficiency_numerator_nicks", []).append([nick for nick in config["nicks"] if "pass" in nick])
				config.setdefault("efficiency_denominator_nicks", []).append([nick for nick in config["nicks"] if "all" in nick])
				config.setdefault("efficiency_nicks", []).append(["mc", "data"])
				config.setdefault("efficiency_methods", []).append(["cp"] * 2)
				config["x_expressions"] = ["probePt"]
				#config["x_bins"] = ["40,0,100"]
				#config["x_bins"] = ["0 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 27 29 31 33 35 40 45 50 55 60 65 70 80 90 100"]
				#DESYbinning
				config["x_bins"] = ["0 10 13 16 19 22 25 28 31 34 37 40 45 50 60 70 100"]
				if channel == "ee":
					config["weights"] = [offline_selections+eta_weights_ee[eta_range],
					offline_selections+eta_weights_ee[eta_range]+"*(probeMatched)",
					offline_selections+eta_weights_ee[eta_range],
					offline_selections+eta_weights_ee[eta_range]+"*(probeMatched)"
					]
				if channel == "mm":
					config["weights"] = [offline_selections+eta_weights_mm[eta_range],
					offline_selections+eta_weights_mm[eta_range]+"*(probeMatched)",
					offline_selections+eta_weights_mm[eta_range],
					offline_selections+eta_weights_mm[eta_range]+"*(probeMatched)"
					]
				config["markers"] = ["ELP", "ELP"]
				config["colors"] = ["#FF0000","#000000"]
				config["y_lims"] = [0.0, 1.2]
				config["legend"] = [0.2, 0.75, 0.4, 0.95]
				config["legend_markers"] = ["ELP"]
				config["y_label"] = "Efficiency"
				config["x_label"] = "probe p_{T} / GeV"
				config["plot_modules"] = ["ExportRoot"]
				config["labels"] = ["Simulation",
						    "Data",
						    "Ratio"]
				config["title"] = "eta_region"+str(eta_range)
				config["filename"] = channel+"_"+probe_trigger+"_"+"eta_region"+str(eta_range)
				if args.ratio:
					if not "Ratio" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
						config.setdefault("analysis_modules", []).append("PrintInfos")
					config.setdefault("ratio_numerator_nicks", []).append("data")
					config.setdefault("ratio_denominator_nicks", []).append("mc")
					config.setdefault("colors", []).append("#000000")
					config.setdefault("markers", []).append("Line")
					config.setdefault("labels", []).append("")
					config["y_subplot_label"] = "Data/MC"
					config["y_subplot_lims"] = [0.75, 1.25]

				config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, probe_trigger))
				if not args.www is None:
					config["www"] = os.path.expandvars(os.path.join(args.www, channel, probe_trigger))
				tmp = config.copy()	
				plot_configs.append(tmp)
				

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		#pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

