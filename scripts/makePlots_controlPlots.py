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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zl", "zj", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zl", "zj", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh", "htt", "data"], 
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--channels", nargs="*",
	                    default=["tt", "mt", "et", "em", "mm", "ee"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
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
	parser.add_argument("-w", "--weight", default="1.0",
	                    help="Additional weight (cut) expression. [Default: %(default)s]")
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
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	list_of_samples = [getattr(samples.Sample, sample) for sample in args.samples]
	sample_settings = samples.Sample()
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
						normalise_signal_to_one_pb=False
				)

				# handle possible JSON files
				json_exists = True
				json_config_file = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/{channel}_{quantity}.json".format(channel=channel, quantity=quantity))

				if not os.path.exists(json_config_file):
					json_exists = False
					json_config_file =  os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/control_plots/{channel}_default.json".format(channel=channel))

				json_config = jsonTools.JsonDict(json_config_file).doIncludes().doComments()
				config = copy.deepcopy(json_config) + config

				config["directories"] = [args.input_dir]

				if not json_exists:
					config["x_expressions"] = quantity
				
				if args.weight != parser.get_default("weight"):
					if "weights" in config:
						newWeights = []
						for weight in config["weights"]:
							newWeights.append(weight + '*' + args.weight)
						config["weights"] = newWeights
					else:
						config["weights"] = args.weight

				if args.ratio:
					config.setdefault("analysis_modules", []).append("Ratio")
					config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples), "data"])
					config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples)] * 2)
					config.setdefault("colors", []).extend(["#000000"] * 2)
					config.setdefault("markers", []).extend(["E2", "E"])
					config.setdefault("legend_markers", []).extend(["ELP"]*2)
					config.setdefault("labels", []).extend([""] * 2)	

				plot_configs.append(config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

