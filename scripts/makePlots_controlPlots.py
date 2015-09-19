#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os

import Artus.Utility.jsonTools as jsonTools

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zl", "zj", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zll", "zl", "zj", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh", "htt", "data"], 
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")
	parser.add_argument("-c", "--channels", nargs="*",
	                    default=["tt", "mt", "et", "em", "mm", "ee"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("-x", "--quantities", nargs="*",
	                    default=["inclusive",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2",
	                             "pt_ll", "eta_ll", "phi_ll", "m_ll", "mt_ll",
	                             "pt_llmet", "eta_llmet", "phi_llmet", "m_llmet", "mt_llmet",
	                             "mt_lep1met",
	                             "pt_sv", "eta_sv", "phi_sv", "m_sv",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njets", "mjj", "jdeta",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("--run2", default=False, action="store_true",
	                    help="Use Run2 samples. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+", default=[],
	                    help="Exclude (default) selection cuts. [Default: %(default)s]")
	parser.add_argument("-m", "--higgs-masses", nargs="+", default=["125"],
	                    help="Higgs masses. [Default: %(default)s]")
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
	                    default="$CMSSW_BASE/src/plots/control_plots/",
	                    help="Output directory. [Default: %(default)s]")
	parser.add_argument("--www", nargs="?", default=None, const="",
	                    help="Publish plots. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	if not args.run2:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples
	else:
		import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples
	
	if args.samples == parser.get_default("samples"):
		args.samples = [sample for sample in args.samples if hasattr(samples.Samples, sample)]
	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "htt"]

	args.categories = [None if category == "None" else category for category in args.categories]

	plot_configs = []
	for channel in args.channels:
		for category in args.categories:
			for quantity in args.quantities:
			
				config = sample_settings.get_config(
						samples=list_of_samples,
						channel=channel,
						category=category,
						higgs_masses=args.higgs_masses,
						normalise_signal_to_one_pb=False,
						ztt_from_mc=args.ztt_from_mc,
						weight=args.weight,
						exclude_cuts=args.exclude_cuts+(["mt"] if quantity == "mt_1" else [])
				)
				
				config["x_expressions"] = quantity
				config["x_bins"] = [channel+"_"+quantity]
				config["x_label"] = channel+"_"+quantity
				
				config["directories"] = [args.input_dir]
				
				for analysis_module in args.analysis_modules:
					if not analysis_module in config.get("analysis_modules", []):
						config.setdefault("analysis_modules", []).append(analysis_module)
				
				if log.isEnabledFor(logging.DEBUG) and (not "PrintInfos" in config.get("analysis_modules", [])):
					config.setdefault("analysis_modules", []).append("PrintInfos")

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

				config["output_dir"] = os.path.expandvars(os.path.join(
						args.output_dir,
						channel if len(args.channels) > 1 else "",
						category if len(args.categories) > 1 else ""
				))
				if not args.www is None:
					config["www"] = os.path.expandvars(os.path.join(
							args.www,
							channel if len(args.channels) > 1 else "",
							category if len(args.categories) > 1 else ""
					))
				plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

