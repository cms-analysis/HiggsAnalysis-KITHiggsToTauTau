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
	parser.add_argument("--fit-method", default="logllh",
						choices=["chi2", "logllh"],
						help="Choose a fit (chi2 or logllh)")
	parser.add_argument("--pt-ranges",
						default=["(pt_2 > 20.0)*(pt_2 < 30.0)","(pt_2 > 30.0)*(pt_2 < 45.0)","(pt_2 > 45.0)"],
						help=""	)
	parser.add_argument("--channels", nargs="*",
	                    default=["mt"],
	                    help="Channels. [Default: %(default)s]")
	parser.add_argument("--decay-modes", nargs="+",
						default=["OneProngPiZeros"],
						choices=["OneProng","OneProngPiZeros", "ThreeProng"],
						help="Decay modes of reconstructed hadronic tau leptons in Z #rightarrow #tau#tau. [Default: %(default)s]")
	parser.add_argument("--quantities", nargs="*",
	                    default=["m_2"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("--analysis-modules", default=[], nargs="+",
	                    help="Additional analysis Modules. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="--plot-modules PlotRootHtt",
	                    help="Additional Arguments for HarryPlotter. [Default: %(default)s]")
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
	sample_ztt = [getattr(samples.Samples, "ztt")]
	sample_rest = [getattr(samples.Samples, sample) for sample in args.samples if sample != "ztt" ]

	es_shifts=[shift for shift in args.es_shifts]
	args.decay_modes = [None if decayMode == "None" else decayMode for decayMode in args.decay_modes]

	plot_configs = []
	for channel in args.channels:
		for decayMode in args.decay_modes:
			for quantity in args.quantities:

				name_hash = hashlib.md5("_".join([str(item) for item in [channel, decayMode, quantity]])).hexdigest()

				merged_config={}

				#one config for each pt range
				for index, (pt_range) in enumerate(args.pt_ranges):
					#one ztt nick config for each es shift
					for shift in args.es_shifts:
						config_ztt = sample_settings.get_config(
								samples=sample_ztt,
								channel=channel,
								category="cat" + decayMode + "_" + channel,
								nick_suffix="_" + str(shift).replace(".", "_") + "_" + str(index),
								ztt_from_mc=args.ztt_from_mc,
								weight=pt_range
						)

						config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
						config_ztt["labels"] = ["ztt_" + str(shift).replace(".", "_") + "_" + str(index)]
						config_ztt["stacks"] = [stack.replace("_" + str(shift).replace(".", "_"), "") for stack in config_ztt["stacks"]]
						config_ztt["weights"] = [weight.replace("(pt_2>30.0)","1.0") for weight in config_ztt["weights"]]

						# merge configs
						merged_config = samples.Samples.merge_configs(merged_config, config_ztt, additional_keys=["ztt_emb_inc_nicks","ztt_from_mc","ztt_mc_inc_nicks","ztt_plot_nicks","ztt_nicks"])

				# config for rest for each pt range
				for index, (pt_range) in enumerate(args.pt_ranges):
					config_rest = sample_settings.get_config(
							samples=sample_rest,
							channel=channel,
							category="cat" + decayMode + "_" + channel,
							nick_suffix="_" + str(index),
							weight=pt_range
					)

					config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])
					config_rest["labels"] = [(label + "_" + str(index)) for label in config_rest["labels"]]
					config_rest["weights"] = [weight.replace("(pt_2>30.0)","1.0") for weight in config_rest["weights"]]

					# merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_rest, additional_keys=["wjets_shape_nicks","wjets_data_control_nicks","wjets_data_substract_nicks","wjets_mc_signal_nicks","wjets_mc_control_nicks","qcd_data_shape_nicks","qcd_data_control_nicks","qcd_data_substract_nicks","qcd_extrapolation_factors_ss_os","qcd_subtract_shape"])

				merged_config["directories"] = [args.input_dir]
				merged_config["nicks_blacklist"].append("noplot")
				merged_config["output_dir"] = os.path.expandvars(args.output_dir)
				merged_config["filename"] = decayMode + "_" + name_hash

				# config to plot the fit
				if args.fit_method == "chi2":

					merged_config.setdefault("analysis_modules", []).append("AddHistograms")
					merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

					# ztt plus bkg
					for shift in args.es_shifts:
						bkg_samples_used = ["ztt_" + str(shift).replace(".", "_")] + [nick for nick in bkg_samples if nick in merged_config["nicks"]]
						merged_config.setdefault("histogram_nicks", []).append([" ".join(bkg_samples_used)])
						merged_config.setdefault("sum_result_nicks", []).append(["noplot_ztt_" + str(shift).replace(".", "_")])

					merged_config["res_hist_nick"]  = "chi2_result"
					merged_config["nicks_whitelist"] = ["chi2_result"]
					merged_config["es_shifts"] = [str(shift) for shift in args.es_shifts]
					merged_config["ztt_nicks"] = ["noplot_ztt_" + str(shift).replace(".", "_") for shift in args.es_shifts]
					merged_config["data_nicks"] = ["data"] * len(args.es_shifts)

					config_plotfit = {}

					config_plotfit["files"] = "plots/tauEsStudies_plots/" + decayMode + "_" + name_hash + ".root"
					config_plotfit["markers"] = ["ALP"]
					config_plotfit["x_expressions"]  = ["data"]
					config_plotfit["filename"] = "chi2_" + decayMode + "_" + name_hash
					config_plotfit["x_label"] = "ES_shift"
					config_plotfit["y_label"] = "Chi2"
				elif args.fit_method == "logllh":
					merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

					for index, (pt_range) in enumerate(args.pt_ranges):
						es_shifts_str = [str(shift) for shift in args.es_shifts]
						merged_config.setdefault("es_shifts", []).append([" ".join(es_shifts_str)])
						merged_config.setdefault("data_nicks", []).append("data" + "_" + str(index))
						bkg_samples_used = [(nick + "_" + str(index)) for nick in bkg_samples if (nick + "_" + str(index)) in merged_config["nicks"]]
						merged_config.setdefault("bkg_nicks", []).append([" ".join(bkg_samples_used)])
						ztt_nicks = [("ztt_" + str(shift).replace(".", "_") + "_" + str(index)) for shift in args.es_shifts]
						merged_config.setdefault("ztt_nicks", []).append([" ".join(ztt_nicks)])
						merged_config.setdefault("res_hist_nicks", []).append("logllh_result" + "_" + str(index))
						merged_config["fit_method"] = "logllh"

					config_plotfit = {}

					merged_config["nicks_whitelist"] = ["logllh_result_2"]
					config_plotfit["files"] = "plots/tauEsStudies_plots/" + decayMode + "_" + name_hash + ".root"
					config_plotfit["markers"] = ["E"]
					config_plotfit["texts"] = [decayMode]
					config_plotfit["x_expressions"]  = ["logllh_result_2"]
					config_plotfit["filename"] = "logllh_" + decayMode + "_" + name_hash
					config_plotfit["x_label"] = "p_{T}^{#tau}[GeV]"
					config_plotfit["y_label"] = "#tau-ES-shift"

				#plot modules
				merged_config.setdefault("plot_modules", []).append("ExportRoot")

				#append merged config to plot configs
				plot_configs.append(merged_config)

				#append config for the fit plot
				plot_configs.append(config_plotfit)

	if log.isEnabledFor(logging.DEBUG):
		import pprint
		pprint.pprint(plot_configs)

	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[args.args], n_processes=args.n_processes, n_plots=args.n_plots)
