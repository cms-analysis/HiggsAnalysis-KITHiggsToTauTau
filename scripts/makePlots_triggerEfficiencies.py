#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
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
				"*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root"
			]
		
			config["folders"] = [channel+"_"+probe_trigger+"/"+channel+"TriggerTP"]
		
			config["x_expressions"] = ["probe.p4.Pt()"]
			config["y_expressions"] = ["probeMatched"]
			config["weights"] = ["tagMatched * (std::abs(tagProbeSystem.mass() - 90.0) < 30)"]
		
			config["x_bins"] = ["40,0,200"]
		
			config["tree_draw_options"] = ["prof"]
		
			config["markers"] = ["E"]
			config["labels"] = ["MC", "Data"]
			config["legend"] = [0.5, 0.2, 0.9, 0.4]
			config["legend_markers"] = ["ELP"]
		
			config["x_label"] = "probe p_{T} / GeV"
			config["y_label"] = "efficiency"
		
			"""
			if args.ratio:
				bkg_samples_used = [nick for nick in bkg_samples if nick in config["nicks"]]
				if not "Ratio" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("Ratio")
				config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples_used), "data"])
				config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples_used)] * 2)
				config.setdefault("colors", []).extend(["#000000"] * 2)
				config.setdefault("markers", []).extend(["E2", "E"])
				config.setdefault("legend_markers", []).extend(["ELP"]*2)
				config.setdefault("labels", []).extend([""] * 2)
			"""

			config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, probe_trigger))
			if not args.www is None:
				config["www"] = os.path.expandvars(os.path.join(args.www, channel, probe_trigger))
			config["filename"] = "efficiency_vs_pt_prof"
		
			plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

