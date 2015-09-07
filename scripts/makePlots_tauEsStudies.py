#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import hashlib

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
						default=[0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06],
	                    help="Energy scale shifts."),
	parser.add_argument("--fit-to-data", default="logllh",
						help="Choose a fit (chi2 or logllh)")
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
	bkg_samples = [sample for sample in args.samples if sample != "data" and sample != "htt" and sample != "qcd"]

	args.categories = [None if category == "None" else category for category in args.categories]

	sample_ztt = [getattr(samples.Samples, "ztt")]
	sample_rest = [getattr(samples.Samples, sample) for sample in args.samples if sample != "ztt" ]

	es_shifts=[shift for shift in args.es_shifts]

	#categories=["OneProngPiZeros", "ThreeProng"]
	categories=["OneProngPiZeros"]

	plot_configs = []
	for channel in args.channels:
		for category in categories:
			for quantity in args.quantities:

				name_hash = hashlib.md5("_".join([str(item) for item in [channel, category, quantity]])).hexdigest()

				merged_config={}

				for index, shift in enumerate(es_shifts):
					# first config for the ztt nick
					config_ztt = sample_settings.get_config(
							samples=sample_ztt,
							channel=channel,
							category="cat" + category + "_" + channel,
							nick_suffix="_" + str(shift).replace(".", "_"),
							ztt_from_mc=args.ztt_from_mc
					)

					config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
					config_ztt["labels"] = ["ztt_" + str(shift).replace(".", "_")]
					config_ztt["stacks"] = [stack.replace("_" + str(shift).replace(".", "_"), "") for stack in config_ztt["stacks"]]

					# merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_ztt, additional_keys=["ztt_emb_inc_nicks","ztt_from_mc","ztt_mc_inc_nicks","ztt_plot_nicks","ztt_nicks"])

				# config for rest
				config_rest = sample_settings.get_config(
						samples=sample_rest,
						channel=channel,
						category="cat" + category + "_" + channel
				)

				config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])

				# merge configs
				merged_config = samples.Samples.merge_configs(merged_config, config_rest)

				merged_config["directories"] = [args.input_dir]
				merged_config["nicks_blacklist"].append("noplot")
				merged_config["output_dir"] = os.path.expandvars(args.output_dir)

				merged_config["filename"] = category + "_" + name_hash

				#analysis_modules
				merged_config.setdefault("analysis_modules", []).append("PrintInfos")

				#plot modules
				merged_config.setdefault("plot_modules", []).append("ExportRoot")
#				merged_config.setdefault("plot_modules", []).append("PlotRootHtt")

				# config to plot the fit
				if args.fit_to_data == "chi2":

					merged_config.setdefault("analysis_modules", []).append("AddHistograms")
					merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

					# ztt plus bkg
					for shift in es_shifts:
						bkg_samples_used = ["ztt_" + str(shift).replace(".", "_")] + [nick for nick in bkg_samples if nick in merged_config["nicks"]]
						merged_config.setdefault("histogram_nicks", []).append([" ".join(bkg_samples_used)])
						merged_config.setdefault("sum_result_nicks", []).append(["noplot_ztt_" + str(shift).replace(".", "_")])

					merged_config["res_hist_nick"]  = "chi2_result"
					merged_config["nicks_whitelist"] = ["chi2_result"]
					merged_config["es_shifts"] = [str(shift) for shift in es_shifts]
					merged_config["ztt_nicks"] = ["noplot_ztt_" + str(shift).replace(".", "_") for shift in es_shifts]
					merged_config["data_nicks"] = ["data"] * len(es_shifts)

					config_plotfit = {}

					config_plotfit["files"] = "plots/tauEsStudies_plots/" + category + "_" + name_hash + ".root"
					config_plotfit["markers"] = ["ALP"]
					config_plotfit["x_expressions"]  = ["data"]
					config_plotfit["filename"] = "chi2_" + category + "_" + name_hash
					config_plotfit["x_label"] = "ES_shift"
					config_plotfit["y_label"] = "Chi2"
				elif args.fit_to_data == "logllh":
					merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

					merged_config["roofit_flag"] = "true"
					merged_config["res_hist_nick"]  = "logllh_result"
					merged_config["nicks_whitelist"] = ["logllh_result"]
					merged_config["es_shifts"] = [str(shift) for shift in es_shifts]
					merged_config["ztt_nicks"] = ["ztt_" + str(shift).replace(".", "_") for shift in es_shifts]
					merged_config["data_nicks"] = ["data"] * len(es_shifts)
					for shift in es_shifts:
						bkg_samples_used = [nick for nick in bkg_samples if nick in merged_config["nicks"]]
						merged_config.setdefault("bkg_nicks", []).append([" ".join(bkg_samples_used)])

					config_plotfit = {}

					config_plotfit["files"] = "plots/tauEsStudies_plots/" + category + "_" + name_hash + ".root"
					config_plotfit["markers"] = ["ALP"]
					config_plotfit["x_expressions"]  = ["data"]
					config_plotfit["filename"] = "logllh_" + category + "_" + name_hash
					config_plotfit["x_label"] = "ES_shift"
					config_plotfit["y_label"] = "-log(L)"
				else:
					print "fit not found"

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

				# append config for the fit plot
				plot_configs.append(config_plotfit)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)

