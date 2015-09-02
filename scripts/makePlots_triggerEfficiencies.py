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
			for efficiency_mode in [True, False]:
		
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
				config["files"] = [
					"DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root",
					"*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root",
				]
		
				config["folders"] = [channel+"_"+probe_trigger+"/"+channel+"TriggerTP"]
		
				config["x_expressions"] = ["probe.p4.Pt()"]
				config["x_bins"] = ["40,0,200"]
				
				config["weights"] = ["tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)" if channel in ["mm", "ee"] else "tagMatched"]
				
				if efficiency_mode:
					config["files"] = list(itertools.chain(*[[input_file] * 2 for input_file in config["files"]]))
					config["weights"] = [weight if index % 2 == 0 else (weight + " * probeMatched") for index, weight in enumerate(config["weights"] * 4)]
					config["nicks"] = [
						"noplot_mc_all",
						"noplot_mc_pass",
						"noplot_data_all",
						"noplot_data_pass",
					]
					
					if not "Efficiency" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Efficiency")
					config.setdefault("efficiency_numerator_nicks", []).append([nick for nick in config["nicks"] if "pass" in nick])
					config.setdefault("efficiency_denominator_nicks", []).append([nick for nick in config["nicks"] if "all" in nick])
					config.setdefault("efficiency_nicks", []).append(["mc", "data"])
					config.setdefault("efficiency_methods", []).append(["cp"] * 2)
					
					config["markers"] = ["P", "P"]
					config["filename"] = "efficiency_vs_pt_cp"
				else:
					config["nicks"] = ["mc", "data"]
					
					config["y_expressions"] = ["probeMatched"]
					config["tree_draw_options"] = ["prof"]
					
					config["markers"] = ["E", "E"]
					config["filename"] = "efficiency_vs_pt_prof"
		
				config["labels"] = ["MC", "Data"]
				config["colors"] = ["#FF0000", "#000000"]
				config["legend"] = [0.5, 0.2, 0.9, 0.4]
				config["legend_markers"] = ["ELP"]
		
				config["x_label"] = "probe p_{T} / GeV"
				config["y_label"] = "efficiency"
				
				if args.ratio:
					if not "Ratio" in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).append("data")
					config.setdefault("ratio_denominator_nicks", []).append("mc")
					config.setdefault("colors", []).append("#000000")
					config.setdefault("markers", []).append("E")
					config.setdefault("labels", []).append("")
					config["y_subplot_label"] = "Data/MC"
					config["y_subplot_lims"] = [0.75, 1.25]

				config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, probe_trigger))
				if not args.www is None:
					config["www"] = os.path.expandvars(os.path.join(args.www, channel, probe_trigger))
		
				plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

