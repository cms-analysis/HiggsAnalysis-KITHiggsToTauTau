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
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2 as samples


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make Data-MC control plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("-i", "--input-dir", required=True,
	                    help="Input directory.")
	parser.add_argument("-s", "--samples", nargs="+",
	                    default=["ztt", "zll", "ttj", "vv", "wj", "qcd", "data"],
	                    choices=["ztt", "zll", "ttj", "vv", "wj", "qcd", "ggh", "qqh", "vh", "htt", "data"],
	                    help="Samples. [Default: %(default)s]")
	parser.add_argument("--lumi", type=float, default=2.301,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--ztt-from-mc", default=False, action="store_true",
	                    help="Use MC simulation to estimate ZTT. [Default: %(default)s]")
	parser.add_argument("--es-shifts", nargs="*",
		     default=[0.96,0.97,0.98,0.99,1.0,1.01,1.02,1.03,1.04,1.05,1.06],
			    #default=[0.960,0.961,0.962,0.963,0.964,0.965,0.966,0.967,0.968,0.969,
	                             #0.970,0.971,0.972,0.973,0.974,0.975,0.976,0.977,0.978,0.979,
	                             #0.980,0.981,0.982,0.983,0.984,0.985,0.986,0.987,0.988,0.989,
	                             #0.990,0.991,0.992,0.993,0.994,0.995,0.996,0.997,0.998,0.999,
	                             #1.000,1.001,1.002,1.003,1.004,1.005,1.006,1.007,1.008,1.009,
	                             #1.010,1.011,1.012,1.013,1.014,1.015,1.016,1.017,1.018,1.019,
	                             #1.020,1.021,1.022,1.023,1.024,1.025,1.026,1.027,1.028,1.029,
	                             #1.030,1.031,1.032,1.033,1.034,1.035,1.036,1.037,1.038,1.039,
	                             #1.040,1.041,1.042,1.043,1.044,1.045,1.046,1.047,1.048,1.049,
	                             #1.050,1.051,1.052,1.053,1.054,1.055,1.056,1.057,1.058,1.059,1.060],
	                    help="Energy scale shifts."),
	parser.add_argument("--fit-method", default="logllh",
						choices=["chi2", "logllh"],
						help="Choose a fit (chi2 or logllh)")
	parser.add_argument("--pt-ranges",
						default=["1.0"],
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
	parser.add_argument("--plot-es-shifts", default=False, action="store_true",
						help="Plot quantity for every energy scale shift.")

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
				
				ztt_configs = []
				rest_config = {}
				
				# config for rest for each pt range
				# need to get "rest" first in order for corrections of negative bin contents to have an effect
				for index, (pt_range) in enumerate(args.pt_ranges):
					config_rest = sample_settings.get_config(
							samples=sample_rest,
							channel=channel,
							category="cat" + decayMode + "_" + channel,
							nick_suffix="_" + str(index),
							weight=pt_range,
							lumi=args.lumi * 1000
					)
                
					config_rest["x_expressions"] = [quantity] * len(config_rest["nicks"])
					config_rest["labels"] = [(label + "_" + str(index)) for label in config_rest["labels"]]
					config_rest["weights"] = [weight.replace("(pt_2>30.0)","1.0") for weight in config_rest["weights"]]
                
					# merge configs
					merged_config = samples.Samples.merge_configs(merged_config, config_rest)
					rest_config = samples.Samples.merge_configs(rest_config, config_rest)

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
								weight=pt_range,
								lumi=args.lumi * 1000
						)

						if decayMode == "OneProng" and quantity == "m_2":
							log.error("Tau mass (m_2) fit not possible in 1prong decay mode")
						if quantity == "m_2":
							config_ztt["x_expressions"] = [quantity + "*" + str(shift)] * len(config_ztt["nicks"])
						elif quantity == "m_vis":
							config_ztt["x_expressions"] = [quantity + "*sqrt(" + str(shift) + ")"] * len(config_ztt["nicks"])
						config_ztt["labels"] = ["ztt_" + str(shift).replace(".", "_") + "_" + str(index)]
						config_ztt["stacks"] = [stack.replace("_" + str(shift).replace(".", "_"), "") for stack in config_ztt["stacks"]]
						config_ztt["weights"] = [weight.replace("(pt_2>30.0)","1.0") for weight in config_ztt["weights"]]
						
						if args.plot_es_shifts:
							shift_config = {}
							shift_config = samples.Samples.merge_configs(shift_config,copy.deepcopy(config_ztt), additional_keys=["ztt_emb_inc_nicks","ztt_from_mc","ztt_mc_inc_nicks","ztt_plot_nicks","ztt_nicks"])
							
							ztt_configs.append(shift_config)

						# merge configs
						merged_config = samples.Samples.merge_configs(merged_config, config_ztt, additional_keys=["ztt_emb_inc_nicks","ztt_from_mc","ztt_mc_inc_nicks","ztt_plot_nicks","ztt_nicks"])
				
				# plot given quantity for every given energy scale shift
				if args.plot_es_shifts:
					for index, shift in enumerate(args.es_shifts):
						shift_config = {}
						shift_config = samples.Samples.merge_configs(shift_config,ztt_configs[index])
						shift_config = samples.Samples.merge_configs(shift_config,rest_config)
						
						all_samples = [nick for nick in shift_config["nicks"] if not "noplot" in nick]
						all_bkgs = [nick for nick in all_samples if not "data" in nick]
						all_data = [nick for nick in all_samples if "data" in nick]
						
						# execute bin correction modules after possible background estimation modules
						shift_config["analysis_modules"].sort(key=lambda module: module in ["BinErrorsOfEmptyBins", "CorrectNegativeBinContents"])
						shift_config["nicks_correct_negative_bins"] = all_bkgs
						shift_config["nicks_empty_bins"] = all_bkgs
						
						shift_config["labels"] = [sample for sample in args.samples]
						
						# ratio
						shift_config.setdefault("analysis_modules", []).append("Ratio")
						shift_config.setdefault("ratio_numerator_nicks", []).extend([" ".join(all_bkgs), " ".join(all_data)])
						shift_config.setdefault("ratio_denominator_nicks", []).extend([" ".join(all_bkgs)] * 2)
						shift_config.setdefault("colors", []).extend(["#000000"] * 2)
						shift_config.setdefault("markers", []).extend(["E2", "E"])
						shift_config.setdefault("legend_markers", []).extend(["ELP"]*2)
						shift_config.setdefault("labels", []).extend([""] * 2)
						
						shift_config["directories"] = [args.input_dir]
						shift_config["nicks_blacklist"].append("noplot")
						shift_config["output_dir"] = os.path.expandvars(args.output_dir)
						shift_config["filename"] = "plot_es-shift_" + str(shift).replace(".","_") + "_" + decayMode + "_" + name_hash
						shift_config["legend"] = [0.7, 0.4, 0.95, 0.83]
						shift_config["cms"] = True
						shift_config["extra_text"] = "Preliminary"
						shift_config["energies"] = [13]
						shift_config["lumis"] = [float("%.1f" % args.lumi)]
						shift_config["title"] = "channel_"+channel
						shift_config["x_bins"] = "42,0.0,4.2"
						shift_config["x_label"] = "m_{#tau_{h}} (GeV)"
						if decayMode == "OneProngPiZeros" and quantity == "m_2":
							shift_config["x_bins"] = "39,0.3,4.2"
						elif decayMode == "ThreeProng" and quantity == "m_2":
							shift_config["x_bins"] = "7,0.8,1.5"
						elif decayMode == "OneProng" or quantity == "m_vis":
							shift_config["x_bins"] = "20,0.0,200.0"
							shift_config["x_label"] = "m_{#mu#tau_{h}} (GeV)"
						shift_config["y_lims"] = [0.0]
						shift_config["y_subplot_lims"] = [0.5, 1.5]
						shift_config["y_label"] = "Events / bin"
						
						plot_configs.append(shift_config)

				merged_config["directories"] = [args.input_dir]
				merged_config["nicks_blacklist"].append("noplot")
				merged_config["output_dir"] = os.path.expandvars(args.output_dir)
				merged_config["filename"] = decayMode + "_" + name_hash
				
				# set proper binnings of the distributions
				if decayMode == "OneProngPiZeros" and quantity == "m_2":
					merged_config.setdefault("x_bins", []).append(["39,0.3,4.2"])
				elif decayMode == "ThreeProng" and quantity == "m_2":
					merged_config.setdefault("x_bins", []).append(["7,0.8,1.5"])
				elif decayMode == "OneProng" or quantity == "m_vis":
					merged_config.setdefault("x_bins", []).append(["20,0.0,200.0"])

				# config to plot the fit
				if args.fit_method == "chi2":
					merged_config.setdefault("analysis_modules", []).append("AddHistograms")
					merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

					# for each shift, sum the ztt and bkg histograms
					for shift in args.es_shifts:
						all_samples = ["ztt_" + str(shift).replace(".", "_") + "_0"] + [nick + "_0" for nick in bkg_samples if nick + "_0" in merged_config["nicks"]]
						
						# needed for AddHistograms module
						merged_config.setdefault("histogram_nicks", []).append([" ".join(all_samples)])
						sum_result_nick = "noplot_ztt_" + str(shift).replace(".", "_") + "_0"
						merged_config.setdefault("sum_result_nicks", []).append([sum_result_nick])
						
						# needed for ExportRoot module
						merged_config.setdefault("labels", []).append([sum_result_nick])
						merged_config.setdefault("nicks_instead_labels", []).append([True])
						
						# needed for TauEsStudies module
						merged_config.setdefault("ztt_nicks", []).append([sum_result_nick])
						merged_config.setdefault("data_nicks", []).append(["data_0"])
						merged_config.setdefault("es_shifts", []).append([str(shift)])
						merged_config.setdefault("res_hist_nicks", []).append(["chi2_result"])
						merged_config["fit_method"] = "chi2"

					config_plotfit = {}
					config_plotfit["files"] = "plots/tauEsStudies_plots/" + decayMode + "_" + name_hash + ".root"
					config_plotfit["markers"] = ["LP"]
					config_plotfit["x_expressions"]  = ["chi2_result"]
					config_plotfit["filename"] = "chi2_" + decayMode + "_" + name_hash
					config_plotfit["x_label"] = "#tau_{ES}"
					config_plotfit["y_label"] = "#Delta#chi^{2}"
				
				elif args.fit_method == "logllh":
					merged_config.setdefault("analysis_modules", []).append("TauEsStudies")

					for index, (pt_range) in enumerate(args.pt_ranges):
						#needed for TauEsStudies module
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

					config_plotfit["files"] = "plots/tauEsStudies_plots/" + decayMode + "_" + name_hash + ".root"
					config_plotfit["markers"] = ["LP"]
					#config_plotfit["texts"] = [decayMode]
					config_plotfit["x_expressions"]  = ["logllh_result_0"]
					config_plotfit["filename"] = "logllh_" + decayMode + "_" + name_hash
					config_plotfit["x_label"] = "#tau_{ES}"
					config_plotfit["y_label"] = "-2NLL"

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
