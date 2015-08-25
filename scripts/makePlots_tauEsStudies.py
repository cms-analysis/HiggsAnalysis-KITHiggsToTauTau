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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run1 as samples


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
	parser.add_argument("--es-shifts", nargs="*",
						default=[0.94,0.95,0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06],
	                    help="Energy scale shifts."),
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=[None],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
	                    default=["m_2"],
	                    help="Quantities. [Default: %(default)s]")
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

	list_of_samples = [getattr(samples.Samples, sample) for sample in args.samples]
	sample_settings = samples.Samples()
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "htt"]

	args.categories = [None if category == "None" else category for category in args.categories]

	sample_ztt = [getattr(samples.Samples, "ztt")]
	sample_rest = [getattr(samples.Samples, sample) for sample in args.samples if sample != "ztt" ]

	es_shifts=[shift for shift in args.es_shifts]

	#0 = OneProng0PiZero
	#1 = OneProng1PiZero
	#2 = OneProng2PiZero
	#10 = ThreeProng0PiZero
	decayModes=["decayMode_2==10","decayMode_2>=1*decayMode_2<=3"]

	plot_configs = []
	for channel in args.channels:
		for decayMode in decayModes:
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

					#merged_config.setdefault("es_shifts", []).append(str(shift))

					config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
					config_ztt["labels"] = [str(decayMode) +"/ztt_" + str(shift).replace(".", "_")]
					config_ztt["stacks"] = [stack.replace("_" + str(shift).replace(".", "_"), "") for stack in config_ztt["stacks"]]

					config_ztt["weights"] = ["eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)*(" + decayMode + ")"] * len(config_ztt["nicks"])

					#print config_ztt["nicks_blacklist"]
					#if (index != 0):
					#	merged_config.setdefault("nicks_blacklist", []).append("^ztt_" + str(shift).replace(".", "_") + "$")

					# merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_ztt, additional_keys=["ztt_emb_inc_nicks","ztt_from_mc","ztt_mc_inc_nicks","ztt_plot_nicks","ztt_nicks"])

				# config for rest
				config_rest = sample_settings.get_config(
						samples=sample_rest,
						channel=channel,
						category=category
				)

				config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])
				config_rest["weights"] = ["eventWeight*((q_1*q_2)<0.0)*(pt_2>30.0)*(lep1MetMt<30.0)*(" + decayMode + ")"]  * len(config_rest["nicks"])

				# merge configs
				merged_config = samples.Samples.merge_configs(merged_config, config_rest)

				merged_config["directories"] = [args.input_dir]
				merged_config["nicks_blacklist"].append("noplot")
				merged_config["output_dir"] = os.path.expandvars(args.output_dir)

				merged_config["filename"] = "tauesstudies_" + decayMode.replace("*","_")

				#data minus background
				bkg_samples_used = ["data"]
				bkg_samples_used = bkg_samples_used + [nick for nick in bkg_samples if nick in merged_config["nicks"]]

				merged_config.setdefault("histogram_nicks", []).extend([" ".join(bkg_samples_used)])
				merged_config.setdefault("sum_scale_factors", []).extend([" ".join(["1" if sample=="data" else "-1" for sample in bkg_samples_used])])
				merged_config.setdefault("sum_result_nicks", []).append("noplot_datanobkg")

				#analysis_modules
				merged_config.setdefault("analysis_modules", []).append("AddHistograms")
				merged_config.setdefault("analysis_modules", []).append("PrintInfos")
				merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

				#plot modules
				merged_config.setdefault("plot_modules", []).append("ExportRoot")
				#merged_config.setdefault("plot_modules", []).append("PlotRootHtt")

				#chi2test
				merged_config["res_hist_nick"]  = ["chi2_result"]
				merged_config["nicks_whitelist"] = ["chi2_result"]
				merged_config["es_shifts"] = [str(shift) for shift in es_shifts]
				merged_config["ztt_nicks"] = ["ztt_" + str(shift).replace(".", "_") for shift in es_shifts]
				merged_config["data_nicks"] = ["noplot_datanobkg"] * len(es_shifts)

				#roofit
			#	merged_config["roofit_flag"] = "false"

				#special
			#	if (index == 0):
			#		merged_config["file_mode"] = "RECREATE"
			#	else:
			#		merged_config["file_mode"] = "UPDATE"

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

				#write a plot config that makes graph
				config_chi2 = {}

				config_chi2["files"] = "plots/tauEsStudies_plots/tauesstudies_" + decayMode.replace("*","_") + ".root"
				config_chi2["markers"] = ["ALP"]
				config_chi2["x_expressions"]  = ["data"]
				config_chi2["filename"] = "chi2result_" + decayMode.replace("*","_")
				config_chi2["x_label"] = "ES_shift"
				config_chi2["y_label"] = "Chi2"

				plot_configs.append(config_chi2)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

