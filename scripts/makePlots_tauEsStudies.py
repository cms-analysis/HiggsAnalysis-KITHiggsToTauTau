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
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")  
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"],
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
	                    default="$CMSSW_BASE/src/plots/tauEsStudies_plots/",
	                    help="Output directory. [Default: %(default)s]")
	
	args = parser.parse_args()
	logger.initLogger(args)
	
	list_of_samples = [getattr(samples.Sample, sample) for sample in args.samples]
	sample_settings = samples.Sample()
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "htt"]

	args.categories = [None if category == "None" else category for category in args.categories]
			
	sample_ztt = [getattr(samples.Sample, "ztt")]
	sample_rest = [getattr(samples.Sample, sample) for sample in args.samples if sample != "ztt" ]
	
#	es_shifts=[0.94,0.95,0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06]
	es_shifts=[1.01]
	
	plot_configs = []
	for channel in args.channels:
		for quantity in args.quantities:

			merged_config={}

			for index, shift in enumerate(es_shifts):
				# first config for the ztt nick
				config_ztt = sample_settings.get_config(
						samples=sample_ztt,
						channel=channel,
						category=category,
						nick_suffix="_" + str(shift).replace(".", "_"),
						ztt_from_mc=args.ztt_from_mc
				)

				config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
				config_ztt["labels"] = ["text/ztt_" + str(shift).replace(".", "_")]
				config_ztt["stacks"] = [stack.replace("_" + str(shift).replace(".", "_"), "") for stack in config_ztt["stacks"]]
				#config_ztt["weights"] =

			#	print config_ztt["nicks_blacklist"]
			#	if (index != 0):
			#		config_ztt.setdefault("nicks_blacklist", []).append("ztt_" + str(shift).replace(".", "_"))

				# merge configs
				merged_config = samples.Sample.merge_configs(merged_config, config_ztt, additional_keys=["ztt_emb_inc_nicks","ztt_from_mc","ztt_mc_inc_nicks","ztt_plot_nicks","nicks_blacklist",""])

			# config for rest
			config_rest = sample_settings.get_config(
					samples=sample_rest,
					channel=channel,
					category=category
			)

			#config_rest["x_expressions"] = [quantity] * len([nick for nick in config_rest["nicks"] if not "noplot" in nick])
			config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])
			#config_rest["stacks"] = ["bkg" if nick != "data" else "data" for nick in config_rest["nicks"] if not "noplot" in nick]

			# merge configs
			merged_config = samples.Sample.merge_configs(merged_config, config_rest)

			#merged_config["legend_markers"] = ["F" if label != "data" else "ELP" for label in merged_config["labels"]]
			merged_config["directories"] = [args.input_dir]
			merged_config["nicks_blacklist"].append("noplot")
			merged_config["output_dir"] = os.path.expandvars(args.output_dir)
			merged_config["filename"] = "m_2_shift" + str(shift)

			bkg_samples_used = ["ztt_" + str(shift).replace(".", "_")]
			bkg_samples_used = bkg_samples_used + [nick for nick in bkg_samples if nick in merged_config["nicks"]]

			merged_config.setdefault("histogram_nicks", []).extend([" ".join(bkg_samples_used)])
			merged_config.setdefault("sum_result_nicks", []).append("noplot_sum")
			merged_config.setdefault("chi2test_nicks", []).append("noplot_sum data")

			#analysis_modules
			merged_config.setdefault("analysis_modules", []).append("AddHistograms")
			merged_config.setdefault("analysis_modules", []).append("PrintInfos")
			merged_config.setdefault("analysis_modules", []).append("Chi2Test")

			if args.ratio:
				bkg_samples_used = ["ztt_" + str(shift).replace(".", "_")]
				bkg_samples_used = bkg_samples_used + [nick for nick in bkg_samples if nick in merged_config["nicks"]]
				merged_config.setdefault("analysis_modules", []).append("Ratio")
				merged_config.setdefault("ratio_numerator_nicks", []).extend([" ".join(bkg_samples_used), "data"])
				merged_config.setdefault("ratio_denominator_nicks", []).extend([" ".join(bkg_samples_used)] * 2)
				merged_config.setdefault("colors", []).extend(["#000000"] * 2)
				merged_config.setdefault("markers", []).extend(["E2", "E"])
				merged_config.setdefault("legend_markers", []).extend(["ELP"]*2)
				merged_config.setdefault("labels", []).extend([""] * 2)

			# append merged config to plot configs
			plot_configs.append(merged_config)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)
			
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

