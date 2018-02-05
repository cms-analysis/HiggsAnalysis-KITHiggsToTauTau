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
			config = {}
			for mode in ['MC', 'data']:
				if not "FunctionFit" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("FunctionFit")
				#config["analysis_modules"] = ["FunctionFit"]
				config["directories"] = [args.input_dir]		
				config["folders"] = [channel+"_"+probe_trigger+"/"+channel+"TriggerTP"]
				if mode == 'MC':
					config["files"] = ["DYJetsToLLM50_RunIISpring15DR74_Asympt25ns_13TeV_MINIAOD_amcatnloFXFX-pythia8/*.root"]
				if mode == 'data':
					config["files"] = ["*_Run2015B_PromptRecov1_13TeV_MINIAOD/*.root"]
				for eta_range in ['barrel', 'endcap']:
					for pt_bins in ['pt_10_15', 'pt_15_20', 'pt_20_30', 'pt_30_40', 'pt_40_60']:
						for probe_type in ['passing', 'failing']:
							config["x_expressions"] = ["tagProbeSystem.fCoordinates.fM"]
							config["x_bins"] = ["40,50,130"]
							config["function_fit"] = ["nick0"]
							config["functions"] = ["(x>[0])*[1]*exp(-0.5*((x-[0])/[2])**2)+(x<[0])*[1]*exp(-0.5*((x-[0])/[3])**2)+[4]*exp([5]*x)"]
							config["function_parameters"] = ["91,1,3,3,308,-0.04"]
							if pt_bins == 'pt_10_15':
								if probe_type == 'passing':
									config["weights"] = ["(probe.p4.Pt()>30)*(probe.p4.Pt()<40)*(probeMatched)"]
									config["plot_modules"] = ["ExportRoot"]					
									config["labels"] = [mode+"/"+eta_range+"/"+pt_bins+"/"+probe_type+"_probes"+"/"+"Histogram",
											    mode+"/"+eta_range+"/"+pt_bins+"/"+probe_type+"_probes"+"/"+"Function"]
									config["filename"] = mode+"_"+eta_range+"_"+pt_bins+"_"+"passing"+"_probes"
									config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, probe_trigger))
									if not args.www is None:
										config["www"] = os.path.expandvars(os.path.join(args.www, channel, probe_trigger))
									tmp = config.copy()	
									plot_configs.append(tmp)
								if probe_type == 'failing':
									config["weights"] = ["(probe.p4.Pt()>30)*(probe.p4.Pt()<40)*(1-probeMatched)"]
									config["plot_modules"] = ["ExportRoot"]						
									config["labels"] = [mode+"/"+eta_range+"/"+pt_bins+"/"+probe_type+"_probes"+"/"+"Histogram",
											    mode+"/"+eta_range+"/"+pt_bins+"/"+probe_type+"_probes"+"/"+"Function"]
									config["filename"] = mode+"_"+eta_range+"_"+pt_bins+"_"+"failing"+"_probes"
									config["output_dir"] = os.path.expandvars(os.path.join(args.output_dir, channel, probe_trigger))
									if not args.www is None:
										config["www"] = os.path.expandvars(os.path.join(args.www, channel, probe_trigger))	
									tmp = config.copy()
									plot_configs.append(tmp)


				

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

