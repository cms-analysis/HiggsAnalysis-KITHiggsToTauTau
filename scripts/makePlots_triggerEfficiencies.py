#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import itertools
import os

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
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
	                    default="$CMSSW_BASE/src/plots/trigger_efficiencies/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="trigger_efficiencies",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	"""
	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]
	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	"""

	plot_configs = []
	for channel, probe_triggers in zip(args.channels, args.probe_triggers):
		for probe_trigger in probe_triggers:
			for plot_mode in ['pt', 'eta']:#, 'combinedMC','combinedData','DataMC']:
		
				"""
				config = sample_settings.get_config(
						samples=list_of_samples,
						channel=channel,
						category=category,
						higgs_masses=args.higgs_masses,
						normalise_signal_to_one_pb=False,
						ztt_from_mc=args.ztt_from_mc,
						weight=args.weight
				)
				"""
				config = {}
				config["directories"] = [args.input_dir]
				
		
				config["folders"] = [channel+"_"+probe_trigger+"/"+"ntuple"]
		
				offline_selections = "(probeCharge != tagCharge)*(tagIsoOverPt<0.1)*(tagPt>20)*(probePt>15)*(puWeight)*"
				eta_range = "(std::abs(probeEta)<2.1)*"
				
				#config["weights"] = ["tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)" if channel in ["mm", "ee"] else "tagMatched"]
				config["weights"] = offline_selections+eta_range+"tagMatched * (std::abs(tagProbeMass - 91.0) < 5)"				

				if plot_mode in ['pt','eta']:
					config["files"] = [
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
					"SingleMuon_Run2015D_PromptRecov4_13TeV_MINIAOD/*.root",
					"SingleMuon_Run2015D_PromptRecov4_13TeV_MINIAOD/*.root",
					"SingleMuon_Run2015D_05Oct2015v1_13TeV_MINIAOD/*.root",
					"SingleMuon_Run2015D_05Oct2015v1_13TeV_MINIAOD/*.root"
					]
					if plot_mode == 'pt':
						config["x_expressions"] = ["probePt"]
						config["x_bins"] = ["0 10 20 30 40 50 60 70 80 100 120 140 170 200"]#["40,0,200"]
					if plot_mode == 'eta':
						config["x_expressions"] = ["probeEta"]
						config["x_bins"] = ["40,-2,2"]
					#config["files"] = list(itertools.chain(*[[input_file] * 2 for input_file in config["files"]]))
					config["weights"] = [weight if index % 2 == 0 else (weight + " * probeMatched") for index, weight in enumerate(config["weights"] * 6)]
					config["nicks"] = [
						"noplot_mc_all",
						"noplot_mc_pass",
						"noplot_data_all",
						"noplot_data_pass",
						"noplot_data_all",
						"noplot_data_pass"
					]
					
					if not "Efficiency" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Efficiency")
					config.setdefault("efficiency_numerator_nicks", []).append([nick for nick in config["nicks"] if "pass" in nick])
					config.setdefault("efficiency_denominator_nicks", []).append([nick for nick in config["nicks"] if "all" in nick])
					config.setdefault("efficiency_nicks", []).append(["mc", "data"])
					config.setdefault("efficiency_methods", []).append(["cp"] * 2)
					
					config["markers"] = ["P", "P"]
		
					config["labels"] = ["MC", "Data"]
					config["colors"] = ["#FF0000", "#000000"]
					config["y_lims"] = [0.0, 1.2]
					config["legend"] = [0.2, 0.75, 0.4, 0.95]
					config["legend_markers"] = ["ELP"]
		
					
					config["y_label"] = "Efficiency"
					if plot_mode == 'pt':
						config["x_label"] = "probe p_{T} / GeV"
						config["filename"] = "efficiency_vs_pt"
					if plot_mode == 'eta':
						config["x_label"] = "probe eta"
						config["filename"] = "efficiency_vs_eta"

				
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

				'''
				if plot_mode in ['combinedMC','combinedData','DataMC']:
					if not "Divide" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Divide")
					config["x_expressions"] = ["probe.p4.Eta()"]
					config["x_bins"] = ["8,-2.1,2.1"]
					config["x_label"] = "probe eta"
					config["y_expressions"] = ["probe.p4.Pt()"]
					config["y_bins"] = ["0 10 20 30 40 50 60 70 80 100 200"]
					config["y_label"] = "probe p_{T} /GeV"
					#config["legend"] = [0.2, 0.85, 0.3, 0.95]
					config["markers"] = "colz"

					if plot_mode == 'combinedMC':
						config["weights"] = [
						"tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)", 
					        "tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30) * probeMatched"
						]
						config["files"] = [
						"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
						"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
						]
						config["nicks"] = ["noplot_mc_all", "noplot_mc_pass"]
						config["divide_denominator_nicks"] = "noplot_mc_all"
						config["divide_numerator_nicks"] = "noplot_mc_pass"
						config["divide_result_nicks"] = "mc"
						config["labels"] = ["MC",""]
						config["title"] = "MC Efficiency"
						config["z_lims"] = [0.0,1.0]
						config["z_label"] = "Efficiency"
						config["filename"] = "efficiency2d_MC"
					if plot_mode == 'combinedData':
						config["weights"] = [
						"tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)", 
					        "tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30) * probeMatched"
						]
						config["files"] = [
						"*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
						"*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root"
						]
						config["nicks"] = ["noplot_data_all", "noplot_data_pass"]
						config["divide_denominator_nicks"] = "noplot_data_all"
						config["divide_numerator_nicks"] = "noplot_data_pass"
						config["divide_result_nicks"] = "data"
						config["labels"] = ["Data",""]
						config["title"] = "Data Efficiency"
						config["z_lims"] = [0.0,1.0]
						config["z_label"] = "Efficiency"
						config["filename"] = "efficiency2d_data"
					if plot_mode == 'DataMC':
						config["weights"] = [
						"tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)", 
					        "tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30) * probeMatched",
						"tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)", 
					        "tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30) * probeMatched"
						]
						config["files"] = [
						"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
						"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
						"*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
						"*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root"
						]
						config["nicks"] = ["noplot_mc_all", "noplot_mc_pass", "noplot_data_all", "noplot_data_pass"]
						config["divide_denominator_nicks"] = ["noplot_mc_all", "noplot_data_all", "noplot_mc"]
						config["divide_numerator_nicks"] = ["noplot_mc_pass", "noplot_data_pass", "noplot_data"]
						config["divide_result_nicks"] = ["noplot_mc", "noplot_data", "datamc"]
		
						#config["labels"] = ["Data / MC",""]
						config["title"] = "Data / MC"
						config["z_label"] = ""
						config["colors"] = "kBlue kWhite kRed"
						config["colormap"] = "True"
						config["z_lims"] = [0.7, 1.3]
						config["filename"] = "efficiency2d_databymc"
				'''

				config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, probe_trigger))
				if not args.www is None:
					config["www"] = os.path.expandvars(os.path.join(args.www, channel, probe_trigger))
		
				plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

